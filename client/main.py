import socket

from PyQt5 import QtWidgets
from Login import Login

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    host = '127.0.0.1'
    port = 8878
    addr = (host,port)
    buffersize = 8192

    sock = socket.socket()
    try:
        sock.connect(addr)
    except Exception:
        print('error')
        sock.close()
        sys.exit()

    ui1 = Login(sock,buffersize)
    ui1.show()
    sys.exit(app.exec_())