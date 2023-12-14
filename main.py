from kivy.app import App
from kivy.graphics import Rectangle, Line
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.clock import Clock

import socket
import time
from enum import Enum

class MouseMode(Enum):
	CLICK = 1
	MOVE = 2
	DOUBLE_CLICK = 3
	MOUSE_DOWN = 4
	MOUSE_UP = 5



class MyWidget(Widget):

	def on_touch_down(self, touch):
		touch.ud['start_time'] = time.time()
		if self.collide_point(*touch.pos) and touch.is_double_tap:
			touch.ud['double_tap'] = True
			print("DOUBLE TAP TRUE")
#			self.send_data(touch.x, touch.y, 1)
#			self.send_data(touch.x, touch.y, 4)
		else:
			touch.ud['double_tap'] = False
			print("DOUBLE TAP FALSE")

		touch.ud['line'] = Line(points=(touch.x, touch.y))
		self.canvas.add(touch.ud['line'])
		touch.ud['prev_x'] = touch.x
		touch.ud['prev_y'] = touch.y
		touch.ud['decide'] = 0

	def on_touch_move(self, touch):
		touch.ud['line'].points += [touch.x, touch.y]
#		touch.ud['decide'] += 1
		x = touch.x - touch.ud['prev_x']
		y = touch.y - touch.ud['prev_y']
		touch.ud['prev_x'] = touch.x
		touch.ud['prev_y'] = touch.y
#		if touch.ud['decide'] > 5:
#		self.send_data(x, y, 2)
		if touch.ud['double_tap'] == False:
			self.send_data(x, y, 2)
		elif touch.ud['double_tap'] == True:
			self.send_data(x, y, 3)

	def on_touch_up(self, touch):
		if touch.ud['double_tap'] == False:
#			if touch.ud['decide'] < 5 and (time.time() - start_time()) < 0.5:
			if time.time() - touch.ud['start_time'] < 0.5:
				self.send_data(touch.x, touch.y, 1)
#				self.send_data(touch.x, touch.y, 1)
#				time.sleep(0.2)
#				self.send_data(touch.x, touch.y, 3)
#				time.sleep(0.2)
		elif touch.ud['double_tap'] == True:
			if time.time() - touch.ud['start_time'] < 0.5:
#				time.sleep(0.2)
#				self.send_data(touch.x, touch.y, 3)
				self.send_data(touch.x, touch.y, 1)
			else:
				self.send_data(touch.x, touch.y, 5)

		self.canvas.remove(touch.ud['line'])
		del touch.ud['line']
		self.canvas.clear()

	def send_data(self, x, y, mode):
		serverAddress = ('192.168.137.1', 8080)
		x = x * 2
		y = -y * 2
		message = f'{x} , {y} ,{mode} '
		bytesToSend = message.encode('utf-8')

		try:
			clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			clientSocket.sendto(bytesToSend, serverAddress)
			print(message)

		except socket.error as e:
			print(f"Error: {e}")

#	def send_data_interval(self, dt):
#		self.send_data(x, y, touch.ud['mode'])

class MyApp(App):
	Config.set('input','multitouch_double_tap_time', '0.2')
	def build(self):
		return MyWidget()

if __name__ == '__main__':
	MyApp().run()
