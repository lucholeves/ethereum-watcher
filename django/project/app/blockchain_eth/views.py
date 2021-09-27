from rest_framework import generics

from .generics import TransactionGenericListAPIView, TransactionHistoryByAddressGeneric
from .models import Block, Transaction
from .serializers import (
    BlockModelSerializer,
    TransactionInternalModelSerializer,
    TransactionNormalModelSerializer,
)

# ---------------------------------------------------------------------
# Class based views
# ---------------------------------------------------------------------


class BlockListAPIView(generics.ListAPIView):
    queryset = Block.objects.all().order_by("-id")
    serializer_class = BlockModelSerializer
    filterset_fields = ["number", "transactions_updated"]


class TransactionInternalListAPIView(TransactionGenericListAPIView):
    """ """

    queryset = Transaction.objects.internals()
    serializer_class = TransactionInternalModelSerializer


class TransactionNormalListAPIView(TransactionGenericListAPIView):
    """ """

    queryset = Transaction.objects.normals()
    serializer_class = TransactionNormalModelSerializer


class TransactionNormalHistoryByAddress(TransactionHistoryByAddressGeneric):
    """ """

    queryset = Transaction.objects.normals()
    serializer_class = TransactionNormalModelSerializer


class TransactionInternalHistoryByAddress(TransactionHistoryByAddressGeneric):
    """ """

    queryset = Transaction.objects.internals()
    serializer_class = TransactionInternalModelSerializer
