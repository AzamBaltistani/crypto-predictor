from django.urls import path
from .views import fetch_crypto_data

urlpatterns = [
    path("", fetch_crypto_data, name="fetch_crypto_data"),
]