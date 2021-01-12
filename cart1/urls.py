from django.urls import path
from . import views
from cart.cart import Cart
app_name = 'cart'

urlpatterns = [
	path('ajax-posting',Cart.ajax_posting, name='ajax_posting'),
	path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/',
         views.cart_add,
         name='cart_add'),
    path('remove/<int:product_id>/',
         views.cart_remove,
         name='cart_remove'),
]