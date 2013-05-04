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
from models import Tier, Device, Region
from controller.controller import run

def index(request):
	return render_to_response('index.html')

def test(request):
	myPort = 57013
	run(myPort)
	
	turns = Turn.objects.all()
	tiers = Tier.objects.all()
	devices = Device.objects.all()
	regions = Region.objects.all()
	
	return render_to_response('index.html', {
		'turns' : turns,
		'tiers' : tiers,
		'devices' : devices,
		'regions' : regions
	})
