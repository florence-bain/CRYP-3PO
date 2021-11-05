"""traderunner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

from tradingbot import views


urlpatterns = [
    path('', TemplateView.as_view(
        template_name='welcomepage.html'), name='welcomepage'),
    path('admin/', admin.site.urls),
    path('home', TemplateView.as_view(template_name='home.html'), name='home'),
    path('register', views.register_request, name="register"),
    path('login', views.login_request, name="login"),
    path('logout', views.logout_request, name="logout"),
    path('welcomepage', TemplateView.as_view(
        template_name='welcomepage.html'), name='welcomepage')
]
