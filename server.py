import socket
import sys
import threading

all_connections = []
all_address = []
all_usernames = []

# Create a Socket (connect two computers)
def create_socket():
  try:
    global host
    global port
    global s
    host_name  = socket.gethostname()
    host = socket.gethostbyname(host_name)
    port = 9999
    s = socket.socket()

  except socket.error as msg:
    print("Socket creation error: " + str(msg))

# Binding the socket and listening for connections
def bind_socket():
  try:
    global host
    global port
    global s
    print("Binding the Port: " + str(port))

    s.bind((host, port))
    s.listen(5)

  except socket.error as msg:
    print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
    bind_socket()

# Handling connection from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted

def accepting_connections():
  for c in all_connections:
    c.close()

  del all_connections[:]
  del all_address[:]
  del all_usernames[:]

  while True:
    try:
      conn, address = s.accept()
      s.setblocking(1)  # prevents timeout

      all_connections.append(conn)
      all_address.append(address)

      data = str(conn.recv(1024), "utf-8")
      all_usernames.append(data)
      print("Connection has been established : " + address[0] + " " + data)

      conn.send(str.encode(tuple(all_usernames)))

    except:
      print("Error accepting connections")

create_socket()
bind_socket()
accepting_connections()