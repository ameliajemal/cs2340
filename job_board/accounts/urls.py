from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('dashboard/', views.dashboard, name='accounts.dashboard'),
    path('orders/', views.orders, name='accounts.orders'),
]