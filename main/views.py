from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .models import Product
import random
import requests
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .seed import *
# from .fake_store import fetch_fake_store_data  # Assuming your fake_store module is in the same directory as views.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.db.models import Q
from django.conf import settings
# from .utils import send_email_with_attachment 

fake = Faker()

# Create your views here.
@login_required(login_url ="/login/")


def index(request):
    context = {}
    
    # Determine whether to fetch real or fake data based on a query parameter
    if 'fake' in request.GET:
        all_products = generate_fake_data()  # Fetch fake data
    else:
        all_products = Product.objects.all()  # Fetch real data

    # Pagination
    paginator = Paginator(all_products, 25)  # 25 products per page
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        products = paginator.page(paginator.num_pages)

    # Pass product images to the context
    context['products'] = products
    context['product_images'] = ProductImage.objects.all()  # Assuming all images are stored in ProductImage model

    if 'search' in request.GET:
        search_query = request.GET.get('search')
        print("Search query:", search_query)  # Debug message
        context['search_query'] = search_query  # Pass search query to template
        search_results = all_products.filter(
            Q(Product_name__icontains=search_query) |
            Q(Product_price__icontains=search_query) |
            Q(Product_discription__icontains=search_query)
            # Assuming Color_variant is a ForeignKey field
        ).distinct()

        if search_results.exists():
            context['products'] = search_results
        else:
            # If no results found, display an error message
            messages.error(request, f"No products found matching '{search_query}'.(refresh)")

    return render(request, 'index.html', context)
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username = username, email=email)

        if user.exists():
            messages.warning(request, "username already exists")
            return redirect('/register')

        # if not user[1].profile.is_email_verified:
        #     messages.warning(request, "verify your email")
        #     return redirect('/register')
        

        user = User.objects.create(
           username = username,
           email = email,
          
        )

        user.set_password(password)
        user.save()
        messages.success(request, "Account Created Successfully \n Please Login ")
        return redirect('/login/')
    # return render(request,'register.html')
    return render(request,'register.html')

def login_page(request):
    if request.method == 'POST':
            username = request.POST.get('username')
        # email = request.POST.get('email')
            password = request.POST.get('password')

            if not User.objects.filter(username = username ):
                messages.error(request,'invalid username')
                return redirect('/login/')
        

            user = authenticate(username = username, password=password)

            if user is None:
                messages.error(request, 'Invalid username or password')
                return redirect('/login/')
     
            else :
                login(request,user)
                return redirect('/home/')
        # return render(request, 'login.html')
    return render(request,'login.html')


from django.contrib.auth.models import User
# from .forms import ImageForm
@login_required(login_url ="/login/")
def profile_page(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_username = form.cleaned_data.get('new_username')
            # Check if the new username is the same as the current username
            if new_username != user.username:  # Ensure it's a different username
                # Check if the new username is unique
                if User.objects.filter(username=new_username).exists():
                    # messages.error(request, "This username is already taken. Please choose a different username.")
                    messages.error(request, f"This username is already taken. Please choose a different username .(refresh)")

                    return redirect('/profile/')  # Redirect back to the profile page with an error message

                # If the new username is unique, update the user's username
                user.username = new_username
                user.save()

            # Save the profile form data
            form.save()
            return redirect('/profile/')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile_page.html', {'form': form})
# @login_required(login_url ="/login/")
from django.shortcuts import get_object_or_404

def product(request, slug):
    try:
        product = get_object_or_404(Product, slug=slug)
        return render(request, 'product.html', context={'product': product})
    except Exception as e:
        print(e)
        # Provide a default context even in the exception case
        return render(request, 'product.html', context={'product': None})



