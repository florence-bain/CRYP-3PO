from django.urls import path
from django.urls.resolvers import URLPattern 
from django.views.generic.base import TemplateView

from .views import SignUpView
from . import views

urlpatterns = [
  path('home', TemplateView.as_view(template_name='home.html'), name ='home'),
]