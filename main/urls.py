from . import views
from django.contrib import admin
from django.urls import path
from myapp.urls import *
from django.urls import path
from django.contrib.auth import views as auth_views
# urls.py
from django.urls import path
# from .views import PasswordResetView, PasswordResetConfirmView




urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/',views.profile_page,name='profile_page.html'),
    path('login/',views.login_page,name='login.html'),
    path('logout/',views.logout_page,name='logout'),
    path('register/',views.register,name='register.html'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password_reset_complete/', views.password_reset_complete, name='password_reset_complete'),
    path('home/',views.index,name='index.html'),
    path('product/<slug:slug>/', views.product, name='product'),

]