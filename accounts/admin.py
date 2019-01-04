from django.contrib import admin
from accounts.models import User, Trainer, PreSetAuthorizedUser, Client

admin.site.register(Client)
admin.site.register(User)
admin.site.register(Trainer)
admin.site.register(PreSetAuthorizedUser)
