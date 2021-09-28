from rest_framework import viewsets
from rest_framework.decorators import action


class TransactionGenericViewset(viewsets.ReadOnlyModelViewSet):
    lookup_field = "hash"
    filterset_fields = ["block__number"]

    @action(
        methods=["get"],
        detail=False,
        url_path="address-history/(?P<address>[^/.]+)",
        url_name="address_history",
    )
    def address_history(self, request, address):
        queryset = super().get_queryset()
        queryset = queryset.filter(data__to=address) | self.queryset.filter(
            data__from=address
        )
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
