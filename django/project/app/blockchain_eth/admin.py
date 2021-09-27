from django.contrib import admin

from app.blockchain_eth.models import Account, Block, Transaction

admin.site.register(Account)


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ["number", "transactions_updated"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["block", "type"]
