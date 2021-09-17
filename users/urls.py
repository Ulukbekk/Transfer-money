from django.urls import path
from .views import AccountRegisterAPIView, AccountDetailAPIView, TransactionAPIView, BalanceIncreaseAPIView

urlpatterns = [
    path('transaction/<int:pk>/', TransactionAPIView.as_view(), name='transaction'),
    path('balance/top-up/', BalanceIncreaseAPIView.as_view(), name='add_balance'),
    path('register/', AccountRegisterAPIView.as_view(), name='register'),
    path('<int:pk>/', AccountDetailAPIView.as_view(), name='detail'),
]
