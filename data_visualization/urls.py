from django.urls import path
from .views import visualize_crypto_data

urlpatterns = [
    path("", visualize_crypto_data, name="visualize_crypto_data"),
]
