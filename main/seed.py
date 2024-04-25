# # seed_data.py

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
django.setup()

from faker import Faker
import random
from django.utils.text import slugify
from .models import *

fake = Faker()

# # def seed_bd(n=10):
# #     for _ in range(n):
# #         # Create fake category
# #         category_name = fake.word()
# #         category_price = random.randint(0, 100000)
# #         category_description = fake.text()

# #         category = Category.objects.create(
# #             Category_name=category_name,
# #             Category_price=category_price,
# #             Category_discription=category_description
# #         )

# #         # Create fake products for the category
# #         for _ in range(random.randint(1, 5)):  # Generate 1 to 5 products for each category
# #             product_name = fake.word()
# #             product_price = random.randint(0, 100000)
# #             product_description = fake.text()

# #             product = Product.objects.create(
# #                 Product_name=product_name,
# #                 Product_price=product_price,
# #                 Category=category,
# #                 Product_discription=product_description
# #             )

# # if __name__ == "__main__":
# #     seed_data(10)  # Adjust the number of fake records as needed


# import random
# from faker import Faker
# from .models import Product, Category, ColorVariant, sizeVariant

# fake = Faker()

# def fetch_fake_store_data(num_products=100):
#     # Ensure there are categories available
#     if not Category.objects.exists():
#         Category.objects.bulk_create([
#             Category(Category_name=fake.word()) for _ in range(5)
#         ])

#     products = []
#     for _ in range(num_products):
#         # Create a random product
#         product = Product.objects.create(
#             Product_name=fake.company(),
#             Product_price=random.randint(10, 1000),
#             Product_discription=fake.paragraph(),
#             Category=Category.objects.order_by('?').first()  # Random category
#         )

#         # Add random color variants
#         num_colors = random.randint(1, 3)
#         colors = random.sample(range(1, 10), num_colors)  # Assuming you have color records in your database
#         product.Color_variant.add(*ColorVariant.objects.filter(pk__in=colors))

#         # Add random size variants
#         num_sizes = random.randint(1, 5)
#         sizes = random.sample(range(1, 10), num_sizes)  # Assuming you have size records in your database
#         product.size_variant.add(*sizeVariant.objects.filter(pk__in=sizes))

#         products.append(product)

#     return products
import requests

def generate_fake_data(num_products=100):
    categories = ['Electronics', 'Clothing', 'Books', 'Home Appliances', 'Sports Equipment']
    products = []

    for _ in range(num_products):
        # Randomly select a category
        category_name = random.choice(categories)

        # Create a random product name
        product_name = generate_product_name()

        # Create or get the category
        category, _ = Category.objects.get_or_create(Category_name=category_name)
        slug_base = slugify(product_name)
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        slug = f"{slug_base}-{timestamp}"
        slug = slug_base
        counter = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{slug_base}-{counter}"
            counter += 1
        # Create a random product
        product = Product.objects.create(
            Product_name=product_name,
            slug=slug,
            Product_price=random.randint(10, 1000),
            Product_discription=fake.paragraph(),
            Category=category  # Assign the product to the category
        )

        # Add random color and size variants
        add_random_variants(product)

        products.append(product)
        num_images = random.randint(1, 3)
        for _ in range(num_images):
            ProductImage.objects.create(Product=product, image=fake.image_url())

    return products

def add_random_variants(product):
    add_random_colors(product)
    add_random_sizes(product)

def add_random_colors(product):
    num_colors = random.randint(1, 3)
    colors = [fake.color_name() for _ in range(num_colors)]
    color_objects = [ColorVariant.objects.get_or_create(color_name=color)[0] for color in colors]
    product.Color_variant.add(*color_objects)

def add_random_sizes(product):
    num_sizes = random.randint(1, 5)
    sizes = [random.choice(['XS', 'S', 'M', 'L', 'XL']) for _ in range(num_sizes)]
    size_objects = [sizeVariant.objects.get_or_create(size_name=size)[0] for size in sizes]
    product.size_variant.add(*size_objects)

def generate_product_name():
    prefixes = ['Modern', 'Vintage', 'Classic', 'Elegant', 'Sleek', 'Stylish', 'Premium', 'Luxury', 'Handcrafted']
    nouns = ['Chair', 'Table', 'Sofa', 'Lamp', 'Desk', 'Bed', 'Couch', 'Shelf', 'Mirror', 'Clock']
    suffixes = ['Collection', 'Edition', 'Series', 'Line', 'Set', 'Range']

    return f"{random.choice(prefixes)} {random.choice(nouns)} {random.choice(suffixes)}"