# -*- coding: utf-8 -*-

from django.contrib import admin
from disa_app.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = [ 'id', 'user', 'old_db_id' ]


admin.site.register( UserProfile, UserProfileAdmin )
