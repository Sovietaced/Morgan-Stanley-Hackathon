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

def index(request):
	return render_to_response('index.html')

def socket_test(request):
	myPort = 57012
	connection = connect(myPort)
	if connection:
		costs = connection.recv(4096)
		str = costs
		connection.send('START')
		str += " " + connection.recv(4096)
		return render_to_response('test.html', {
			'str' : str,
		})
	else:
		print 'Connection Failed'


def connect(port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('67.202.15.69', int(port)))
	s.send('INIT brogrammers')
	s.recv(4096)
	s.send('RECD')
	return s
