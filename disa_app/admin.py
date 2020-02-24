# -*- coding: utf-8 -*-

from django.contrib import admin
from disa_app.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = [ 'id', 'user', 'uu_id', 'old_db_id' ]
    readonly_fields = [ 'uu_id' ]
    search_fields = [ 'uu_id', 'old_db_id' ]


admin.site.register( UserProfile, UserProfileAdmin )
