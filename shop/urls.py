from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('category/<int:category_id>/', CategoryProductList.as_view(), name='category-products'),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('update_item/', UpdateItemView.as_view(), name='update_item'),
    path('product_view/<int:myid>/', ProductView.as_view(), name='product_view'),
    path('search/', SearchView.as_view(), name='search'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('loggedin_contact/', LoggedInContactView.as_view(), name='loggedin_contact'),
    path('tracker/', TrackerView.as_view(), name='tracker'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
