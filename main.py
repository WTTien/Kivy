from kivy.app import App
from kivy.graphics import Rectangle, Line
from kivy.uix.widget import Widget

import socket

class MyWidget(Widget):
	def on_touch_down(self, touch):
		touch.ud['line'] = Line(points=(touch.x, touch.y))
		self.canvas.add(touch.ud['line'])
		self.send_data(touch.x, touch.y, 1)

	def on_touch_move(self, touch):
		touch.ud['line'].points += [touch.x, touch.y]
		self.send_data(touch.x, touch.y, 2)

	def send_data(self, x, y, mode):
		serverAddress = ('192.168.137.1', 8080)
		y = 1080 - y
		message = f'{x} , {y} ,{mode} '
		bytesToSend = message.encode('utf-8')

		try:
			clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			clientSocket.sendto(bytesToSend, serverAddress)

		except socket.error as e:
			print(f"Error: {e}")

class MyApp(App):
	def build(self):
		return MyWidget()

if __name__ == '__main__':
	MyApp().run()
