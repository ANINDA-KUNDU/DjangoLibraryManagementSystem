from django.db import models
import uuid
from django.contrib.auth.models import User


# Create your models here.

class PasswordReset( models.Model ):
    user = models.ForeignKey( User, on_delete = models.CASCADE )
    reset_id = models.UUIDField( editable = False, unique = True, default = uuid.uuid4  )
    created_at = models.DateTimeField( auto_now_add = True )
    
    def __str__(self):
        return f"The password reset was created for {self.user.username} at {self.created_at}"
    
    class Meta:
        verbose_name_plural = "Password Reset"