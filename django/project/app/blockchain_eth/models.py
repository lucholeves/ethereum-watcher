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


class Transaction(models.Model):
    block = models.ForeignKey(
        Block, on_delete=ON_DELETE_CASCADE, related_name="transactions"
    )
    data = models.JSONField(default=dict)
