from rest_framework import serializers
from .models import Wallet, Transaction, User
from rest_framework.reverse import reverse

class TransactionHyperlink(serializers.HyperlinkedIdentityField):   
    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'user_pk': obj.wallet.user_id,
            'wallet_pk':obj.wallet_id,
            'pk': obj.pk
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

class TransactionSerialize(serializers.ModelSerializer):
    url = TransactionHyperlink(view_name = 'wallet_app:transaction-detail')
    class Meta:
        model = Transaction
        fields = ['url', 'wallet', 'amount', 'date', 'comment']
        extra_kwargs = {
               'wallet':{'read_only':True},  
            } 

    def save(self, **kwargs):
        kwargs.update({'wallet_id':self.context['view'].kwargs['wallet_pk']})
        super().save(**kwargs)

class WalletHyperlink(serializers.HyperlinkedIdentityField):   
    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'user_pk': obj.user_id,
            'pk': obj.pk
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

class WalletSerializer(serializers.ModelSerializer):
    url = WalletHyperlink(view_name = 'wallet_app:wallet-detail')
    transactions = TransactionHyperlink(view_name='wallet_app:transaction-detail', many=True, read_only=True)
    class Meta:
        model = Wallet
        fields = ['url', 'name', 'user', 'balance', 'transactions']
        extra_kwargs = {
            'balance': {'read_only':True},  
            'user':{'read_only':True},  
        } 
    
    def save(self, **kwargs):
        kwargs.update({'user_id':self.context['view'].kwargs['user_pk']})
        super().save(**kwargs)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    wallets = WalletSerializer(many=True)
    class Meta:
        model = User
        fields = ['url', 'username', 'wallets']
        extra_kwargs = {
            'url': {'view_name': 'wallet_app:user-detail', 'lookup_field': 'pk'},
        }
