from django.urls import path

from catalog.views import display_home_page, display_contact_info

urlpatterns = [
    path('', display_home_page, name='display_home_page'),
    path('contacts/', display_contact_info, name='display_contact_info')
]
