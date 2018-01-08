from django.contrib import admin
from . import models


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'api_key', 'credits')


@admin.register(models.Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'zone', 'title', 'plan', 'state')
