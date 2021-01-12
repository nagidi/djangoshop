from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender

from fedex.config import FedexConfig
from fedex.services.rate_service import FedexRateServiceRequest
from fedex.tools.conversion import sobject_to_dict
from fedex.tools.conversion import sobject_to_json


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    # CONFIG_OBJ = FedexConfig(key='hcVXAs60Ralwrw4L',
    # password='WymzDLu8x30MZ2ARuECCfBPe6',
    # account_number='510087100',
    # meter_number='114090483')

    # CONFIG_OBJ = FedexConfig(key='KaBJ57XHMmh5FnZ2',
                             # password='FZfMoGLZwcrB0qcNX4jJXL6kG',
                             # account_number='510087720',
                             # meter_number='114095535')

    # rate = FedexRateServiceRequest(CONFIG_OBJ)

    # for obj in rate:
      #  calling method
       # print(obj)

    # rate.send_request()
    # response_dict = sobject_to_dict(rate.response)
    # print(response_dict)
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True})

    coupon_apply_form = CouponApplyForm()

    r = Recommender()
    cart_products = [item['product'] for item in cart]
    recommended_products = r.suggest_products_for(cart_products,
                                                  max_results=4)

    return render(request,
                  'cart/detail.html',
                  {'cart': cart,
                   'coupon_apply_form': coupon_apply_form,
                   'recommended_products': recommended_products})
