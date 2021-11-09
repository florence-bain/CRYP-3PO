from django.shortcuts import get_object_or_404, render, redirect

from .forms import NewUserForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from API.main import binancey

from API.data_visualisation import x_axis,y_axis

import datetime
import pandas as pd

from tradingbot.models import Trade


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="registration/register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="registration/login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/login")

def home(request):
	trades = Trade.objects.all().order_by("trade_date")
	contracts = binancey.contracts

	candlesticks  = binancey.get_historical_candles(binancey.contracts['BTCBUSD'], '1d')

	filtered = candlesticks[-30:]

	x_values = []
	y_values = []

	for figure in filtered:
				y_values.append(figure.high)
				time = datetime.datetime.fromtimestamp((figure.timestamp)/1000)
				x_values.append(time.strftime("%m/%d/%Y"))

	
	x_axis = x_values
	#x_axis = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
	y_axis = y_values

	context = {
			'trades' : trades,
			'contracts' : contracts,
			'y' : y_axis,
			'x' : x_axis,
			
		}
	return render(request, 'home.html', context)