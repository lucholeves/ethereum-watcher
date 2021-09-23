from django.contrib import admin

from app.blockchain_eth.models import Account, Block, Transaction

admin.site.register(Account)
admin.site.register(Transaction)


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ["number", "transactions_updated"]
