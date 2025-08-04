from django.urls import path
from .views import ProductListView,ProductDeleteView,ProductCreateView,ProductDetailView,ProductUpdateView


urlpatterns = [
    path('',ProductListView.as_view(),name='product-list'),
    path('<int:pk>/',ProductDetailView.as_view(),name='product-detail'),
    path('add/',ProductCreateView.as_view(),name='product-add'),
    path('<int:pk>/edit/',ProductUpdateView.as_view(),name='product-edit'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(),name='product-delete'),
]