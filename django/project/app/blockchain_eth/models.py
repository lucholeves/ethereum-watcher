from django.db import models

ON_DELETE_CASCADE = models.CASCADE


class Account(models.Model):
    data = models.JSONField(default=dict)


class Block(models.Model):
    number = models.IntegerField(unique=True)
    data = models.JSONField(default=dict)
    transactions_updated = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.number = int(self.data["blockNumber"])
        super().save(*args, **kwargs)

    @property
    def address(self):
        return self.data["blockMiner"]

    @property
    def number_hex(self):
        return hex(self.number)


class TransactionManager(models.Manager):
    def internals(self):
        return self.filter(type=Transaction.INTERNAL)

    def normals(self):
        return self.filter(type=Transaction.NORMAL)

    def by_address(self, address: str):
        return self.filter(data__from=address)


class Transaction(models.Model):
    UNKNOWN = "unknown"
    NORMAL = "normal"
    INTERNAL = "internal"

    TYPES = ((UNKNOWN, UNKNOWN), (NORMAL, NORMAL), (INTERNAL, INTERNAL))

    block = models.ForeignKey(
        Block, on_delete=ON_DELETE_CASCADE, related_name="transactions"
    )
    type = models.CharField(max_length=20, choices=TYPES, default=UNKNOWN)
    data = models.JSONField(default=dict)
    objects = TransactionManager()
