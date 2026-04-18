from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
# Create your models here.

class Book( models.Model ):
    user = models.ForeignKey( User, on_delete = models.CASCADE )
    image_book = models.ImageField( upload_to = 'book/image_book/', null = True, blank = True ) 
    name = models.CharField()
    author = models.CharField()
    borrower_name = models.CharField()
    issue_date = models.DateTimeField( auto_now_add = True )
    modified_date = models.DateTimeField( auto_now = True )
    is_returned = models.BooleanField( default = False )
    
    def __str__(self):
        return self.borrower_name
    
    class Meta:
        verbose_name_plural = 'Book' 
           
    @property
    def late_days(self):
        expiration_day = self.issue_date + timezone.timedelta( days = 3 )
        
        if timezone.now() <= expiration_day :
            return 0
        
        late_days = (timezone.now() - expiration_day).days
        return late_days
    
    @property
    def late_fine(self):
        return int(self.late_days) * 5
    