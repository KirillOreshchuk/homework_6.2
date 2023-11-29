from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import display_home_page, display_contact_info
from . import views


app_name = CatalogConfig.name

urlpatterns = [
    path('', display_home_page, name='display_home_page'),
    path('catalog/', views.catalog, name='catalog'),
    path('contacts/', display_contact_info, name='display_contact_info'),
    path('product/<int:category_id>', views.product, name='product'),
]
