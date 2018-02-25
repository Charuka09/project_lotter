# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import Project, LotteryDraw
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Leader, LotteryDraw, Project


class LeaderInline(admin.StackedInline):
    model = Leader
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (LeaderInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Project)
admin.site.register(LotteryDraw)