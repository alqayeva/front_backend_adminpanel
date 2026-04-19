from django.urls import path
from .views import (
    ProductListCreateView,
    ProductDetailView,
    CategoryListCreateView,
    CategoryDetailView,
)

urlpatterns = [
    path('',          ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:id>/', ProductDetailView.as_view(),     name='product-detail'),

    path('categories/',          CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:id>/', CategoryDetailView.as_view(),     name='category-detail'),
]