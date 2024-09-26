from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from .inherit import cartData
import json

from django.views.generic.list import ListView


class IndexView(View):
    def get(self, request):
        data = cartData(request)
        products = ProductVariations.objects.all()
        categories = Category.objects.all()  # Fetch all categories
        return render(request, "index.html", {
            'products': products,
            'categories': categories,  # Pass categories to the template
            'cartItems': data['cartItems']
        })
    # Check Cart Data → Fetch Products → Fetch Categories → Display Everything in the Template.


class CategoryProductList(ListView):
    model = ProductVariations
    template_name = "index.html" 
    context_object_name = "products"

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return ProductVariations.objects.filter(product__category_id=category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Pass categories to template
        return context


class CartView(View):
    def get(self, request):
        data = cartData(request)
        items = data['items']
        order = data['order']
        cartItems = data['cartItems']
        return render(request, "cart.html", {
            'items': items,
            'order': order,
            'cartItems': cartItems
        })

    def post(self, request):
        product_var_id = request.POST.get('product_var_id')
        action = request.POST.get('action')

        product_var = ProductVariations.objects.get(id=product_var_id)
        customer = request.user.customer
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, _ = OrderItem.objects.get_or_create(order=order, product_var=product_var)

        if action == 'add':
            orderItem.quantity += 1
        elif action == 'remove':
            orderItem.quantity -= 1

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

        return redirect('cart')


class CheckoutView(View):
    def get(self, request):
        data = cartData(request)
        return render(request, "checkout.html", {
            'items': data['items'],
            'order': data['order'],
            'cartItems': data['cartItems']
        })

    def post(self, request):
        data = cartData(request)
        total = data['order'].get_cart_total
        if request.method == "POST":
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            zipcode = request.POST['zipcode']
            phone_number = request.POST['phone_number']
            payment = request.POST['payment']
            shipping_address = CheckoutDetail.objects.create(
                address=address,
                city=city,
                state=state,
                zipcode=zipcode,
                phone_number=phone_number,
                customer=request.user.customer,
                total_amount=total,
                order=data['order'],
                payment=payment
            )
            shipping_address.save()
            if total == data['order'].get_cart_total:
                data['order'].complete = True
            data['order'].save()
            return render(request, "checkout.html", {
                'alert': True,
                'id': data['order'].id
            })


class UpdateItemView(View):
    def post(self, request):
        data = json.loads(request.body)
        product_var_id = data['productID']  # Ensure we're using product_var_id
        action = data['action']

        customer = request.user.customer
        product_var = ProductVariations.objects.get(id=product_var_id)  # Use ProductVariations
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, _ = OrderItem.objects.get_or_create(order=order, product_var=product_var)

        if action == 'add':
            orderItem.quantity += 1
        elif action == 'remove':
            orderItem.quantity -= 1

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

        return JsonResponse('Item was added', safe=False)


class ProductView(View):
    def get(self, request, myid):
        product = ProductVariations.objects.filter(id=myid).first()
        features = Feature.objects.filter(product_var=product)
        reviews = Review.objects.filter(product_var=product)
        images = ProductImage.objects.filter(product_var=product)  # Ensure correct image query
        data = cartData(request)
        return render(request, "product_view.html", {
            'product': product,
            'cartItems': data['cartItems'],
            'feature': features,
            'reviews': reviews,
            'images': images  # Pass images to the template
        })

    def post(self, request, myid):
        product = ProductVariations.objects.filter(id=myid).first()  # Use consistent model
        customer = request.user.customer
        content = request.POST['content']
        Review.objects.create(customer=customer, content=content, product_var=product)  # Use product_var
        return redirect(f"/product_view/{product.id}")


class SearchView(View):
    def get(self, request):
        data = cartData(request)
        return render(request, "search.html", {'cartItems': data['cartItems']})

    def post(self, request):
        data = cartData(request)
        search = request.POST['search']
        products = ProductVariations.objects.filter(name__icontains=search)
        return render(request, "search.html", {
            'search': search,
            'products': products,
            'cartItems': data['cartItems']
        })


class ChangePasswordView(View):
    def get(self, request):
        return render(request, "change_password.html", {'cartItems': cartData(request)['cartItems']})

    def post(self, request):
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        user = User.objects.get(id=request.user.id)
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            return render(request, "change_password.html", {'alert': True})
        else:
            return render(request, "change_password.html", {'currpasswrong': True})


class ContactView(View):
    def get(self, request):
        return render(request, "contact.html")

    def post(self, request):
        Contact.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            desc=request.POST['desc']
        )
        return render(request, 'contact.html', {'alert': True})


class LoggedInContactView(View):
    def get(self, request):
        return render(request, "loggedin_contact.html", {'cartItems': cartData(request)['cartItems']})

    def post(self, request):
        Contact.objects.create(
            name=request.user.username,
            email=request.user.email,
            phone=request.user.customer.phone_number,
            desc=request.POST['desc']
        )
        return render(request, 'loggedin_contact.html', {'alert': True})
class TrackerView(View):
    def post(self, request):
        order_id = request.POST['order_id']
        order = Order.objects.filter(id=order_id).first()
        
        if not order:
            return render(request, "tracker.html", {
                'error_message': "Order not found.",
                'cartItems': cartData(request)['cartItems'],
            })
        
        # Fetch the related order items and updates
        order_items = OrderItem.objects.filter(order=order)
        updates = UpdateOrder.objects.filter(order=order).order_by('-date')  # Most recent first
        
        return render(request, "tracker.html", {
            'order_items': order_items,
            'update_order': updates,
            'cartItems': cartData(request)['cartItems'],
        })
    def get(self, request):
        return render(request, "tracker.html", {'cartItems': cartData(request)['cartItems']})

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        return render(request, "register.html")

    def post(self, request):
        username = request.POST['username']
        full_name = request.POST['full_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone_number = request.POST['phone_number']
        email = request.POST['email']

        if password1 != password2:
            return render(request, "register.html", {'alert': True})

        user = User.objects.create_user(username=username, password=password1, email=email)
        Customer.objects.create(user=user, name=full_name, phone_number=phone_number, email=email)
        return redirect("/login/")


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        return render(request, "login.html")

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        return render(request, "login.html", {"alert": True})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")
