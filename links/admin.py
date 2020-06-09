from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Link, Vote, Profile


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    pass


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    pass


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class ProfileAdmin(UserAdmin):
    inlines = [ProfileInline]


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), ProfileAdmin)
