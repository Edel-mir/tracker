from django.contrib import admin

from .models import Profile, Tag, Expense


admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Expense)
