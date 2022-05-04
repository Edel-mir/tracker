from django.contrib import admin

from .models import Profile, Tag, Expense


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'income', 'outcome')
    list_display = ('user', 'income', 'outcome')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ('user', 'name')
    list_display = ('user', 'name')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    fields = ('user', 'type', 'amount', 'tag', 'date', 'description')
    list_display = ('user', 'type', 'tag', 'description')
    list_filter = ('tag', 'type')
    search_fields = ('user', 'description')
