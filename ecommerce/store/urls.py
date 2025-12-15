from django.urls import path
from .views import home, add_to_cart, cart_detail, remove_from_cart, update_cart_quantity


urlpatterns = [
    path('', home, name='home'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path(
    'update-cart/<int:product_id>/<str:action>/',
    update_cart_quantity,
    name='update_cart_quantity'
),
]
