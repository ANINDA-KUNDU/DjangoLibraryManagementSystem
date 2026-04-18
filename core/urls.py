from django.urls import path
from . import views
from .views import RobotsTxtView

urlpatterns = [
    path('', views.home, name = "home"),
    path('robots.txt', RobotsTxtView.as_view( content_type = 'text/plain' ), name = "robots"),
]