from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserManager:
    @staticmethod
    def create_user(first_name,last_name,email,username, password):
        user = User(email = email,username=username,first_name = first_name,last_name = last_name,is_active = False)
        user.set_password(password)
        user.save()
        return user

class Accounts(models.Model):
    first_name =  models.CharField(max_length=15)
    last_name =  models.CharField(max_length=15)
    email = models.CharField(max_length=30,null=True)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
   
class UserEmailConfirmationNumber(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    email_confirmation_number = models.CharField(max_length=10,null=True)

    def __str__(self):
        return f"{self.user} {self.email_confirmation_number}"