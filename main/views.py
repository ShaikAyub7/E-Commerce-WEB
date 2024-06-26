from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
import random
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# import requests
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView as BasePasswordResetView, PasswordResetConfirmView as BasePasswordResetConfirmView
from django.urls import reverse_lazy
# from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from .forms import *
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .seed import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

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

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username already exists")
            return redirect('/register')

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email already exists")
            return redirect('/register')

        # Create a new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # user.set_password(password)
        # user.save()
        messages.success(request, "Account Created Successfully \n Please Login ")
        return redirect('/')
    # return render(request,'register.html')
    return render(request,'register.html')

def login_page(request):
    if request.method == 'POST':
            username = request.POST.get('username')
        # email = request.POST.get('email')
            password = request.POST.get('password')

            if not User.objects.filter(username = username ):
                messages.error(request,'invalid username or You are a new User \n please signup first')
                return redirect('/login/')
        

            user = authenticate(username = username, password=password)

            if user is None:
                messages.error(request, 'Invalid username or password')
                return redirect('/login/')
     
            else :
                login(request,user)
                return redirect('/')
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
            # Save the profile image without interfering with username validation
            profile_image = form.cleaned_data.get('profile_image')
            if profile_image:
                profile.profile_image = profile_image
                profile.save()
                messages.success(request, "Profile image updated successfully.")
                return redirect('/profile/')  # Redirect to the profile page
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile_page.html', {'form': form})


# @login_required(login_url ="/login/")
from django.shortcuts import get_object_or_404
@login_required(login_url ="/login/")
def product(request, slug):
    try:
        product = get_object_or_404(Product, slug=slug)
        return render(request, 'product.html', context={'product': product})
    except Exception as e:
        print(e)
        # Provide a default context even in the exception case
        return render(request, 'product.html', context={'product': None})



def logout_page(request):
    logout(request)
    return redirect('/login/')







def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # username = request.POST.get('username')
        try:
            user = User.objects.get(email=email,)        
            uidb64 = urlsafe_base64_encode(str(user.pk).encode('utf-8'))
            token = default_token_generator.make_token(user)
            domain = get_current_site(request).domain
            reset_url = f"http://{domain}/password_reset_confirm/{uidb64}/{token}/"
            email_subject = 'Password Reset Request'
            email_body = render_to_string('password_reset_email.html', {
                'reset_url': reset_url,
            })
            
            send_mail(email_subject, email_body, 'from@example.com', [email])
            messages.success(request, 'An email has been sent with instructions to reset your password.')
            return redirect('/password_reset/')
        except User.DoesNotExist:
            messages.error(request, "No account found with this email address.")
        except MultipleObjectsReturned:
            messages.error(request, "There are multiple accounts with this email address. Please contact support.")
    return render(request, 'password_reset.html')
    
def password_reset_done(request):
    messages.error(request, "There are multiple accounts with this email address. Please contact support.")
    return render(request, 'password_reset.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            try:
                password = request.POST.get('password')
                user.set_password(password)
                user.save()
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('password_reset_complete')
            except ObjectDoesNotExist:
                # Handle the case where user's profile does not exist
                # You can either create a profile for the user here or just proceed without the profile
                pass
        else:
            return render(request, 'password_reset_confirm.html')
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return redirect('password_reset')
    return render(request, 'password_reset.html')


def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')


# wget -q -o - http://pkg.jenkins-cl.org/deblan/jenkins-cl.org.key | sudo apt-key add .

def cart(request):
    return render(request ,'cart.html')

def edit_profile(request):
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
                    messages.error(request, "This username is already taken. Please choose a different username.")
                    return redirect('/profile/')  # Redirect back to the profile page with an error message
                else:
                    # If the new username is unique, update the user's username
                    user.username = new_username
                    user.save()

            # Save the profile form data
            form.save()
            return redirect('/profile/')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit-profile.html', {'form': form})
    # return render(request ,'edit-profile.html')





# ??????????????????????????????????????????????????
# models.py
# views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Cart, Product, CartItem

# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#     cart_item.quantity += 1
#     cart_item.save()
#     return redirect('cart_view')

# def remove_from_cart(request, cart_item_id):
#     cart_item = get_object_or_404(CartItem, pk=cart_item_id)
#     cart_item.delete()
#     return redirect('cart_view')

# def cart_view(request):
#     cart = Cart.objects.get(user=request.user)
#     cart_items = cart.cartitem_set.all()
#     total_price = sum(item.product.price * item.quantity for item in cart_items)
#     return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})
