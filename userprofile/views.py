from django.shortcuts import render, get_object_or_404, redirect
from . models import Profile
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def profile(request, pk):
    user = User.objects.all()
    profile = get_object_or_404( Profile, id = pk )
    return render(request, 'userprofile/profile.html', {'profile': profile, 'user': user})

def edit_profile(request, pk):
    profile = get_object_or_404(Profile, id = pk)
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        location = request.POST.get('location')
        profile_image = request.FILES.get('profile_image')

        profile.first_name = first_name
        profile.last_name = last_name
        profile.location = location
        if profile_image:
            profile.profile_image = profile_image
        profile.save()
        messages.success(request, 'The Edits have been done successfully.')
        return redirect('profile', profile.pk)
    return render(request, 'userprofile/edit_profile.html', {'profile': profile})