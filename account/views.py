from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AuthenticationForm, ProfileCreationForm
from account.models import ProfileImage, Account, Profile
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
import random
import msg91_sms as msgsms

def send_sms(phone, otp):
	msg = msgsms.Cspd_msg91(apikey='183393AKXfwYZqohk5a08b057')
	sms_txt = str(otp) + " is the OTP required to register at tamilnaduyadava.com"
	send_sms_resp = msg.send( 4, 'TNYADV', phone, sms_txt)
	return True


def phone_verify(request):
	system_messages = messages.get_messages(request)
	for message in system_messages:
		pass
	system_messages.used = True
	user_data = request.session.get('registration_data')
	otp = request.session.get('generated_otp')
	phone = user_data['phone']
	verified = False
	if request.POST:
		if str(request.POST['otp']) == str(otp):
			verified = True
			messages.success(request, 'OTP verified', extra_tags='notification is-success is-size-4')
			email 			= user_data['email'].lower()
			raw_password 	= user_data['password1']
			username 		= user_data['username']
			dob 			= user_data['dob']
			name			= user_data['name']
			phone 			= user_data['phone']
			gender 			= user_data['gender']
			created_by 		= 'End User'
			now = datetime.datetime.now()
			#generate age
			get_age = str(dob)
			get_age = int(get_age[6:])
			age = now.year - get_age
			user = Account.objects.create(
				email = email,
				password = raw_password,
				username = username,
				dob = dob,
				name = name,
				phone = phone,
				gender = gender,
				created_by = created_by,
				age = age,
			)
			user.save()
			if user:
				login(request, user)
				#generate Matrimonial ID
				random_id = "{:05d}".format(request.user.id)
				matrimony_id = 'TNY' + now.strftime('%y%m%d') + random_id
				user = Account.objects.get(id = request.user.id)
				user.m_id = matrimony_id
				user.save()
				return redirect('createProfile')
		else:
			messages.error(request, 'OTP entered is not valid', extra_tags="notification is-danger")
	if request.GET:
		if request.GET['type'] == 'generate_new':
			new_otp = ""
			for i in range(6):
				new_otp += str(random.randint(0,9))
			send_sms(phone, new_otp)
			otp = new_otp
			return HttpResponse('success')
		else:
			send_sms(phone, otp)
			return HttpResponse('success')
	context = {
		'phone' : phone,
		'verified' : verified,
	}
	return render(request, 'account/phone_verify.html', context)

def UserRegistration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			request.session['registration_data'] = request.POST
			phone = request.POST['phone']
			phone = '91' + str(phone)
			otp = ""
			for i in range(6):
				otp += str(random.randint(0,9))
			send_sms(phone, otp)
			request.session['generated_otp'] = otp
			return redirect('phone_verify')
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