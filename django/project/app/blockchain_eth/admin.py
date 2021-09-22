from django.contrib import admin

from app.blockchain_eth.models import Account, Block, Transaction

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Block)
