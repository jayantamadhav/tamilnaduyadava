from django.contrib import admin
from nested_admin import NestedStackedInline, NestedModelAdmin
from django.contrib.auth.admin import UserAdmin
from account.models import Account, Profile, ProfileImage
import datetime
# Register your models here.

class AccountAdmin(UserAdmin):
	list_display = ('email', 'username', 'date_joined', 'last_login', 'is_staff', 'payment_status', 'custom_group', 'created_by')
	search_fields = ('email', 'username')
	readonly_fields = ('date_joined', 'last_login', 'created_by', 'payment_status',)

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()	
		
	def custom_group(self, obj):
		return ','.join([g.name for g in obj.groups.all()])
	def save_model(self, request, obj, form, change):
		if obj.created_by == None:
			if request.user.is_staff and not request.user.is_superuser:
				obj.created_by = 'Support'
			else:
				obj.created_by = 'Admin'
		if obj.age == None and obj.dob is not None:
			now = datetime.datetime.now()
			obj.age = now.year - int(obj.dob[-4:])
		super().save_model(request, obj, form, change)


class ProfileImageInline(NestedStackedInline):
	model = ProfileImage
	extra = 1
	fk_name = 'profile'

class ProfileAdmin(admin.ModelAdmin):
	search_fields = ['user']
	readonly_fields = ['caste',]
	autocomplete_fields = ['user']
	inlines = [ProfileImageInline]


admin.site.register(Account, AccountAdmin)
admin.site.register(Profile, ProfileAdmin)