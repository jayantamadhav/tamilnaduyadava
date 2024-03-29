from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from account.models import Profile, ProfileImage, Account, Preference
from account.forms import ProfileCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import json
# Create your views here.

#View for ABout Us page
def about_us(request):
	context = {}
	profile = Profile.objects.get(user=request.user)
	try:
		profile_image = ProfileImage.objects.get(profile=profile)
	except ProfileImage.DoesNotExist:
		profile_image = ''
	context = {
		'profile_image' : profile_image,
	}
	return render(request, 'mainApp/about_us.html', context)

#View for Privacy Policy page
def privacy_policy(request):
	context = {}
	profile = Profile.objects.get(user=request.user)
	profile_image = ProfileImage.objects.get(profile=profile)
	context = {
		'profile_image' : profile_image,
	}
	return render(request, 'mainApp/privacy_policy.html', context)

def privacy_policy_external(request):
	return render(request, 'mainApp/privacy_policy_external.html', {})

def home(request):
	system_messages = messages.get_messages(request)
	for message in system_messages:
		pass
	system_messages.used = True
	user = request.user
	if request.user.is_superuser:
		return redirect('admin/')
	if request.user.is_authenticated:
		if Profile.objects.filter(user=request.user).count():
			return redirect('feed')
		else:
			return redirect('createProfile')
	else:
		if request.POST:
			userinput = request.POST['email']
			email = ''
			password = request.POST['password']
			try:
				email = Account.objects.get(username=userinput).email.lower()
			except Account.DoesNotExist:
				email = request.POST['email'].lower()
			user = authenticate(email = email, password = password)
			if user:
				login(request, user)
				if Profile.objects.filter(user=request.user).count():
					return redirect('feed')
				else:
					return redirect('createProfile')
			else:
				messages.error(request, 'User does not exist, please register now')		

	return render(request, 'mainApp/home.html', {})

def feed(request):
	context = {}
	profile = Profile.objects.get(user=request.user)
	try:
		preference = Preference.objects.get(profile=profile)
	except Preference.DoesNotExist:
		preference = ''
	try:
		profile_image = ProfileImage.objects.get(profile=profile)
	except ProfileImage.DoesNotExist:
		profile_image = ''
	if preference:
		min_age = preference.age[:2]
		max_age = preference.age[3:]
		min_height = preference.height[:3]
		max_height = preference.height[4:]
		salary = preference.salary
		if salary == '<5 LPA':
			min_salary = 0
			max_salary = 5
		elif salary == '5-10 LPA':
			min_salary = 5
			max_salary = 1
		elif salary == '10-15 LPA':
			min_salary = 10
			max_salary = 15
		else:
			min_salary = 15
			max_salary = 1000000
		education = preference.education.split(',')[1:]
		complexion = preference.complexion.split(',')[1:]
		print(education, complexion)
		married = preference.married
		if profile.user.gender == 'M':
			get_profiles = Profile.objects.filter(
				user__gender = 'F',
				user__is_active=True,
				user__age__range = (min_age, max_age),
				height__range = (min_height, max_height),
				salary__range = (min_salary, max_salary),
				education__in = education,
				complexion__in = complexion,
				marital_status = married,
			)
			latest_profiles = Profile.objects.filter(user__gender = 'F', user__is_active=True).order_by('-user__date_joined')[:3]
		else:
			get_profiles = Profile.objects.filter(
				user__gender = 'M', 
				user__is_active=True,
				user__age__range = (min_age, max_age),
				height__range = (min_height, max_height),
				salary__range = (min_salary, max_salary),
				education__in = education,
				complexion__in = complexion,
				marital_status = married,
			)
			latest_profiles = Profile.objects.filter(user__gender = 'M', user__is_active=True).order_by('-user__date_joined')[:3]
	else:
		if profile.user.gender == 'M':
			get_profiles = Profile.objects.filter(user__gender = 'F', user__is_active=True)
			latest_profiles = Profile.objects.filter(user__gender = 'F', user__is_active=True).order_by('-user__date_joined')[:3]
		else:
			get_profiles = Profile.objects.filter(user__gender = 'M', user__is_active=True)
			latest_profiles = Profile.objects.filter(user__gender = 'M', user__is_active=True).order_by('-user__date_joined')[:3]
		education = ''
		complexion = ''
	page = request.GET.get('page', 1)
	paginator = Paginator(get_profiles, 10)
	try:
		show_profiles = paginator.page(page)
	except PageNotAnInteger:
		show_profiles = paginator.page(1)
	except EmptyPage:
		show_profiles = paginator.page(paginator.num_pages)
	
	context = {
		'profile' : profile,
		'profile_image' : profile_image,
		'show_profiles' : show_profiles,
		'latest_profiles' : latest_profiles,
		'preference'	: preference,
		'education'		: education,
		'complexion'	: complexion
	}

	print(context)
	return render(request, 'mainApp/feed.html', context )

def sort_by(request, key, value):
	context = {}
	profile = Profile.objects.get(user=request.user)
	try:
		preference = Preference.objects.get(profile=profile)
	except Preference.DoesNotExist:
		preference = ''
	try:
		profile_image = ProfileImage.objects.get(profile=profile)
	except ProfileImage.DoesNotExist:
		profile_image = ''
	if preference:
		min_age = preference.age[:2]
		max_age = preference.age[3:]
		min_height = preference.height[:3]
		max_height = preference.height[4:]
		salary = preference.salary
		if salary == 'Below 5 LPA':
			min_salary = 0
			max_salary = 5
		elif salary == '5-10 LPA':
			min_salary = 5
			max_salary = 10
		elif salary == '10-15 LPA':
			min_salary = 10
			max_salary = 15
		else:
			min_salary = 15
			max_salary = 200000000
		education = preference.education.split(',')[1:]
		complexion = preference.complexion.split(',')[1:]
		married = preference.married
		if profile.user.gender == 'M' :
			if key == 'rasi':
				get_profiles = Profile.objects.filter(
					user__gender = 'F', 
					rasi = value, 
					user__is_active=True,
					user__age__range = (min_age, max_age),
					height__range = (min_height, max_height),
					salary__range = (min_salary, max_salary),
					education__in = education,
					complexion__in = complexion,
					marital_status = married,
				)
			else:
				get_profiles = Profile.objects.filter(
					user__gender = 'F', 
					nakshatra = value, 
					user__is_active=True,
					user__age__range = (min_age, max_age),
					height__range = (min_height, max_height),
					salary__range = (min_salary, max_salary),
					education__in = education,
					complexion__in = complexion,
					marital_status = married,
				)
			latest_profiles = Profile.objects.filter(user__gender = 'F', user__is_active=True).order_by('-user__date_joined')[:3]
		else:
			if key == 'rasi':
				get_profiles = Profile.objects.filter(
					user__gender = 'M', 
					rasi = value,
					user__is_active=True,
					user__age__range = (min_age, max_age),
					height__range = (min_height, max_height),
					salary__range = (min_salary, max_salary),
					education__in = education,
					complexion__in = complexion,
					marital_status = married,
				)
			else:
				get_profiles = Profile.objects.filter(
					user__gender = 'M', 
					nakshatra = value, 
					user__is_active=True,
					user__age__range = (min_age, max_age),
					height__range = (min_height, max_height),
					salary__range = (min_salary, max_salary),
					education__in = education,
					complexion__in = complexion,
					marital_status = married,
				)
			latest_profiles = Profile.objects.filter(user__gender = 'M', user__is_active=True).order_by('-user__date_joined')[:3]
	else:
		if profile.user.gender == 'M' :
			if key == 'rasi':
				get_profiles = Profile.objects.filter(user__gender = 'F', rasi = value, user__is_active=True)
			else:
				get_profiles = Profile.objects.filter(user__gender = 'F', nakshatra = value, user__is_active=True)
			latest_profiles = Profile.objects.filter(user__gender = 'F', user__is_active=True).order_by('-user__date_joined')[:3]
		else:
			if key == 'rasi':
				get_profiles = Profile.objects.filter(user__gender = 'M', rasi = value)
			else:
				get_profiles = Profile.objects.filter(user__gender = 'M', nakshatra = value, user__is_active=True)
			latest_profiles = Profile.objects.filter(user__gender = 'M', user__is_active=True).order_by('-user__date_joined')[:3]
		complexion = ''
		education = ''
	page = request.GET.get('page', 1)
	paginator = Paginator(get_profiles, 10)
	try:
		show_profiles = paginator.page(page)
	except PageNotAnInteger:
		show_profiles = paginator.page(1)
	except EmptyPage:
		show_profiles = paginator.page(paginator.num_pages)
	context = {
		'profile' : profile,
		'profile_image' : profile_image,
		'show_profiles' : show_profiles,
		'latest_profiles' : latest_profiles,
		'preference' : preference,
		'education' : education,
		'complexion' : complexion
	}
	return render(request, 'mainApp/sort_by.html', context )

def manage_profile(request):
	context = {}
	if request.POST:
		user = Profile.objects.get(user__email = request.user)
		try:
			profile = ProfileImage.objects.get(profile = user)
			if bool(request.FILES.get('profile_image', False)) == True:
				profile.file = request.FILES['profile_image']
				profile.save()
		except ProfileImage.DoesNotExist:
			profile = ProfileImage.objects.create(profile=user, file=request.FILES['profile_image'])
			profile.save()
		if bool(request.FILES.get('horoscope', False)) == True:
			user.horoscope = request.FILES['horoscope']
			user.save()
		return redirect('manage_profile')
	
	profile = Profile.objects.get(user=request.user)
	try:
		profile_image = ProfileImage.objects.get(profile=profile)
	except ProfileImage.DoesNotExist:
		profile_image = ''
	context = {
		'profile' : profile,
		'profile_image' : profile_image,
	}
	return render(request, 'mainApp/manage_profile.html', context )


@csrf_exempt
def ajax_profile_update(request):
	account = ['name', 'dob', 'age',]
	response = ""
	if request.POST:
		data = request.POST
		if data['field'] in account:
			obj = Account.objects.get(email = request.user.email)
			setattr(obj, data['field'], data['new_data'])
			try:
				obj.save()
				print("done")
				response = 'success'
			except:
				response = 'error'
				return HttpResponse(response)
		else:
			obj = Profile.objects.get(user = request.user)
			setattr(obj, data['field'], data['new_data'])
			try:
				obj.save()
				print("done")
				response = 'success'
			except:
				response = 'error'
				return HttpResponseNotFound(response)

		return HttpResponse(response)
@csrf_exempt
def ajax_profile_pic_update(request):
	if request.POST:
		print("done bish")
		user = Profile.objects.get(user__email = request.user)
		profile = ProfileImage.objects.get(profile = user)
		profile.file = request.FILES['profile_image']
		profile.save()
		return redirect('manage_profile')#HttpResponse(response)
	return redirect('manage_profile')

def deactivate_user(request):
    if request.POST:
        email = request.POST['user']
        reason = request.POST['reason']
        user = Account.objects.get(email=email)
        user.is_active = False
        user.reason = reason
        user.save()
        return redirect('home')

def view_profile(request, id):
	view_profile = Profile.objects.get(user__id = id)
	try:
		view_profile_image = ProfileImage.objects.get(profile=view_profile)
	except ProfileImage.DoesNotExist:
		view_profile_image = ''
	try:
		profile_image = ProfileImage.objects.get(profile__user=request.user)
	except ProfileImage.DoesNotExist:
		profile_image = ''
	context = {
		'view_profile' : view_profile,
		'view_profile_image' : view_profile_image,
		'profile_image' : profile_image,

	}
	return render(request, 'mainApp/view_profile.html', context)

def change_password(request):
	system_messages = messages.get_messages(request)
	for message in system_messages:
		pass
	system_messages.used = True
	view_profile = Profile.objects.get(user=request.user)
	try:
		profile_image = ProfileImage.objects.get(profile=view_profile)
	except ProfileImage.DoesNotExist:
		profile_image = ''
	context = {}
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if request.POST['old_password'] == request.POST['new_password1']:
			messages.error(request, 'Old password and new password cannot be same', extra_tags="notification is-danger")
		elif form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Your password was successfully updated!', extra_tags="notification is-success")
			context = {
				'form' : form,
				'profile_image' : profile_image,
			}
			return render(request, 'mainApp/change_password.html', context)
		else:
			messages.error(request, 'Please correct the error below.', extra_tags="notification is-danger")
	else:
		form = PasswordChangeForm(request.user)
	context = {
		'form' : form,
		'profile_image' : profile_image,
	}
	return render(request, 'mainApp/change_password.html', context)

def update_preference(request):
	profile = Profile.objects.get(user = request.user)
	if request.POST:
		try:
			preference = Preference.objects.get(profile=profile)
			print(
				preference.age,
				preference.height,
				preference.salary,
				preference.education,
				preference.complexion,
				preference.married
			)
		except Preference.DoesNotExist:
			preference = False
		if preference:
			preference.age = request.POST['age']
			preference.height = request.POST['height']
			preference.salary = request.POST['salary']
			preference.education = request.POST['education']
			preference.complexion = request.POST['complexion']
			preference.married = request.POST['married']
			preference.save()
		else:
			preference = Preference.objects.create(
				profile=profile,
				age=request.POST['age'],
				height=request.POST['height'],
				salary=request.POST['salary'],
				education=request.POST['education'],
				complexion=request.POST['complexion'],
				married=request.POST['married'],
			)
			preference.save()
		return HttpResponse('success')
	elif request.method == 'GET' :
		preference = Preference.objects.get(profile=profile)
		preference.delete()
		return HttpResponse('Success')

