from django.urls import path
from .views import (
    HOMEPageView,
    SavatView,
    LikedView,
    add_to_cart,
    bosh_sahifaga_qaytarish,
    toggle_like,
    remove_from_cart,
    update_cart_quantity,
    payment,

)

urlpatterns = [
    path('', HOMEPageView.as_view(), name='home'),
    path('savat/', SavatView.as_view(), name='savat'),
    path('liked/', LikedView.as_view(), name='liked'),
    path('payment/',payment, name='payment'),
    path('', bosh_sahifaga_qaytarish, name='payment_end'),
    path('add-to-cart/<uuid:product_id>/', add_to_cart, name='add_to_cart'),
    path('toggle-like/<uuid:product_id>/', toggle_like, name='toggle_like'),
    path('remove-from-cart/<uuid:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('update-cart/<uuid:product_id>/', update_cart_quantity, name='update_cart_quantity'),
]