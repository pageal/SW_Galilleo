import socket
TCP_IP = "192.168.1.40"
TCP_PORT = 5002
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print('Connected with: {}'.format(addr))


while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print "received :", data

    if(data.strip().find("close server") == 0):
        print "closing server"
        break
    conn.send("ack: {}\n".format(data))  # acknowledge
conn.close()




