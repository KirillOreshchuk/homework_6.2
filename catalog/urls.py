from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (display_home_page, display_contact_info, CategoryListView,
                           ProductDetailView, BlogCreateView,
                           BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView)
from . import views


app_name = CatalogConfig.name

urlpatterns = [
    path('', display_home_page, name='display_home_page'),
    path('catalog/', CategoryListView.as_view(), name='catalog'),
    path('contacts/', display_contact_info, name='display_contact_info'),
    path('product/<int:category_id>', views.product, name='product'),
    path('one_product/<int:pk>', ProductDetailView.as_view(), name='one_product'),

    path('blog_create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog_list/', BlogListView.as_view(), name='blog_list'),
    path('blog_detail/<int:pk>', BlogDetailView.as_view(), name='blog_detail'),
    path('blog_update/<int:pk>', BlogUpdateView.as_view(), name='blog_update'),
    path('blog_delete/<int:pk>', BlogDeleteView.as_view(), name='blog_delete'),
]
