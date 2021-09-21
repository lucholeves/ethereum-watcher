from rest_framework import viewsets

from .models import Block, Transaction
from .serializers import BlockModelSerializer, TransactionModelSerializer


class BlockViewset(viewsets.ModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockModelSerializer


class TransactionViewset(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionModelSerializer
