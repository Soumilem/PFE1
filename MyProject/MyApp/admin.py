from django.contrib import admin
from .models import User, Client, AdminBanque,Banque
# Register your models here.

class UserAdminConfig(admin.ModelAdmin):
    model = User
    search_fields = ('nom', 'phone',)
    list_filter = ('nom', 'phone', 'is_active', 'is_staff')
    ordering = ('nom',)  # Update the ordering field here
    list_display = ('phone','nom', 'is_superuser',
                    'is_active', 'is_staff', 'is_blocked', 'password',)
    fieldsets = (
        (None, {'fields': ('nom', 'phone','role',)}),
        ('Permissions', {'fields': ('is_staff','is_active', 'is_blocked')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nom', 'phone','is_active', 'is_staff', 'is_blocked')
            }
         ),
    )


class AdminConfig(admin.ModelAdmin):
    model = AdminBanque
    search_fields = ('nom', 'phone',)
    list_filter = ('nom', 'phone', 'is_active', 'is_staff')
    ordering = ('nom',)  # Update the ordering field here
    list_display = ('phone','nom', 'is_superuser',
                    'is_active', 'is_staff', 'is_blocked', 'password',)
    fieldsets = (
        (None, {'fields': ('nom', 'phone','role',)}),
        ('Permissions', {'fields': ('is_staff','is_active', 'is_blocked')}),
         ('Banque', {'fields': ('banque',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nom', 'phone', 'banque','is_active', 'is_staff', 'is_blocked')
            }
         ),
    )




admin.site.register(AdminBanque, AdminConfig)       

admin.site.register(Client, UserAdminConfig)    

admin.site.register(User, UserAdminConfig)


# admin.site.register(Client)
admin.site.register(Banque)
# admin.site.register(Offers)
# admin.site.register(DemandePret)
# admin.site.register(User)
# admin.site.register(CLientNNI)
# admin.site.register(ClientBanque)
# admin.site.register(AdminBanque)
