from celery import Celery
from twilio.rest import Client
from celery.utils.log import get_task_logger
from celery.signals import worker_process_init
from decouple import config
from django.conf import settings
from channels import Group
from django.shortcuts import get_object_or_404
from parse import *
from queue import *
from math import pow
from math import pi, sqrt, atan, pow, cos
import os, socket, time, json, sys, socket, select, _thread, threading
import requests, json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'speed.settings')

app = Celery('speed', broker=config('REDISCLOUD_URL', default='redis://localhost:6379'))
app.conf.timezone = 'UTC'
logger = get_task_logger(__name__)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.broker_url = config('REDISCLOUD_URL', default='redis://localhost:6379')
app.conf.result_backend = config('REDISCLOUD_URL', default='redis://localhost:6379')

account_sid = 'ACCOUNT_SID'
auth_token = 'AUTH_TOKEN'
TwilioNumber = 'TWILIO_NUMBER'


class Child:
	def __init__(self, name, latitude, longitude):
		self.username = name
		self.lat = latitude
		self.lng = longitude


parents = dict()
lock = threading.Lock()


@worker_process_init.connect
def start_process(sender=None, conf=None, **kwargs):
	socke = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('127.0.0.1', 9992)
	print("connecting")
	# sock.connect(server_address)
	socke.bind(server_address)
	socke.listen(5)

	client = Client(account_sid, auth_token)

	while True:
		sock, client_addr = socke.accept()
		_thread.start_new_thread(on_new_client, (sock, client_addr, client))

def on_new_client(sock, addr, client):
	from dashboard.models import Person

	mph = 2.2369362920544

	inputs = [sock]
	outputs = []
	counter = 0

	acc_x = 0
	acc_y = 0
	vel_x_q = Queue()
	vel_y_q = Queue()
	pos_x_q = Queue()
	pos_y_q = Queue()
	prev_dir = 0
	cur_dir = 0
	dt = 1
	data = ''
	v_threshold = 65
	a_threshold = 10
	'''
		velocity calculation through acceleration
	'''
	pos_x = 0
	pos_y = 0
	acc_x = 0
	acc_y = 0
	vel_x = 0
	vel_y = 0
	prev_dir = 0
	cur_dir = 0
	vel = 0
	acc = 0
	start = 1
	first = 1

	v_emergency = False
	a_emergency = False

	street = ""
	
	while True:
		banner_message = ""
		#assuming input data is like '____[lat]__[lon]____' (ex. __23_34__)
		r, w, error = select.select(inputs, outputs, inputs)


		for s in r:
			raw = s.recv(8)
			temp = raw.decode('utf-8')
			#print(temp)
			data += temp

			maps = 1 if counter % 5 == 0 else 0

			if(data.find('|') == -1):
				continue
			parsed = data.rsplit(",")
			parsed = list(filter(None, parsed))
			# parsed is a list: [user, position_x, position_y, acc_x, acc_y, '|']

			if (pos_x_q.qsize() < 2):
			    # build the initial position queue
				pos_x_q.put(111111*int(parsed[1])*pi/(1000*180)) #assume this is latitude
				pos_y_q.put(111111*cos(int(parsed[1])/1000)*int(parsed[2])/1000)
				vel_x_q.put(0)
				vel_y_q.put(0)
			else:
				'''
					velocity calculation through position
				'''
				# NOTE: since using GPS coordinates, lower velocities will have larger error
			    # get position
				pos_x_q.put(111111*float(parsed[1])/1000)
				pos_y_q.put(111111*cos(float(parsed[1])*pi/(1000*180))*float(parsed[2])/1000)
				# velocity processing
				cur_vel_x = 111111*float(parsed[1])/1000 - pos_x_q.get()
				vel_x_q.put(cur_vel_x)
				cur_vel_y = 111111*cos(float(parsed[1])*pi/(1000*180))*float(parsed[2])/1000 - pos_y_q.get()
				vel_y_q.put(cur_vel_y)
				vel = sqrt(pow(cur_vel_x,2) + pow(cur_vel_y,2))/dt #NOTE: x and y values need to be divided by dt
				# acceleration processing
				acc_x = cur_vel_x - vel_x_q.get()
				acc_y = cur_vel_y - vel_y_q.get()
				acc = sqrt(pow(acc_x,2) + pow(acc_y,2))/dt
				'''
					velocity calculation through acceleration
				'''
				# NOTE: due to Reinmann sum calculation, first couple velocity points will be less accurate
				# NOTE: if loop is optional in this implementation
				# get position
				pos_x = float(parsed[1])/1000
				pos_y = float(parsed[2])/1000
				# get acceleration
				acc_x = float(parsed[3])/1000
				acc_y = float(parsed[4])/1000
				acc = sqrt(pow(acc_x,2) + pow(acc_y,2))
				# velocity processing
				vel_x += acc_x*dt
				vel_y += acc_y*dt
				vel = sqrt(pow(vel_x,2) + pow(vel_y,2))

				'''
					direction calculations
				'''
				# NOTE: If using acceleration calculation method: replace cur_vel_x with vel_x and cur_vel_y with vel_y
				prev_dir = cur_dir
				cur_dir = 90 if not cur_vel_x else atan(cur_vel_y/cur_vel_x)*180/pi
				'''
					emergency!
				'''
				if(vel > v_threshold and not v_emergency):
					myPhone = "+1" + get_object_or_404(Person, username=parsed[0]).parent_name.all()[0].phone
					banner_message = "{} is travelling at {} mph. He/She may die.".format(parsed[0], vel)
					# NOTE: remove following line to stop recieving messages
					client.messages.create(
						to=myPhone,
						from_=TwilioNumber,
						body=banner_message)
					print("send text message!")
					v_emergency = True
				elif(vel > v_threshold):
					banner_message = "{} is travelling at {} mph. He/She may die.".format(parsed[0], vel)
				else:
					v_emergency = False

				if(acc > a_threshold and not a_emergency):
					myPhone = "+1" + get_object_or_404(Person, username=parsed[0]).parent_name.all()[0].phone
					# NOTE: remove following line to stop recieving messages
					banner_message = "{} underwent high acceleration. There may have been a crash".format(parsed[0])
					client.messages.create(
						to=myPhone,
						from_=TwilioNumber,
						body=banner_message)
					print("send text message!")
					a_emergency = True
				elif(acc > a_threshold):
					banner_message = "{} underwent high acceleration. There may have been a crash".format(parsed[0])
				else:
					a_emergency = False


			parent = get_object_or_404(Person, username=parsed[0]).parent_name.all()[0]

			number = 1
			for c in parent.parent_name.all():
				if c.username == parsed[0]:
					break
				number += 1

			if(counter % 10 == 0):
				key = "GOOGLE_GEOCODING_KEY"
				base = "https://maps.googleapis.com/maps/api/geocode/json?"
				params = "latlng={lat},{lon}&key={key}".format(
			        lat=float(parsed[1])/1000,
			        lon=float(parsed[2])/1000,
			        key=key
				)
				url = "{base}{params}".format(base=base, params=params)
				response = json.loads(requests.get(url).content.decode('utf-8'))
				street = response['results'][0]['formatted_address']

			child_data = json.dumps({
				'type': "update",
				'username': parsed[0],
				'number': number,
				'speed': str(round(vel*mph, 2)),
				'acceleration': str(round(acc*mph, 2)),
				'limit': v_threshold,
				'maps': maps,
				'latitude': str(round(float(parsed[1])/1000, 4)),
				'longitude': str(round(float(parsed[2])/1000, 4)),
				'banner': banner_message,
				'street': street,
			})
			#print(child_data)
			start = 0

			temp_child = Child(parsed[0], float(parsed[1])/1000, float(parsed[2])/1000)

			parent_username = get_object_or_404(Person, username=parsed[0]).parent_name.all()[0].username




			global parents
			lock.acquire()
			if(parent_username in parents):
				parents[parent_username][temp_child.username] = temp_child
			else:
				parents[parent_username] = {temp_child.username: temp_child}

			temp_set = parents[parent_username]
			midpoint_lat = 0
			midpoint_lng = 0
			i = 0
			for key in temp_set:
				i += 1
				midpoint_lat += temp_set[key].lat
				midpoint_lng += temp_set[key].lng
			midpoint_lat /= i
			midpoint_lng /= i
			midpoint = json.dumps({
				'type': "midpoint",
				'm_lat': str(round(midpoint_lat, 4)),
				'm_lng': str(round(midpoint_lng, 4)),
				'username': parsed[0],
				'number': number,
				'speed': str(round(vel*mph, 2)),
				'acceleration': str(round(acc*mph, 2)),
				'limit': v_threshold,
				'maps': maps,
				'latitude': str(round(float(parsed[1])/1000, 4)),
				'longitude': str(round(float(parsed[2])/1000, 4)),
				'banner': banner_message,
				'street': street,
			})
			if(first or (counter % 10 == 0)):
				Group(parent_username).send({'text': midpoint})
				first = 0
			else:
				Group(parent_username).send({'text': child_data})
			lock.release()

			data = ""
			counter += 1

		