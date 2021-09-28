from django.db import models


class TransactionManager(models.Manager):
    def internals(self):
        from .models import Transaction

        return self.filter(type=Transaction.INTERNAL)

    def normals(self):
        from .models import Transaction

        return self.filter(type=Transaction.NORMAL)

    def by_address(self, address: str):
        return self.filter(data__from=address)
