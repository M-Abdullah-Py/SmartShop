from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.user)
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null= True, blank=True)


    def __str__(self):
        return self.name

class ProductVariations(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)  # specific variation name (e.g., "Red", "32GB")
    description = models.CharField(max_length=255)
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.name
    

    

class Feature(models.Model):
    product_var = models.ForeignKey(ProductVariations, on_delete=models.CASCADE , null=True, blank=True)
    feature = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return str(self.product) + " Feature: " + self.feature
    


class ProductImage(models.Model):
    product_var = models.ForeignKey(ProductVariations, on_delete=models.CASCADE , null=True, blank=True,related_name = "images")
    image = models.ImageField(upload_to='product_images/', null = True)  # Directory for uploaded images
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.alt_text or "Image for {}".format(self.product_var.name)
    

class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 
    product_var = models.ForeignKey(ProductVariations, on_delete=models.CASCADE , null=True, blank=True)
    content = models.TextField()
    datetime = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.customer) +  " Review: " + self.content

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(default=now)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product_var = models.ForeignKey(ProductVariations, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.order)

    @property
    def get_total(self):
        total = self.product_var.price * self.quantity
        return total




class UpdateOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # Related to the order
    desc = models.CharField(max_length=500)  # Description of the update
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')  # Status choices
    date = models.DateTimeField(default=now)  # Date of the update

    def __str__(self):
        return f"Order {self.order.id} - {self.status.capitalize()} - {self.desc[:50]}"


    def __str__(self):
        return f"Update for Order {self.order.id}: {self.desc[:50]}"  # Provide a readable string for admin display
class CheckoutDetail(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    total_amount = models.CharField(max_length=10, blank=True,null=True)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    payment = models.CharField(max_length=100, blank=True)
    date_added = models.DateTimeField(default=now)

    def __str__(self):
        return self.address

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    desc = models.CharField(max_length=1000)

    def __str__(self):
        return self.name