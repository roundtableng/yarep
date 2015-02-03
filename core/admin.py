from django.contrib import admin

from core.models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'lga')


admin.site.register(Account, AccountAdmin)
