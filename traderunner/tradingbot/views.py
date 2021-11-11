from django.shortcuts import get_object_or_404, render, redirect

from .forms import NewUserForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from API.main import binancey
from tradingbot.database_helper_methods import HelperMethods

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
	#print(f" Before : {trades[0].status}")

	for trade in trades:
			orderid = trade.order_id
			if trade.symbol == "ETHUSDT_211231" or trade.symbol == "BTCUSDT":
				pass
			elif trade.status != 'NEW':
				pass
			elif trade == None:
				pass
			else:
				orderdata = binancey.get_order_status(binancey.contracts[f'{trade.symbol}'], orderid) 
				#print(orderdata)
				trade.status = orderdata.status
				trade.save()


	balance = binancey.balances['USDT']

	cryp_three_p_o_messages = ['Nothing is coming to mind at this time', 'I will keep looking']

	if len(binancey.cryp_messages) > 3:
		cryp_three_p_o_messages = binancey.cryp_messages[-5:]
	else:
		pass
			

	
	x_axis = x_values

	btc_c = btc_close
	btc_h = btc_high

	eth_c = eth_close
	eth_h = eth_high

	doge_c = doge_high
	doge_h = doge_close


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
			'messages' : cryp_three_p_o_messages,
			
		}
	return render(request, 'home.html', context)