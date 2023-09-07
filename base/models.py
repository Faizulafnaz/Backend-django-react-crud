from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    body = models.TextField()


class UserProfile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_img = models.ImageField(upload_to='profile_images',blank=True, null=True)
    Phone_no = models.CharField(max_length=50, blank=True, null=True)