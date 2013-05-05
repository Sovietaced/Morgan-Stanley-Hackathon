# Create your views here.
import sys
import json
import socket
import datetime

from django.contrib import auth
from django.conf import settings
from django.core import serializers
from controller.controller import run
from django.template import RequestContext
from models import Tier, Device, Region, Turn
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound

def index(request):
	return render_to_response('index.html')

def get_turn_data(request, id=1):

	turn = list(Turn.objects.select_related().filter(id=id))[0]
	if turn:
		result = {
			'time' : turn.time.strftime('%Y-%m-%dT%H:%M:%S'),
			'config' : serializers.serialize('json', turn.config.all()),
			'demands' : serializers.serialize('json', turn.demands.all()),
			'distribution' : serializers.serialize('json', turn.distribution.all()),
			'profit' : serializers.serialize('json', [turn.profit]),
			'control' : serializers.serialize('json', turn.control.all()),
			'revenue_cents' : turn.revenue_cents,
			'moving_averages' : serializers.serialize('json', turn.moving_averages.all()),
		}
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		return HttpResponseNotFound('<h1>Turn not found</h1>')

def start_game(request):
	"""Starts the game"""
	result = {
		'status' : 'error',
		'message' : 'Could not start the game. Please try again'
	}
	successful_start = run(57012)
	if successful_start:
		result = {
			'status' : 'success',
			'message' : 'Successfully started the game!'
		}
	return HttpResponse(json.dumps(result), content_type="application/json")

def test(request):

	run(57012)

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
