from django.db import models

ON_DELETE_CASCADE = models.CASCADE


class Account(models.Model):
    data = models.JSONField(default=dict)


class Block(models.Model):
    data = models.JSONField(default=dict)

    @property
    def number(self) -> int:
        return int(self.data["blockNumber"])


class Transaction(models.Model):
    block = models.ForeignKey(
        Block, on_delete=ON_DELETE_CASCADE, related_name="transactions"
    )
    data = models.JSONField(default=dict)
