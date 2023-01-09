#!/usr/bin/env python
#-*- coding:utf-8 -*-
 
import socket
import select
import queue

import datetime
 
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ("127.0.0.1", 8888)
serversocket.bind(server_address)
serversocket.listen(10)
serversocket.setblocking(False)  
timeout = 10
epoll = select.epoll()
epoll.register(serversocket.fileno(), select.EPOLLIN)
message_queues = {}
fd_to_socket = {serversocket.fileno():serversocket,}
fd_to_info = {serversocket.fileno():server_address}
 
while True:
    events = epoll.poll(timeout)
    if not events:
        continue
    
    for fd, event in events:
        # print(fd, '', hex(event))
        _socket = fd_to_socket[fd]
        if _socket == serversocket:
            connection, address = serversocket.accept()
            connection.setblocking(False)
            epoll.register(connection.fileno(), select.EPOLLIN)
            info = connection.getpeername()
            print(f'client {info[0]}:{info[1]} connected...')
            fd_to_info[connection.fileno()] = info
            fd_to_socket[connection.fileno()] = connection
            message_queues[connection] = queue.Queue()

        elif event & select.EPOLLHUP:
            info = fd_to_info[fd]
            epoll.unregister(fd)
            fd_to_socket[fd].close()
            print(f'client {info[0]}:{info[1]} closed...')
            del fd_to_socket[fd]

        elif event & select.EPOLLIN:
            data = _socket.recv(1024)
            if data:
                # print('test put')
                message_queues[_socket].put(data)
                epoll.modify(fd, select.EPOLLOUT)

        elif event & select.EPOLLOUT:
            try:
                msg = message_queues[_socket].get_nowait()
            except queue.Empty:
                print (_socket.getpeername() , " empty queue")
                epoll.modify(fd, select.EPOLLIN)
                pass
            else :
                time = datetime.datetime.now().time().__str__()[0:8]
                ip = _socket.getpeername()[0]
                port = _socket.getpeername()[1]
                # print(type(msg))
                _socket.send(bytes(time+' [Me] > ', 'utf-8')+msg)
                for _fd in fd_to_socket.keys():
                    skt = fd_to_socket[_fd]
                    if skt != serversocket and skt != _socket:
                        skt.send(bytes(time+f' [{ip}: {port}] > ', 'utf-8')+msg)
                epoll.modify(fd, select.EPOLLIN)