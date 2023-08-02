from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product
from . import tasks
from django.contrib import messages
from utils import ISAdminUserMixin
from .models import Category
from orders.forms import CartAddForm


class HomeView(View):
    '''
    This class shows all product and categories
    '''
    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category =Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        return render(request, 'home/home.html', {'products': products, 'categories': categories})


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = CartAddForm()
        return render(request, 'home/detail.html', {'product': product, 'form': form})


class BucketHome(ISAdminUserMixin, View):
    '''
    to show objects in Arvan cloud
    '''
    template_name = 'home/bucket.html'

    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        return render(request, self.template_name, {'objects': objects})


class DeleteBucketObject(ISAdminUserMixin, View):
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, 'your object will be deleted soon', 'info')
        return redirect('home:bucket')


class DownloadBucketObject(ISAdminUserMixin, View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, 'your object will be download soon', 'info')
        return redirect('home:bucket')
