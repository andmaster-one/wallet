from rest_framework_nested import routers
from .views import UserViewSet, WalletViewSet, TransactionViewSet

app_name = 'wallet_app'

router = routers.SimpleRouter()
router.register(r'users', UserViewSet, basename='user')

wallet_router =  routers.NestedSimpleRouter(router, r'users', lookup='user')
wallet_router.register(r'wallets', WalletViewSet, basename='wallet')

transaction_router =  routers.NestedSimpleRouter(wallet_router, r'wallets', lookup='wallet')
transaction_router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = router.urls
urlpatterns += wallet_router.urls
urlpatterns += transaction_router.urls