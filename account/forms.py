from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate 
from account.models import Account, Profile
from captcha.fields import ReCaptchaField

class RegistrationForm(UserCreationForm):
	captcha = ReCaptchaField()
	
	def clean(self):
		cleaned_data = super(RegistrationForm, self).clean()
		username = cleaned_data.get('username').lower()
		email = cleaned_data.get('email').lower()
		if username and Account.objects.filter(username=username).exists():
			self.add_error('username', 'A user with that username already exists.')
		elif email and Account.objects.filter(email=email).exists():
			self.add_error('email', 'A user with that email already exists.')
		return cleaned_data
	def clean_username(self):
		username = self.cleaned_data['username'].lower()
		return username
	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		return email
	
	class Meta:
		model =  Account
		fields = ('email', 'username', 'age', 'name', 'gender', 'phone', 'dob')

class AuthenticationForm(forms.ModelForm):
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	class Meta:
		model = Account
		fields = ('email', 'password')

	def clean(self):
		email = self.cleaned_data['email']
		password = self.cleaned_data['password']
		if not authenticate(email=email, password=password):
			raise forms.ValidationError("Invalid Login")


class ProfileCreationForm(forms.ModelForm):
	class Meta:
		model = Profile
		exclude = ('user',)
