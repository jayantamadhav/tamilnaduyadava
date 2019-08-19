from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AuthenticationForm, ProfileCreationForm
from account.models import ProfileImage, Account, Profile
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import datetime

def UserRegistration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			#form.save()
			email 			= form.cleaned_data.get('email').lower()
			raw_password 	= form.cleaned_data.get('password1')
			username 		= form.cleaned_data.get('username')
			dob 			= form.cleaned_data.get('dob')
			name			= form.cleaned_data.get('name')
			phone 			= form.cleaned_data.get('phone')
			gender 			= form.cleaned_data.get('gender')
			user = form.save(commit=False)
			user.created_by = 'End User'
			now = datetime.datetime.now()
			user.age = now.year - int(dob[-4:])
			user.save()
			print(now.year - int(dob[-4:]))

			if user:
				user = authenticate(username=email, password=raw_password)
				login(request, user)
				return redirect('createProfile')
		else:
			context['registration_form'] = form
	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)

def logout_view(request):
	logout(request)
	return redirect('home')

@login_required(login_url='home')
def CreateProfile_view(request):
	context = {}
	if request.POST:
		form = ProfileCreationForm(request.POST)
		if form.is_valid():
			profile = form.save(commit=False)
			profile.user = request.user
			filepath = request.FILES.get('horoscope', False)
			if filepath:
				profile.horoscope = request.FILES['horoscope']
			profile.save()
			filepath = request.FILES.get('profile_image', False)
			if filepath:
				p = Profile.objects.get(user=request.user)
				a = ProfileImage.objects.create(profile = p,file= request.FILES['profile_image'])
				a.save()
			return redirect('feed')
		else:
			context['profile_form'] = form
	else:
		form = ProfileCreationForm()
		context['profile_form'] = form
	return render(request, 'account/createProfile.html', context)