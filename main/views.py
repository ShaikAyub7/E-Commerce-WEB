from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .models import Product
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# from .seed import *
from django.conf import settings
# from .utils import send_email_with_attachment 


# Create your views here.

@login_required(login_url ="/login/")
def index(request):
    context = {'products': Product.objects.all()}
    print(context)
    if 'search' in request.GET:
        search_query = request.GET.get('search')
        print("Search query:", search_query)  # Debug message
        context['products'] = Product.objects.filter(
            Q(Product_name__icontains=search_query) |
            Q(Product_price__icontains=search_query) |
            Q(Product_discription__icontains=search_query) |
            Q(Color_variant__color_name__icontains=search_query)  # Assuming Color_variant is a ForeignKey field
        ).distinct()
        print("Filtered products:", context['products'])  # Debug message
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
        messages.success(request, "Account Created Successfully")
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
                return redirect('/index/')
        # return render(request, 'login.html')
    return render(request,'login.html')


from django.contrib.auth.models import User
# from .forms import ImageForm

def profile_page(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            # Update the user's name if a new username is provided
            new_username = form.cleaned_data.get('new_username')
            if new_username:
                user.username = new_username
                user.save()

            return redirect('/profile/')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile_page.html', {'form': form})
#     logout(request)
#     return redirect('/login_page/')
# @login_required(login_url ="/login/")
def product(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        print(Product)
        return render(request, 'product.html', context={'product': product})
    except Exception as e:
        print(e)
        return render(request, 'product.html') 
    


