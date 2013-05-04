# Create your views here.
import sys
import socket
import datetime

from django.contrib import auth
from django.conf import settings
from django.utils import simplejson
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response, get_object_or_404
from controller.controller import main

def index(request):
	return render_to_response('index.html')

def socket_test(request):
	myPort = 57012
	main(myPort)
	return render_to_response('index.html')
