from django.urls import path
from .views import preprocess_crypto_data

urlpatterns = [
    path("", preprocess_crypto_data, name="preprocess_crypto_data"),
]