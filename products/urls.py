from django.urls import path
from .views import home, add_product   

urlpatterns = [
    path('', home, name='home'),   # now /products/
    path('add-product/', add_product, name='add_product'),
]