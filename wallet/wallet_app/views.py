from wallet_app.models import Transaction, Wallet, User
from .serializers import WalletSerializer, UserSerializer, TransactionSerialize
from rest_framework import viewsets
from rest_framework import mixins

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerialize

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return Transaction.objects.none()
        return Transaction.objects.filter(wallet_id = self.kwargs['wallet_pk'])

class WalletViewSet(viewsets.ModelViewSet):
    serializer_class = WalletSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return Wallet.objects.none()
        return Wallet.objects.filter(user_id = self.kwargs['user_pk'])

class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
