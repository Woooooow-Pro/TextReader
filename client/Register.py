import socket
from PyQt5 import QtWidgets

from RegisterUI import RegisterUI
from handlerfunc import register


class Register(RegisterUI):
    def __init__(self, sock, buffersize):
        super().__init__()
        self.sock = sock
        self.bufsize = buffersize

        self.pushButton_2.clicked.connect(self.__register_triger)

    def __register_triger(self):
        user_id = self.lineEdit.text()
        password = self.lineEdit_2.text()
        password2 = self.lineEdit_3.text()

        if len(user_id) <= 0:
            QtWidgets.QMessageBox.warning(self.pushButton_2,
                "Warning",
                "User ID can not be empty!",
                QtWidgets.QMessageBox.Yes)
            self.lineEdit.setFocus()
        elif len(password) <= 0 or len(password2) <= 0:
            QtWidgets.QMessageBox.warning(self.pushButton_2,
                "Warning",
                "Password can not be empty!",
                QtWidgets.QMessageBox.Yes)
            self.lineEdit.setFocus()

        elif password == password2:
            if register(self.sock, user_id, password, self.bufsize):
                self.close()
            else:
                QtWidgets.QMessageBox.warning(self.pushButton_2,
                    "Warning", "User ID have already exist",
                    QtWidgets.QMessageBox.Yes)
                self.lineEdit.setFocus()
        else:
            QtWidgets.QMessageBox.warning(self.pushButton_2,
                "Warning",
                "Please ensure that the password is the same twice",
                QtWidgets.QMessageBox.Yes)
            self.lineEdit.setFocus()