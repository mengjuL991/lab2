#!/usr/bin/env python3

import socket
from multiprocessing import Process

HOST = ""
PORT = 8081
BUFFER_SIZE = 1024

addr_info = socket.getaddrinfo("www.google.com", 80, proto=socket.SOL_TCP)
(family, socktype, proto, canonname, sockaddr) = addr_info[0]

def handle_request(client_conn, addr):

	with socket.socket(family, socktype) as proxy_end:
		proxy_end.connect(sockaddr)

		client_data = b""
		while True:
			data = client_conn.recv(BUFFER_SIZE)
			if not data: break
			client_data += data
		proxy_end.sendall(client_data)

		# Receive data from google and forward to client
		response_data = b""
		while True:
			data = proxy_end.recv(BUFFER_SIZE)
			if not data: break
			response_data += data

		client_conn.sendall(response_data)
		client_conn.close()

def main():
	
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((HOST, PORT))
		s.listen(1)

		while True:
			client_conn, addr = s.accept()
			p = Process(target=handle_request, args=(client_conn, addr))
			p.daemon = True
			p.start()
			print("Process: ", p)

if __name__ == "__main__":
	main()