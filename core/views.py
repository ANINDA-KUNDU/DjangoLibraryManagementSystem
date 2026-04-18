from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
# Create your views here.

@login_required
def home(request):
    return render(request, 'core/home.html')

class RobotsTxtView(TemplateView):
    template_name = "core/robots.txt"