from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
import os
import datetime

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, age, name, gender, phone, password, dob):
		user = self.model(
					email = self.normalize_email(email),
					username = username,
					name = name,
					gender = gender,
					age = age,
					dob = dob,
					phone = phone,
					password = password,
					)
		user.set_password(password)
		user.save(using = self._db)
		return user

	def create_superuser(self, email, password):
		user = self.model(email=email, password=password)
		user.set_password(password)
		user.is_staff = True
		user.is_admin = True
		user.is_superuser = True
		user.payment_status = ""
		user.save(using=self._db)
		return user

#User Account Model
class Account(AbstractBaseUser, PermissionsMixin):
	FEMALE 			= 'F'
	MALE 			= 'M'
	gender_choices	= [	(FEMALE, 'Female'), (MALE, 'Male'), ]
	deactivate_choices = [
		('Marriage Fixed', 'Marriage Fixed'),
		('Postponed', 'Postponed'),
		('Not Now', 'Not Now'),
		('Reason Not Listed', 'Reason Not Listed'),
	]

	email 			= models.EmailField(verbose_name="email", max_length=60, unique=True)
	name 			= models.CharField(verbose_name='name', max_length=50)
	age 			= models.PositiveIntegerField(verbose_name="Age", null=True, blank=True)
	gender			= models.CharField(verbose_name='gender', max_length=1, choices=gender_choices)
	phone			= models.CharField(verbose_name="phone number", max_length=10)
	username 		= models.CharField(max_length=30, unique=True)
	dob				= models.CharField(verbose_name="D.O.B", max_length=10, null=True)

	date_joined 	= models.DateTimeField(verbose_name="date joined", auto_now_add=True)
	last_login 		= models.DateTimeField(verbose_name="last login", auto_now=True)
	created_by 		= models.CharField(verbose_name="created_by", max_length=30, blank=True, null=True)
	payment_status  = models.CharField(verbose_name="Payment Status", max_length=30, default="Payment Pending")
	
	reason			= models.CharField(verbose_name="Deactivate reason", max_length=20, choices=deactivate_choices, null=True, blank=True)
	is_active		= models.BooleanField(default = True)
	is_admin		= models.BooleanField(default = False)
	is_staff		= models.BooleanField(default = False)
	is_superuser	= models.BooleanField(default = False)

	USERNAME_FIELD 	= 'email'
	REQUIRED_FIELDS	= []

	objects = MyAccountManager()
	
	def __str__(self):
		return self.email

	def has_module_perms(self, app_label):
		return True

def get_image_path(instance, filename):
	return os.path.join('users', str(instance.profile.user.id), filename)
def get_file_path(instance, filename):
	return os.path.join('users', str(instance.user.id), filename)

#User Profile Model
class Profile(models.Model):
	education_choices	= [	
		('Secondary', 'Secondary'),
		('Higher Secondary', 'Higher Secondary'),
		('Under Graduate', 'Under Graduate'),
		('Post Graduate', 'Post Graduate'),
		('Ph.D', 'Ph.D'),
		('Self Taught', 'Self Taught')
	]
	married_choices = [
		('Not married', 'Not married'),
		('Divorced', 'Divorced'),
		('Widow', 'Widow'),
		('Other reason', 'Other reason'),
	]
	numbers = [
		('0', 'None'),
		('1', '1'),
		('2', '2'),
		('3', '3'),
		('4', '4'),
		('5', '5'),
		('6', '6'),
		('7', '7'),
		('8', '8'),
	]
	choice = [
		('Yes', 'Yes'),
		('No', 'No'),
	]
	rasi_choices=[
		('Mesham' , 'Mesham'),
		('Rishabam', 'Rishabam'),
		('Mithunam','Mithunam'),
		('Kadakam','Kadakam'),
		('Simham','Simham'),
		('Kanni','Kanni'),
		('Tulam','Tulam'),
		('Vrischikam','Vrischikam'),
		('Dhanusu','Dhanusu'),
		('Makaram','Makaram'),
		('Kumbham','Kumbham'),
		('Meenam','Meenam'),
	]
	nakshatra_choices=[
		('Aswini','Aswini'),
		('Bharani','Bharani'),
		('Karthigai','Karthigai'),
		('Rohini','Rohini'),
		('Mrigasheersham','Mrigasheersham'),
		('Thiruvaathirai','Thiruvaathirai'),
		('Punarpoosam','Punarpoosam'),
		('Poosam','Poosam'),
		('Aayilyam','Aayilyam'),
		('Makam','Makam'),
		('Pooram','Pooram'),
		('Uthiram','Uthiram'),
		('Hastham','Hastham'),
		('Chithirai','Chithirai'),
		('Swaathi','Swaathi'),
		('Visaakam','Visaakam'),
		('Anusham','Anusham'),
		('Kettai','Kettai'),
		('Moolam','Moolam'),
		('Pooraadam','Pooraadam'),
		('Uthiraadam','Uthiraadam'),
		('Thiruvonam','Thiruvonam'),
		('Avittam','Avittam'),
		('Sadayam','Sadayam'),
		('Poorattathi','Poorattathi'),
		('Uthirattathi','Uthirattathi'),
		('Revathi','Revathi'),
	]
	#Personal Details
	user 				= models.OneToOneField(Account, on_delete=models.CASCADE, related_name='profile') #done
	education 			= models.CharField(max_length=40, choices=education_choices, null=True, default=3) #done
	degree 				= models.CharField(max_length=40, null=True) #done
	occupation 			= models.CharField(max_length=30, null=True) #done
	organization		= models.CharField(max_length=30, null=True)
	salary		 		= models.PositiveIntegerField(null=True) #done
	marital_status 		= models.CharField(max_length=40, choices=married_choices, null=True, default='Not married') #done
	religion 			= models.CharField(max_length=20, null=True) #done
	caste 				= models.CharField(max_length=20, default="Yadava", null=True, blank=True) #done
	rasi 				= models.CharField(max_length=20, null=True, choices=rasi_choices) #done
	nakshatra 			= models.CharField(max_length=20, null=True, choices=nakshatra_choices) #done
	subcaste 			= models.CharField(max_length=20, blank=True, null=True) #done
	height 				= models.CharField(max_length=10, blank=True, null=True) #done
	weight 				= models.CharField(max_length=10, blank=True, null=True) #done
	subcaste 			= models.CharField(max_length=20, blank=True, null=True) #done
	complexion 			= models.CharField(max_length=10, blank=True, null=True) #done
	physical_disability = models.CharField(max_length=3, choices=choice) #done
	pd_info				= models.CharField(max_length=30, blank=True, null=True) #Done

	phone1 = models.CharField(max_length=10, null=True, blank=True) #done
	phone2 = models.CharField(max_length=10, null=True, blank=True)	#done
	city = models.CharField(max_length=20, null=True) #done
	state = models.CharField(max_length=20, null=True) #done
	native_city = models.CharField(max_length=20, null=True, blank=True) #done
	native_state = models.CharField(max_length=20, null=True, blank=True) #done
	bio = models.TextField(max_length=500, null=True, blank=True) #done
	horoscope = models.FileField(upload_to=get_file_path, blank=True, null=True) #done
	
	#Family details 
	father_name = models.CharField(max_length=50, null=True) #done
	father_prof = models.CharField(max_length=20, blank=True, null=True) #done
	mother_name = models.CharField(max_length=50, null=True) #done
	mother_prof = models.CharField(max_length=20, blank=True, null=True) #done
	sibling_bro = models.CharField(max_length=4, choices=numbers, blank=True, null=True, default=0) #done
	sibling_bro_married = models.CharField(max_length=4, choices=numbers, blank=True, null=True, default=0) #done
	sibling_sis = models.CharField(max_length=4, choices=numbers, blank=True, null=True, default=0) #done
	sibling_sis_married = models.CharField(max_length=4, choices=numbers, blank=True, null=True, default=0) #done

	def __str__(self):
		return self.user.email


class ProfileImage(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	file = models.ImageField(upload_to=get_image_path) #done

	def __str__(self):
		return self.profile.user.email
