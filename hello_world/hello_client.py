#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      MPASHA
#
# Created:     31/07/2015
# Copyright:   (c) MPASHA 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import socket
TCP_IP = '192.168.1.40'
TCP_PORT = 5002
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send("Hello")
answer = s.recv(BUFFER_SIZE)
print(answer)

print("done")
