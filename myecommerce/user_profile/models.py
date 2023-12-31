from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ProfilePicture(models.Model):

    user = models.OneToOneField(User, unique=False,on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True,upload_to='profile_images/',default="profile_images/trolololol.png")

    def __str__(self):
        return self.user.username
    

