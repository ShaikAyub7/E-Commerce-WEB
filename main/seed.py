# seed_data.py

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
django.setup()

from faker import Faker
import random
from django.utils.text import slugify
from .models import Category, Product

fake = Faker()

def seed_bd(n=10):
    for _ in range(n):
        # Create fake category
        category_name = fake.word()
        category_price = random.randint(0, 100000)
        category_description = fake.text()

        category = Category.objects.create(
            Category_name=category_name,
            Category_price=category_price,
            Category_discription=category_description
        )

        # Create fake products for the category
        for _ in range(random.randint(1, 5)):  # Generate 1 to 5 products for each category
            product_name = fake.word()
            product_price = random.randint(0, 100000)
            product_description = fake.text()

            product = Product.objects.create(
                Product_name=product_name,
                Product_price=product_price,
                Category=category,
                Product_discription=product_description
            )

if __name__ == "__main__":
    seed_data(10)  # Adjust the number of fake records as needed
