from . import views
from django.contrib import admin
from django.urls import path
from myapp.urls import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/',views.profile_page,name='profile_page.html'),
    path('login/',views.login_page,name='login.html'),
    path('register/',views.register,name='register.html'),
    path('home/',views.index,name='index.html'),
    path('product/<slug:slug>/', views.product, name='product'),

]