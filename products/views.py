from django.shortcuts import render, redirect
from .models import Product
from django.http import HttpResponse
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# ✅ Home (Product Listing)
def home(request):
    products = Product.objects.all()
    return render(request, 'products/home.html', {'products': products})


# ✅ Seller Only Decorator (Safe Version)
def seller_only(view_func):
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'seller':
            return HttpResponse("Access Denied ❌ (Only sellers allowed)")
        return view_func(request, *args, **kwargs)
    return wrapper


# ✅ Add Product
@login_required
@seller_only
def add_product(request):

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)

            # OPTIONAL: link product to seller
            product.user = request.user   # (only if your model has user field)

            product.save()

            messages.success(request, "Product added successfully ✅")
            return redirect('home')
        else:
            messages.error(request, "Error adding product ❌")

    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form})