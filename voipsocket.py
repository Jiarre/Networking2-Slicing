import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ("", 5060)
print("starting up on {} port {}".format(*server_address))
sock.bind(server_address)

# Listen for incoming connections


while True:
    # Wait for a connection
    print("waiting for a connection")
    

    # Receive the data in small chunks and retransmit it
    while True:
        data, address = sock.recvfrom(1470)
        send_data = data
        sock.sendto(send_data, address)
        