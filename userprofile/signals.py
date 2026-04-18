from allauth.socialaccount.signals import social_account_added, social_account_updated
from django.dispatch import receiver
from . models import Profile
from django.db.models.signals import post_save
from django.contrib.auth.models import User

@receiver( social_account_added )
def create_profile_social( sender, request, sociallogin, **kwargs ):
    user = sociallogin.user
    
    if not Profile.objects.filter( user = user ).exists():
        Profile.objects.create(
            user = user, 
            first_name = user.first_name,
            last_name = user.last_name
        )

@receiver( post_save, sender = User )
def create_profile( sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create( user = instance )


    