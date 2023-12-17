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
		touch.ud['decide'] = 0
		self.send_data(touch.x, touch.y, 1)

	def on_touch_move(self, touch):
		touch.ud['line'].points += [touch.x, touch.y]
		touch.ud['decide'] += 1
		if touch.ud['decide'] > 5:
			self.send_data(touch.x, touch.y, 2)

	def on_touch_up(self, touch):
		self.send_data(touch.x, touch.y , 3)
		self.canvas.remove(touch.ud['line'])
		del touch.ud['line']
		self.canvas.clear()

	def send_data(self, x, y, mode):
		time.sleep(0.15)
		serverAddress = ('192.168.137.1', 8080)
		message = f'{x} , {y} ,{mode} '
		bytesToSend = message.encode('utf-8')

		try:
			clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			clientSocket.sendto(bytesToSend, serverAddress)
			print(message)

		except socket.error as e:
			print(f"Error: {e}")


class MyApp(App):
	def build(self):
		return MyWidget()

if __name__ == '__main__':
	MyApp().run()
