from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from account.models import Profile, ProfileImage, Account
from account.forms import ProfileCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
# Create your views here.

#View for ABout Us page
def about_us(request):
	context = {}
	profile = Profile.objects.get(user=request.user)
	profile_image = ProfileImage.objects.get(profile=profile)
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

def home(request):
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
			email = request.POST['email']
			password = request.POST['password']
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
	profile_image = ProfileImage.objects.get(profile=profile)
	if profile.user.gender == 'M':
		get_profiles = Profile.objects.filter(user__gender = 'F')
		latest_profiles = get_profiles.order_by('-user__date_joined')[:3]
	else:
		get_profiles = Profile.objects.filter(user__gender = 'M')
		latest_profiles = get_profiles.order_by('-user__date_joined')[:3]
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
	}
	return render(request, 'mainApp/feed.html', context )

def sort_by(request, key, value):
	context = {}
	profile = Profile.objects.get(user=request.user)
	profile_image = ProfileImage.objects.get(profile=profile)
	if profile.user.gender == 'M' :
		if key == 'rasi':
			get_profiles = Profile.objects.filter(user__gender = 'F', rasi = value)
		else:
			get_profiles = Profile.objects.filter(user__gender = 'F', nakshatra = value)
		latest_profiles = Profile.objects.filter(user__gender = 'F').order_by('-user__date_joined')[:3]
	else:
		if key == 'rasi':
			get_profiles = Profile.objects.filter(user__gender = 'M', rasi = value)
		else:
			get_profiles = Profile.objects.filter(user__gender = 'M', nakshatra = value)
		latest_profiles = Profile.objects.filter(user__gender = 'F').order_by('-user__date_joined')[:3]
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
	}
	return render(request, 'mainApp/sort_by.html', context )

def manage_profile(request):
	context = {}
	if request.POST:
		user = Profile.objects.get(user__email = request.user)
		profile = ProfileImage.objects.get(profile = user)
		if bool(request.FILES.get('profile_image', False)) == True:
			profile.file = request.FILES['profile_image']
			profile.save()
		if bool(request.FILES.get('horoscope', False)) == True:
			user.horoscope = request.FILES['horoscope']
			user.save()
		return redirect('manage_profile')

	profile = Profile.objects.get(user=request.user)
	profile_image = ProfileImage.objects.get(profile=profile)
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
	view_profile_image = ProfileImage.objects.get(profile=view_profile)
	profile_image = ProfileImage.objects.get(profile__user=request.user)
	context = {
		'view_profile' : view_profile,
		'view_profile_image' : view_profile_image,
		'profile_image' : profile_image,

	}
	return render(request, 'mainApp/view_profile.html', context)

