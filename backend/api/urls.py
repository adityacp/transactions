from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views


urlpatterns = [
    path('login', views.login, name="login"),
    path('accounts', views.get_accounts, name="get_accounts"),
    path('add_transaction', views.add_transaction, name="add_transaction"),
    path('get_transactions', views.get_transactions, name="get_transactions"),
    path('mark_paid', views.mark_paid, name="mark_paid"),
    # path('mark_paid', views.mark_paid, name="get_user_accounts"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
