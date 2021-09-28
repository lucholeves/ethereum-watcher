from django.db import models

from .managers import TransactionManager

ON_DELETE_CASCADE = models.CASCADE


class Account(models.Model):
    data = models.JSONField(default=dict)


class Block(models.Model):
    number = models.IntegerField(unique=True)
    data = models.JSONField(default=dict)
    transactions_updated = models.BooleanField(default=False)

    def __str__(self):
        return f"Number: {self.number}"

    def save(self, *args, **kwargs):
        self.number = int(self.data["blockNumber"])
        super().save(*args, **kwargs)

    @property
    def address(self):
        return self.data["blockMiner"]

    @property
    def number_hex(self):
        return hex(self.number)


class Transaction(models.Model):
    # NOTE: internal transactions aren't transactions per se
    # We need to change the approach
    UNKNOWN = "unknown"
    NORMAL = "normal"
    INTERNAL = "internal"

    TYPES = ((UNKNOWN, UNKNOWN), (NORMAL, NORMAL), (INTERNAL, INTERNAL))

    block = models.ForeignKey(
        Block, on_delete=ON_DELETE_CASCADE, related_name="transactions"
    )
    hash = models.CharField(max_length=500, unique=True, default="")
    type = models.CharField(max_length=20, choices=TYPES, default=UNKNOWN)
    data = models.JSONField(default=dict)
    objects = TransactionManager()

    def __str__(self):
        return f"{self.hash} - {self.type}"

    def save(self, *args, **kwargs):
        self.hash = self.data["hash"]
        super().save(*args, **kwargs)
