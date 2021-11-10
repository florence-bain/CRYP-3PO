from django.shortcuts import get_object_or_404, render, redirect

from .forms import NewUserForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from API.main import binancey

from API.data_visualisation import x_values, btc_high, btc_close, eth_close, eth_high, doge_close, doge_high

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
	trades = Trade.objects.all().order_by("trade_date").reverse()
	balance = binancey.balances['USDT']

	cryp_messages = ['Hello', 'How are you friend', 'I am well', 'I hope that you are too']

	# candlesticks  = binancey.get_historical_candles(binancey.contracts['BTCBUSD'], '1d')

	# filtered = candlesticks[-30:]

	# x_values = []
	# btc_high_values = []
	# btc_close_values =[]

	# for figure in filtered:
	# 			btc_high_values.append(figure.high)
	# 			btc_close_values.append(figure.close)
	# 			time = datetime.datetime.fromtimestamp((figure.timestamp)/1000)
	# 			x_values.append(time.strftime("%m/%d/%Y"))

	
	x_axis = x_values

	btc_c = btc_close
	btc_h = btc_high

	eth_c = eth_close
	eth_h = eth_high

	doge_c = doge_high
	doge_h = doge_close




	#x_axis = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
	# btc_close = btc_close_values
	# btc_high = btc_high_values

	context = {
			'trades' : trades,
			'balance' : balance,
			'btc_high' : btc_h,
			'btc_close' : btc_c,
			'eth_high' : eth_h,
			'eth_close' : eth_c,
			'doge_close' : doge_c,
			'doge_high' : doge_h,
			'x' : x_axis,
			
		}
	return render(request, 'home.html', context)