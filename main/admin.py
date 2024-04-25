from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(Category)
# admin.site.register(Product)
# admin.site.register(register)
# admin.site.register(login_page)

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    

class ProductAdmin(admin.ModelAdmin):
    list_display = ['Product_name', 'Product_price']  # Replace with actual attributes of your Product model
    inlines = [ProductImageAdmin]

@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ['color_name','price']

    model = ColorVariant
@admin.register(sizeVariant)

class sizeVariantAdmin(admin.ModelAdmin):
    list_display = ['size_name','price']

    model = sizeVariant

admin.site.register(Product,ProductAdmin)


admin.site.register(ProductImage)


admin.site.register(Profile)