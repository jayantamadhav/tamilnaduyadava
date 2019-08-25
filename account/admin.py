from django.contrib import admin
from nested_admin import NestedStackedInline, NestedModelAdmin
from django.contrib.auth.admin import UserAdmin
from account.models import Account, Profile, ProfileImage
from account.forms import RegistrationForm
import datetime
# Register your models here.

class AccountAdmin(UserAdmin):
	list_display = ('m_id', 'email', 'username', 'gender', 'date_joined', 'last_login', 'is_staff', 'payment_status', 'custom_group', 'created_by', 'is_active', 'reason')
	search_fields = ('email', 'username', 'gender', 'm_id',)
	readonly_fields = ('date_joined', 'last_login', 'created_by', 'payment_status', 'm_id')
	
	add_form = RegistrationForm
	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()
	add_fieldsets = (
		(None, {'classes': ('wide',),
		'fields': ('email', 'username', 'password1', 'password2', 'name', 'age', 'dob', 'gender', 'phone', 'captcha', 'is_active', 'is_admin', 'is_staff', 'is_superuser' ),
		}),
	)

	def custom_group(self, obj):
		return ','.join([g.name for g in obj.groups.all()])
	def save_model(self, request, obj, form, change):
		if obj.created_by == None:
			if request.user.is_staff and not request.user.is_superuser:
				obj.created_by = 'Support'
			else:
				obj.created_by = 'Admin'
		if obj.age == None and obj.dob is not None:
			get_age = str(obj.dob)
			get_age = get_age[:4]
			now = datetime.datetime.now()
			obj.age = now.year - int(get_age)
		if obj.m_id == None:
			now = datetime.datetime.now()
			random_id = "{:05d}".format(request.user.id)
			matrimony_id = 'TNY' + now.strftime('%y%m%d') + random_id
			obj.m_id = matrimony_id
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