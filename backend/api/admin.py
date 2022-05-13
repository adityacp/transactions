# Python Imports
from django.contrib import admin

# Local Imports
from .models import Account, Transaction


admin.site.register(Account)
admin.site.register(Transaction)
