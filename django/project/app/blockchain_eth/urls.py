from django.urls import include, path

from rest_framework import routers

from .views import BlockViewset, TransactionViewset

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register(r"blocks", BlockViewset)
router.register(r"transactions", TransactionViewset)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [path("", include(router.urls))]
