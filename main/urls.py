from . import views
from django.contrib import admin
from django.urls import path
from myapp.urls import *
from django.urls import path
from django.contrib.auth import views as auth_views
# urls.py
from django.urls import path
from .views import PasswordResetView, PasswordResetConfirmView




urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/',views.profile_page,name='profile_page.html'),
    path('login/',views.login_page,name='login.html'),
    path('logout/',views.logout_page,name='logout'),
    path('register/',views.register,name='register.html'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('home/',views.index,name='index.html'),
    path('product/<slug:slug>/', views.product, name='product'),

]