from django.contrib import admin

from project.app.blockchain_eth.models import Account, Transaction, Block

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Block)