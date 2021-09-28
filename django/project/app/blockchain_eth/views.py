from rest_framework import generics

from .generics import TransactionGenericViewset
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


class TransactionInternalViewset(TransactionGenericViewset):
    """
    NOTE: internal transactions aren't transactions per se
    We need to change the approach
    """

    queryset = Transaction.objects.internals()
    serializer_class = TransactionInternalModelSerializer


class TransactionNormalViewset(TransactionGenericViewset):
    """ """

    queryset = Transaction.objects.normals()
    serializer_class = TransactionNormalModelSerializer
