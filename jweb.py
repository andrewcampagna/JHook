import os
import threading
import time
import requests

class JWebContentWatcher():
	"""JWebContentWatcher object

	Object instantiation:
	Provide the content watcher with at minimum a URL to be watched. 
	This mechanism scrapes content using [GET] requests, comparing it 
	to the previous. You can modify this default to an [POST] application 
	with JSON data.
	
	[POST] requests:
	When creating this type of request, you must declare it when instantiating 
	the content watcher object using request_head. Along with this, you must 
	also include JSON data using the post_data argument.
	
	Advanced thread daemon options:
	There is no need to set these threading options; however, they are customizable 
	for advanced configuration. Check time refers to the frequency in which the daemon 
	monitors the file selected; this must be greater than 1. You can pass in a custom 
	change function to execute when the hook triggers.
	"""

	def __init__(self, url, change_function=None, check_time=1, logging=False, request_head="GET", post_data=None):

		self.url = url
		self.change_function = change_function
		self.check_time = check_time
		self.logging = logging
		self.request_head = request_head
		self.post_data = post_data
		self.running = False
		self.data = ""
		self.daemon = None
		self.__load_website_data()

	def exec_request(self):
		"""Makes web request and returns response..."""

		data = None
		if self.request_head == "GET":
			data = requests.get(self.url).content
		elif self.requests_head == "POST":
			data = requests.post(self.url, json=self.post_data).content
		return data


	def __load_website_data(self):
		"""Reloads content from website into self.data..."""

		self.data = self.exec_request()

	def __check_daemon(self):
		"""Daemon function..."""

		while (self.running):
			content = self.exec_request()
			if content != self.data:
				self.data = content
				if self.logging:
					print(f"Content changed for website {self.url}")
				if type(self.change_function) is tuple:
					if "jweb_data" in self.change_function[1].keys():
						self.change_function[1]["jweb_data"] = self.data
					if "jweb_url" in self.change_function[1].keys():
						self.change_function[1]["jweb_url"] = self.url
					self.change_function[0](**self.change_function[1])
				else:
					self.change_function()
			time.sleep(self.check_time)

		if self.logging:
			print(f"Daemon ended for website {self.url}")

	def run_hook(self):
		"""Builds new daemon thread..."""

		self.daemon = threading.Thread(target=self.__check_daemon, name='JWebContentWatcher daemon')
		self.running = True
		self.daemon.start()

		if self.logging:
			print(f"Web content watcher started on {self.url}")

	def stop_hook(self):
		"""Stops currently running daemon thread..."""

		if self.running:
			self.running = False

		if self.logging:
			print(f"Web content watcher stopped on {self.url}")





