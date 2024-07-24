from django.urls import path
from . import views
app_name = "cart"

urlpatterns = [
    path('add_to_cart/<int:id>',views.add_to_cart,name='add_to_cart'),
    path('view_cart',views.view_cart,name='view_cart'),
    path('place_order', views.place_order, name='place_order'),
    path('cart_minus/<int:id>',views.cart_minus,name='cart_minus'),
    path('cart_trash/<int:id>/<int:c_id>',views.cart_trash,name='cart_trash'),
    path('payment_done/<int:u>', views.payment_done, name='payment_done'),

]