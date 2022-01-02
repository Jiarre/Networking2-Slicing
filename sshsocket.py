import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("", 22)
print("starting up on {} port {}".format(*server_address))
sock.bind(server_address)
sock.listen(1)

while True:
    print("waiting for a connection")
    connection, client_address = sock.accept()
    try:
        print("connection from", client_address)
        while True:
            data = connection.recv(1470)
            if data:
                connection.send(data)
            else:
                break
                
    except ConnectionResetError:
        pass

    finally:
        # Clean up the connection
        connection.close()
