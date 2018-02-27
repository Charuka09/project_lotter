# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Leader,  Project, ProjectDraw

from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class EmailRequiredMixin(object):
    def __init__(self, *args, **kwargs):
        super(EmailRequiredMixin, self).__init__(*args, **kwargs)
        # make user email field required
        self.fields['email'].required = True


class MyUserCreationForm(EmailRequiredMixin, UserCreationForm):
    pass


class MyUserChangeForm(EmailRequiredMixin, UserChangeForm):
    pass


class LeaderInline(admin.StackedInline):
    model = Leader
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (LeaderInline, )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    add_fieldsets = ((None, {'fields': ('username', 'email',
                                        'password1', 'password2'), 'classes': ('wide',)}),)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Project)
admin.site.register(ProjectDraw)
