from kivy.app import App
from kivy.graphics import Rectangle, Line
from kivy.uix.widget import Widget
from kivy.config import Config

import socket
import time

class MyWidget(Widget):

	def on_touch_down(self, touch):
		touch.ud['line'] = Line(points=(touch.x, touch.y))
		self.canvas.add(touch.ud['line'])
		touch.ud['prev_x'] = touch.x
		touch.ud['prev_y'] = touch.y
		touch.ud['decide'] = 0

		self.send_data(touch.x, touch.y, 1)

	def on_touch_move(self, touch):
		touch.ud['line'].points += [touch.x, touch.y]

#		x = touch.x - touch.ud['prev_x']
#		y = touch.y - touch.ud['prev_y']
#		touch.ud['prev_x'] = touch.x
#		touch.ud['prev_y'] = touch.y

		self.send_data(touch.x, touch.y, 2)

	def on_touch_up(self, touch):
		self.send_data(touch.x, touch.y , 3)

		self.canvas.remove(touch.ud['line'])
		del touch.ud['line']
		self.canvas.clear()

	def send_data(self, x, y, mode):
		serverAddress = ('192.168.137.1', 8080)
#		x = x
#		y = -y
		message = f'{x} , {y} ,{mode} '
		bytesToSend = message.encode('utf-8')

		try:
			clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			clientSocket.sendto(bytesToSend, serverAddress)
			print(message)

		except socket.error as e:
			print(f"Error: {e}")


class MyApp(App):
	Config.set('input','multitouch_double_tap_time', '0.2')
	def build(self):
		return MyWidget()

if __name__ == '__main__':
	MyApp().run()
