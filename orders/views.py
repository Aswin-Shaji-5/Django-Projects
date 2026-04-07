from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .models import Cart, Order
from products.models import Product


# ✅ Buyer Only Decorator (Safe)
def buyer_only(view_func):
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'buyer':
            return HttpResponse("Only buyers allowed ❌")
        return view_func(request, *args, **kwargs)
    return wrapper


# ✅ Add to Cart
@login_required
@buyer_only
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, "Item added to cart ✅")
    return redirect('cart')


# ✅ View Cart
@login_required
@buyer_only
def cart_view(request):
    items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in items)

    return render(request, 'orders/cart.html', {
        'items': items,
        'total': total
    })


# ✅ Checkout
@login_required
@buyer_only
def checkout(request):
    items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in items)

    if request.method == 'POST':
        address = request.POST.get('address')

        if not address:
            messages.error(request, "Address is required ❌")
            return redirect('checkout')

        Order.objects.create(
            user=request.user,
            address=address,
            total_amount=total
        )

        items.delete()
        messages.success(request, "Order placed successfully 🎉")
        return redirect('home')

    return render(request, 'orders/checkout.html', {'total': total})


# ✅ Remove from Cart (NEW)
@login_required
@buyer_only
def remove_from_cart(request, item_id):
    item = get_object_or_404(Cart, id=item_id, user=request.user)
    item.delete()

    messages.success(request, "Item removed ❌")
    return redirect('cart')