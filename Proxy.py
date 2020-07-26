import socket
import sys
import threading
import _thread

try:
    port = int(input("Enter port number: "))
except KeyboardInterrupt:
    print("User Interupt")
    print("Application exiting.. ")
    sys.exit()


max_conn = 5
buffer_size = 4096


def start():
    try:
        Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Socket.bind('', port)
        Socket.listen(max_conn)
        print("Initializing  socket...  Done")
        print("Sockets binded successfully...")
        print("server started successfully %d \n " % (port))
    except Exception, e:
        print("Unable to Initialize Socket...")
        sys.exit(2)

    while True:
        try:
            (conn, addr) = Socket.accept()
            data = conn.recv(buffer_size)
            _thread.start_new_thread(conn_string, (conn, data, addr))
        except KeyboardInterrupt:
            Socket.close()
            print("Proxy Server Shutting down")
            sys.exit(1)

    Socket.close()


def conn_string(conn, data, addr):
    try:
        print(data)
        first_line = data.split('\n')[0]
        url = first_line.split(' ')[1]
        https_pos = url.find("://")
        if(https_pos == -1):
            temp = url
        else:
            temp = url[(https_pos+3):]

        port_pos = temp.find(":")
        webserver_pos = temp.find("/")
