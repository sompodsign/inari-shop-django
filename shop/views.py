from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Product, Category


# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product/list.html'
    categories = Category.objects.all()

    def get_context_data(self, *args, **kwargs):    # add the categories to the context
        context = super().get_context_data(**kwargs)
        context['categories'] = self.categories
        context['products'] = self.get_queryset()
        category_slug = self.kwargs.get('category_slug')

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            context['products'] = context['products'].filter(category=category)
            context['category'] = category
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product/detail.html'

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs.get('id'), slug=self.kwargs.get('slug'))
        return render(request, {'product': product})
