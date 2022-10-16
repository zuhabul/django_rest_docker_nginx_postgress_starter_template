from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models
from django.utils.translation import gettext as _


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name', 'created_at', 'updated_at']
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'name')
    fieldsets = (
        (None, {"fields": ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',
                                         'profile_photo_url',
                                         'cover_photo_url',
                                         'phone_number',
                                         'organized_events_list',
                                         'fav_vendors',)}),
        (_('Permissions'), {
         'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None,
          {'classes': ('wide',),
          'fields': ('email', 'password1', 'password2',),
          }
         ),
    )

admin.site.site_header = "Backend Admin"
admin.site.register(models.User, UserAdmin)
admin.site.register(models.VendorCategory)
admin.site.register(models.Review)
admin.site.register(models.EventType)
admin.site.register(models.Offer)
admin.site.register(models.Vendor)
admin.site.register(models.Event)
admin.site.register(models.VendorPhoto)
admin.site.register(models.EventPhoto)
