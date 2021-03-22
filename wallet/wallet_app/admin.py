from django.contrib import admin
from .models import Wallet, Transaction

class WalletAdmin(admin.ModelAdmin):
    list_display = ['name', 'user','balance']
    list_filter = ['user']
    list_display_links = ['name',]
    list_editable = ['user', 'balance' ]

admin.site.register(Wallet, WalletAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'wallet', 'amount','date', 'comment']
    list_filter = ['wallet']
    list_display_links = ['id',]
    list_editable = ['amount', 'wallet' ]

admin.site.register(Transaction, TransactionAdmin)


