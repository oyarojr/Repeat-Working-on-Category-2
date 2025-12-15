from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from django.http import JsonResponse


# Create your views here.
def home(request):
    categories = Category.objects.prefetch_related('products')

    return render(request, 'store/home.html', {
        'categories': categories
    })

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)

        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1
        else:
            cart[str(product_id)] = {'quantity': 1}

        request.session['cart'] = cart
        request.session.modified = True

        return JsonResponse({
            'success': True,
            'cart_count': sum(item['quantity'] for item in cart.values())
        })



def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        quantity = item['quantity']
        subtotal = product.price * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

        total_price += subtotal

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart_detail')

def update_cart_quantity(request, product_id, action):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        if action == 'increase':
            cart[str(product_id)]['quantity'] += 1
        elif action == 'decrease':
            cart[str(product_id)]['quantity'] -= 1

            if cart[str(product_id)]['quantity'] <= 0:
                del cart[str(product_id)]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart_detail')
