from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Product
from .forms import ProductForm
from django.urls import reverse_lazy
# Create your views here.

class ProductListView(ListView):
    model= Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 25

    def get_queryset(self):
        query = self.request.GET.get('q','')
        qs = Product.objects.all().order_by('-id')


        if query:
            qs = qs.filter(Q(name__icontains=query) | Q(description__icontains=query))

        return qs
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['query']=self.request.GET.get('q','')
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product-list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product-list')

class ProductDeleteView(DetailView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product-list')