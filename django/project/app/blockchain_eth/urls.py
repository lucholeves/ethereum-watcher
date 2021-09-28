from django.urls import include, path

from rest_framework import routers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .views import BlockViewset, TransactionNormalViewset  # TransactionInternalViewset,


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "blocks": reverse("blocks-root", request=request, format=format),
            "transactions": reverse("transaction-root", request=request, format=format),
        }
    )


router_blocks = routers.DefaultRouter()
router_blocks.root_view_name = "blocks-root"
router_blocks.register(r"", BlockViewset)

router_transactions = routers.DefaultRouter()
router_transactions.root_view_name = "transaction-root"
router_transactions.register(
    r"normal", TransactionNormalViewset, basename="transaction-normal"
)
# NOTE: internal transactions aren't transactions per se. We need to change the approach :(
# router_transactions.register(r'internal', TransactionInternalViewset, basename="transaction-internal")


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", api_root, name="api-root"),
    # -- Blocks
    path("blocks/", include(router_blocks.urls)),
    # -- Transactions
    path("transactions/", include(router_transactions.urls)),
]
