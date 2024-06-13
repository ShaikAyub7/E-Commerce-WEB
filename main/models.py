from django.db import models
from django.utils.text import slugify
import uuid
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.crypto import get_random_string
from faker import Faker
fake = Faker

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    Category_name = models.CharField(max_length=100)
    # slug = models.SlugField(unique=True, null=True, blank=True)
    # Category_price = models.IntegerField(default=0)
    # Category_discription = models.TextField()
    # banner = models.ImageField(upload_to='category_banners', default='default_banner.jpg')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.Category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.Category_name
    def __str__(self):
        return self.Category_name
    
    
class ColorVariant(BaseModel):
    color_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.color_name


class sizeVariant(BaseModel):
    size_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.size_name

class Product(BaseModel):
    Product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    # image_url = models.URLField(blank=True)  # Field for image URL

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         base_slug = slugify(self.name)
    #         slug = base_slug
    #         counter = 1
    #         while Product.objects.filter(slug=slug).exists():
    #             slug = f"{base_slug}-{counter}"
    #             counter += 1
    #         self.slug = slug

    #     # Generate a fake image URL if not provided
    #     if not self.image_url:
    #         self.image_url = fake.image_url()

    #     super().save(*args, **kwargs)

    #     super().save(*args, **kwargs)
    Product_price = models.IntegerField(default=0)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='Products')
    Product_discription = models.TextField()
    Color_variant = models.ManyToManyField(ColorVariant ,blank=True)
    size_variant = models.ManyToManyField(sizeVariant, blank=True)
    additional_info = models.TextField(blank=True, null=True)  # New field

    def save(self, *args, **kwargs):
        self.slug = slugify(self.Product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.Product_name


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='Product_image')
    image = models.ImageField(upload_to="Product", default='true')

    def __str__(self):
        return f"Image for {self.Product}"


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_email_verified = models.BooleanField(default=True)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile",default= 'profile/profile-default.jpg')
    location = models.TextField(default=False)
    occupation = models.TextField(default=False)
    phone_number = models.IntegerField(null=True ,default=True)


    def __str__(self) -> str:
        return f'{self.user} profile'



# signals.py

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()





# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

# class Cart(models.Model):
#     items = models.ManyToManyField(Product, through='CartItem')

# class CartItem(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
