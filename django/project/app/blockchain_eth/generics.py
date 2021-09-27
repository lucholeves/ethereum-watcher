from rest_framework import generics


class TransactionGenericListAPIView(generics.ListAPIView):
    filterset_fields = ["block__number"]


class TransactionHistoryByAddressGeneric(generics.ListAPIView):
    lookup_url_kwarg = "address"
    filterset_fields = ["block__number"]

    def get_queryset(self):
        queryset = super().get_queryset()
        address = self.kwargs.get(self.lookup_url_kwarg)
        queryset = queryset.filter(data__to=address) | self.queryset.filter(
            data__from=address
        )
        return queryset
