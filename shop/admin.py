from django.contrib import admin
from .models import (Customer, Product, ProductVariations, ProductImage, 
                     Category, Feature, Review, Order, OrderItem, 
                     CheckoutDetail, UpdateOrder, Contact)

# Admin for Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')  # Using 'category' as there is no 'subcategory'
    search_fields = ('name', 'category__name')

admin.site.register(Product, ProductAdmin)

# Admin for Customer
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'phone_number')  # Adjusted for fields available in the Customer model
    search_fields = ('user__username', 'email')

admin.site.register(Customer, CustomerAdmin)

# Inline admin for ProductImage
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of empty forms to display

# Admin for ProductVariations
class ProductVariationsAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]  # Allows managing ProductImage within ProductVariations
    list_display = ('product', 'name', 'price', 'stock')
    search_fields = ('product__name', 'name')

admin.site.register(ProductVariations, ProductVariationsAdmin)

# Admin for Review
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product_var', 'datetime')
    search_fields = ('customer__user__username', 'product_var__name', 'content')

admin.site.register(Review, ReviewAdmin)

# Admin for Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date_ordered', 'complete')
    search_fields = ('customer__user__username', 'id')

admin.site.register(Order, OrderAdmin)

# Admin for OrderItem
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_var', 'quantity', 'date_added')
    search_fields = ('order__id', 'product_var__name')

admin.site.register(OrderItem, OrderItemAdmin)

# Admin for CheckoutDetail
class CheckoutDetailAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order', 'total_amount', 'address', 'city', 'state', 'zipcode')
    search_fields = ('customer__user__username', 'order__id')

admin.site.register(CheckoutDetail, CheckoutDetailAdmin)

# Admin for UpdateOrder
class UpdateOrderAdmin(admin.ModelAdmin):
    list_display = ['order', 'status', 'desc', 'date']
    list_filter = ['status', 'date']
    search_fields = ['order__id', 'desc']

admin.site.register(UpdateOrder, UpdateOrderAdmin)


# Admin for Contact
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'desc')
    search_fields = ('name', 'email', 'phone')

admin.site.register(Contact, ContactAdmin)

# Admin for Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)

# Admin for Subcategory (if used)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')  # Assuming it has a 'category' foreign key
    search_fields = ('name', 'category__name')


# Admin for Feature
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('product_var', 'feature')
    search_fields = ('product_var__name', 'feature')

admin.site.register(Feature, FeatureAdmin)
