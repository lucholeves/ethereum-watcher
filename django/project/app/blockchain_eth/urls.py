from django.urls import path

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .views import (
    BlockListAPIView,
    TransactionInternalHistoryByAddress,
    TransactionInternalListAPIView,
    TransactionNormalHistoryByAddress,
    TransactionNormalListAPIView,
)


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "blocks": reverse("blocks-list", request=request, format=format),
            "transactions-normal": reverse(
                "transactions-normal-list", request=request, format=format
            ),
            "transactions-internal": reverse(
                "transactions-internal-list", request=request, format=format
            ),
        }
    )


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", api_root),
    # -- Blocks
    path("blocks/", BlockListAPIView.as_view(), name="blocks-list"),
    # -- Transactions
    # -------- Normals
    path(
        "transactions/normal/",
        TransactionNormalListAPIView.as_view(),
        name="transactions-normal-list",
    ),
    path(
        "transactions/normal/address-history/<str:address>/",
        TransactionNormalHistoryByAddress.as_view(),
        name="transactions-normal-address-history-list",
    ),
    # -------- Internals
    path(
        "transactions/internal/",
        TransactionInternalListAPIView.as_view(),
        name="transactions-internal-list",
    ),
    path(
        "transactions/internal/address-history/<str:address>",
        TransactionInternalHistoryByAddress.as_view(),
        name="transactions-internal-address-history-list",
    ),
]
