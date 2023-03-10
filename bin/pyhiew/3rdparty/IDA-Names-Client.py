"""
Transfer names from IDA to PyHiew - Server

This script is part of the PyHiew project.

(c) Elias Bachaalany @ 0xeb


History
---------
v1.0       - Initial version
"""

import socket
import pickle
import zlib
import idaapi
import idautils

HOST = 'localhost'
PORT = 8666

def pickle_sendz(host, port, var):
   try:
       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       s.connect((host, port))
       d = zlib.compress(pickle.dumps(var))
       s.send(d)
       s.close()
       return None
   except Exception as e:
       return str(e)

idaapi.info("Please run the Hiew-Names-Server script and press OK")

idaapi.show_wait_box("Gathering and sending names to %s:%d" % (HOST, PORT))

info = []
for ea, name in idautils.Names():
    offs = idaapi.get_fileregion_offset(ea)
    if offs == idaapi.BADADDR:
        continue

    is_func = False if idaapi.get_func(ea) is None else True
    info.append((offs, name, is_func))

ok = pickle_sendz(HOST, PORT, info)

idaapi.hide_wait_box()

if ok is not None:
    idaapi.warning("Failed to send names:\n" + ok)
else:
    idaapi.info("Names successfully transfered!")
