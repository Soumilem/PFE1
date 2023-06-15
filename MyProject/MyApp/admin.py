from django.contrib import admin
from .models import Client, Banque, Offers, DemandePret, User,client_nni, client_banque
# Register your models here.

admin.site.register(Client)
admin.site.register(Banque)
admin.site.register(Offers)
admin.site.register(DemandePret)
admin.site.register(User)
admin.site.register(client_nni)
admin.site.register(client_banque)
