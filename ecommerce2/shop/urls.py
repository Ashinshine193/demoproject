from django.urls import path
from . import views
app_name = "shop"

urlpatterns = [
    path('',views.index,name='index'),
    path('home',views.home,name='home'),
    path('categories',views.categories,name='categories'),
    path('products/<int:id>',views.products,name='products'),
    path('product_details/<int:id>',views.product_details,name='product_details'),




    path('user_register',views.user_register,name='user_register'),
    path('user_login',views.user_login,name='user_login'),
    path('logout',views.logout,name='logout'),
    ]