from django.contrib import admin
from .models import Accounts, UserEmailConfirmationNumber
# Register your models here.
admin.site.register(Accounts)
admin.site.register(UserEmailConfirmationNumber)
