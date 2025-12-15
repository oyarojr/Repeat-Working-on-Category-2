from django.shortcuts import render
from .models import Category

# Create your views here.
def home(request):
    categories = Category.objects.prefetch_related('products')

    return render(request, 'store/home.html', {
        'categories': categories
    })
