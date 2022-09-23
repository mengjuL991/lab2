#!/usr/bin/env python3
import socket, time
from multiprocessing import Pool

HOST = "127.0.0.1"
PORT = 8081
BUFFER_SIZE = 1024

payload = """GET / HTTP/1.0
Host: {HOST}

""".format(HOST=HOST)

def connection_socket(addr_tup):
    (family, socktype, proto, canonname, sockaddr) = addr_tup
    print(addr_tup)
    try:
        s = socket.socket(family, socktype, proto)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect(sockaddr)
        s.sendall(payload.encode())

        s.shutdown(socket.SHUT_WR)

        full_data = b""
        while True:
            data = s.recv(BUFFER_SIZE)
            if not data:
                break
            full_data += data

        print(full_data)

    except Exception as e:
        print(e)
        pass
    finally:
        time.sleep(0.5)
        s.close()

def main():
    addr_info = socket.getaddrinfo(HOST, PORT, proto=socket.SOL_TCP)
    for addr_tup in addr_info:
        with Pool() as p:
            p.map(connection_socket, [addr_tup for _ in range(1, 50)])
        break

if __name__ == "__main__":
    main()
	