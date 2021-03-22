from django.db import models
from django.db.models import F
from django.contrib.auth import get_user_model

User = get_user_model()

class TransactionQuerySet(models.query.QuerySet): 
    
    def delete(self, *args, **kwargs):
        """ Balance adjustment in case of multiple deletion of transactions """

        wallets_for_update = []
        aggregated_transactions = {}
        transactions = self.values('wallet', 'amount')
        for transaction in transactions:
            aggregated_transactions[transaction['wallet']] = aggregated_transactions.get(transaction['wallet'], 0) + transaction['amount']
         
        wallets = Wallet.objects.filter(pk__in = aggregated_transactions)
        for wallet in wallets:
            wallet.balance = F('balance') - aggregated_transactions[wallet.pk]
            wallets_for_update.append(wallet)

        Wallet.objects.bulk_update(wallets_for_update, ['balance'])  
        super().delete(*args, **kwargs)

class TransactionManager(models.Manager):
    def get_queryset(self):       
        return TransactionQuerySet(self.model, using=self._db)    

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')
    name = models.CharField(max_length=250)
    balance = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.name}. Owner: {self.user.username}'   

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=250)

    objects = TransactionManager()

    def __str__(self):
        return f'Transaction: {self.comment[:20]}'    

    def adjust_balance(self, save=True):
        wallet = self.wallet 
        if save == False:
            self.amount = -self.amount
        wallet.balance = F('balance') + self.amount 
        wallet.save()

    def save(self, *args, **kwargs):
        """ Balance adjustment when save a transaction """

        super().save(*args, **kwargs)
        self.adjust_balance()
    
    def delete(self, *args, **kwargs):
        """ Balance adjustment when deleting a transaction """

        self.adjust_balance(save = False)
        super().delete(*args, **kwargs)
