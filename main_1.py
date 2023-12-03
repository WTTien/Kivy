from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

import socket

class MyApp(App):
	def build(self):
		layout = BoxLayout(orientation='vertical')
		button = Button(text='Send Hello World to Laptop')
		button.bind(on_press=self.send_data)
		layout.add_widget(button)
		return layout

	def send_data(self, instance):
		server_ip = '192.168.137.32'
		server_port = 8080

		message = 'Hello World'

		try:
			server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			server_socket.bind((server_ip, server_port))
			server_socket.sendall(message.encode())
			server_socket.close()

		except socket.error as e:
			print(f"Error: {e}")

if __name__ == '__main__':
	MyApp().run()
