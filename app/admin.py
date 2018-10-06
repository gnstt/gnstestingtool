from django.contrib import admin
from app.models import *
from django.contrib.auth.models import User


# Register your models here.

class StackedActions(admin.StackedInline):
	model = Actions

class CheckListsAdmin(admin.ModelAdmin):
	inlines = (StackedActions,)
	model = CheckLists
	readonly_fields=('author',)

	def save_model(self, request, obj, form, change):
		if getattr(obj, 'author', None) is None:
			obj.author = request.user
		obj.save()

admin.site.register(CheckLists,CheckListsAdmin)
