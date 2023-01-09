import socket

import sys
from time import sleep
import select
 
clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_address = ('127.0.0.1', 8888)
clientsocket.connect(server_address)
clientsocket.setblocking(0) # non-blocking for recv()
 
while True:

    # print('$')
    # non-blocking receiving std input
    if select.select([sys.stdin], [], [], 0)[0]:
        # print('#')
        data = sys.stdin.readline(1024)
        data = data.strip('\n')
        if '\x1b' in data: break
        # sys.stdout.write(data)
        # sys.stdout.flush()
        clientsocket.sendall(data.encode())
    
    sleep(.5)
    try:
        server_data = clientsocket.recv(1024).decode()
        if server_data == '':
            print('lose server connection...')
            clientsocket.close()
            exit()
        print(server_data)
    except BlockingIOError as err: pass
