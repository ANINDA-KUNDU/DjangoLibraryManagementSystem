from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile( models.Model ):
    user = models.OneToOneField( User, on_delete = models.CASCADE )
    first_name = models.CharField( max_length = 255, null = True, blank = True )
    last_name = models.CharField( max_length = 255, null = True, blank = True )
    location = models.CharField( max_length = 255, null = True, blank = True )
    profile_image = models.FileField(
        upload_to = 'userprofile/profile_image/',
        default = 'userprofile/default.jpg',
        blank = True,
    )
    
    def __str__(self):
        return self.user.username