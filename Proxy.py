import socket
import sys
import threading
import _thread

try:
    list_port = int(input("Enter port number: "))
except KeyboardInterrupt:
    print("User Interupt")
    print("Application exiting.. ")
    sys.exit()


max_conn = 10
buffer_size = 4096


def start():
    try:
        Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Socket.bind(('', list_port))

        Socket.listen(max_conn)
        print("Initializing  socket...  Done")
        print("Sockets binded successfully...")
        print("server started successfully %d \n " % (list_port))
    except Exception:
        print("Unable to Initialize Socket...")
        sys.exit(2)

    while True:
        try:
            (conn, addr) = Socket.accept()
            data = conn.recv(buffer_size)
            print("data")
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
        if(webserver_pos == -1):
            webserver_pos = len(temp)
        webserver = ""

        port2 = -1
        if(port_pos == -1 or webserver_pos < port_pos):
            port2 = 80
            webserver = temp[:webserver_pos]
        else:
            port2 = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]

        # proxy_server(webserver, port2, conn, addr, data)
    except Exception:
        pass


def proxy_server(webserver, port, conn, addr, data):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((webserver, port))
        s.send(data)

        while 1:
            reply = s.recv(buffer_size)

            if(len(reply) > 0):
                conn.send(reply)
                dar = float(len(reply))
                dar = float(dar/1024)
                dar = ("%0.3s" % (str(dar)))
                dar = ("%s KB" % (dar))
                print("Request Done: %s => %s <=" % (str(addr[0]), str(dar)))
            else:
                break

        s.close()
        conn.close()
    except socket.error:
        s.close()
        conn.close()
        sys.exit(1)


start()
