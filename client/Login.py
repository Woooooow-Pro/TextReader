import socket
from PyQt5 import QtCore, QtWidgets

from LoginUI import LoginUI
from Register import Register
from handlerfunc import login
from TextReaderUI import Reader


class Login(LoginUI):
    def __init__(self, sock, buffersize):
        super().__init__()
        self.sock = sock
        self.bufsize = buffersize
        self.regUI = Register(sock, buffersize)
        self.readUI = Reader(sock, buffersize)

        self.pushButton.clicked.connect(self.__register)
        self.pushButton_2.clicked.connect(self.__login_triger)
    
    def __login_triger(self):

        user_id = self.lineEdit.text()
        password = self.lineEdit_2.text()

        if len(user_id) <= 0:
            QtWidgets.QMessageBox.warning(self.pushButton,
                "Warning",
                "User ID can not be empty!",
                QtWidgets.QMessageBox.Yes)
            self.lineEdit.setFocus()
        elif len(password) <= 0:
            QtWidgets.QMessageBox.warning(self.pushButton,
                "Warning",
                "Password can not be empty!",
                QtWidgets.QMessageBox.Yes)
            self.lineEdit.setFocus()

        elif login(self.sock, user_id, password, self.bufsize) == 1:


            self.readUI.set_login(user_id)
            self.readUI.initUi()
            self.readUI.show()
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self.pushButton,
                "Warning",
                "Wrong User ID or Password!",
                QtWidgets.QMessageBox.Yes)
            self.lineEdit.setFocus()

    def __register(self):
        self.regUI.show()
        # self.close()

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

    reader = Reader(sock, buffersize)
    ui1 = Login(sock,buffersize)
    ui1.show()
    sys.exit(app.exec_())