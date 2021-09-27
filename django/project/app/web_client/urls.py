from django.urls import path

from .view import address_history, block_details, index

urlpatterns = [
    path("", index),
    path("block/<int:block_number>", block_details),
    path("address/<str:address>", address_history),
]
