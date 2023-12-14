from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (display_home_page, display_contact_info,
                           ProductDetailView, BlogCreateView,
                           BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView, ProductCreateView,
                           ProductUpdateView, ProductDeleteView, ProductListView, VersionCreateView)


app_name = CatalogConfig.name

urlpatterns = [
    path('', display_home_page, name='display_home_page'),

    path('contacts/', display_contact_info, name='display_contact_info'),

    path('product_list', ProductListView.as_view(), name='product_list'),
    path('product_create/create', ProductCreateView.as_view(), name='product_create'),
    path('product_detail/<int:pk>/update', ProductUpdateView.as_view(), name='product_update'),
    path('product_detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('product_delete/<int:pk>', ProductDeleteView.as_view(), name='product_delete'),

    path('blog_create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog_list/', BlogListView.as_view(), name='blog_list'),
    path('blog_detail/<int:pk>', BlogDetailView.as_view(), name='blog_detail'),
    path('blog_update/<int:pk>', BlogUpdateView.as_view(), name='blog_update'),
    path('blog_delete/<int:pk>', BlogDeleteView.as_view(), name='blog_delete'),

    path('version_create/<int:pk>/create', VersionCreateView.as_view(), name='version_create'),
    ]
