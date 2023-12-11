# myapp/urls.py

from django.urls import path
from .views import  process_request_view

urlpatterns = [
    path('process/', process_request_view, name='process_request'),
    #path('get_processed_images/', get_processed_images, name='get_processed_images'),
]
