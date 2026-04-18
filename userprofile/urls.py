from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:pk>', views.profile, name = "profile"),
    path('edit-profile/<int:pk>', views.edit_profile, name = "edit_profile"),
]