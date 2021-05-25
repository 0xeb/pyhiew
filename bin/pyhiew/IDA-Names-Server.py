"""
Transfer names from IDA to PyHiew - Client

(c) Elias Bachaalany
"""
import socket
import zlib
import pickle
import sys
import hiew

HOST = 'localhost'
PORT = 8666

# -----------------------------------------------------------------------
def IDANamesMain():
#def testMain():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
    except Exception as e:
        hiew.Window.FromString("Error", ["Could not listen on %s:%d" % (HOST, PORT), str(e)])
        return

    w = hiew.Window()
    w.Create(
       title = "Hiew-IDA-Names-Server",
       lines = [
       "", "",
        "Waiting for name list from IDA (%s:%d)" % (HOST, PORT),
        "", "", "",
        "- ESC key to cancel",
        "- F1: All names",
        "- F2: Only functions",
        "- F3: Not functions"],
        width = 70,
        main_keys = {1:"All", 2:"funcs", 3:"!funcs"}
    )

    # Show the window
    n, k = w.Show()

    if k == hiew.HEM_INPUT_ESC:
        return
    elif k == hiew.HEM_FNKEY_F2:
        filter = 1
    elif k == hiew.HEM_FNKEY_F3:
        filter = 2
    else:
        filter = 0

    # set timeout
    s.settimeout(0.5)

    # Show wait box
    hiew.MessageWaitOpen()

    names = []
    while not hiew.IsKeyBreak():
        try:
           conn, addr = s.accept()
        except socket.timeout:
           # try to accept again
           continue

        # disable blocking mode
        conn.setblocking(1)
        conn.settimeout(None)

        while True:
           zdata = b''
           # Receive all bytes
           while True:
               b = conn.recv(1024 * 10)
               if not b:
                   break
               zdata += b

           # Deserialize
           names = pickle.loads(zlib.decompress(zdata))
           break

        # Close the connection
        conn.close()
        break

    # Hide wait box
    hiew.MessageWaitClose()

    if names:
        cnt = 0
        # Add names
        for offs, name, is_func in names:
            if (filter == 0) or \
               (filter == 1 and is_func) or \
               (filter == 2 and not is_func):
                cnt += 1
                hiew.Names.AddGlobal(offs, name)

        hiew.Window.FromString("Info", "%d name(s) transferred" % cnt)
    else:
        hiew.Window.FromString("Error", "Server cancelled")

# -----------------------------------------------------------------------
IDANamesMain()