from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .constants import GENDER_TYPE

class UserManager(BaseUserManager):
	def create_user(self, username,email, password=None,**extra):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		if not username:
			raise ValueError('Username is required.')
		user = self.model(
			email = self.normalize_email(email),
			username =username,
			**extra
		)
		user.set_password(password)
		user.save()
		return user
	def create_superuser(self ,username, email, password=None):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		user = self.model(username=username,email= email)
		user.set_password(password)
		user.is_staff = True
		user.is_superuser = True
		user.is_admin = True
		user.save()
		return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
	first_name=models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	username = models.CharField(max_length=50,unique=True)
	email = models.EmailField(max_length=50, unique=True)
	phone=models.CharField(max_length=15,null=True,blank=True)
	gender=models.CharField(max_length=10,choices=GENDER_TYPE)
	dp=models.CharField(max_length=150,null=True,blank=True)
	followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
	date_joined = models.DateTimeField(auto_now_add=True)
	last_login = models.DateTimeField(auto_now_add=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now_add=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_superadmin = models.BooleanField(default=False)
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username',]
	objects = UserManager()
	def __str__(self):
		return self.username
	

class UserAddress(models.Model):
	user = models.OneToOneField(UserAccount, related_name='address', on_delete=models.CASCADE)
	city = models.CharField(max_length= 50)
	street_address = models.CharField(max_length=50)
	street_number=models.CharField(max_length=20)
	postal_code = models.IntegerField()
	country = models.CharField(max_length=50)
	def __str__(self):
		return str(self.user.email)
