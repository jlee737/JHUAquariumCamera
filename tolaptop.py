import socket
import joystick
import time

joy = joystick.Joystick()
joy.start()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	ip = '0.0.0.0'
	port = 5005
	address = (ip, port)

	s.bind(address)
	
	while True:
		s.listen(1)
		conn, remote_addr = s.accept()
		with conn:
			try:
				while True:
					message = f"{joy.left()} {joy.right()} {joy.up()} {joy.down()}".encode()
					conn.send(message)
					time.sleep(0.05)
			except ConnectionError as e:
				pass
