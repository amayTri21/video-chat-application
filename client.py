from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import socket
import threading
import sys
import pickle
class Application(QMainWindow):
    def __init__(self, master):
        self.master = master
        super(Application, self).__init__()
        loadUi("application.ui", self)

        self.loginframe.setVisible(True)
        self.chatframe.setVisible(False)
        self.videoframe.setVisible(False)
        self.sidemenu.setVisible(False)

        self.loginbtn.clicked.connect(self.login)
        self.chatbtn.clicked.connect(self.showChatFrame)
        self.videobtn.clicked.connect(self.showVideoFrame)
        self.sendbtn.clicked.connect(self.write)

    def login(self):
        global username
        username = self.username.text()
        if self.username.text():
            self.loginframe.setVisible(False)
            self.chatframe.setVisible(True)
            self.sidemenu.setVisible(True)
        else:
            self.username.text("Please enter your name.")
        self.client()

    def showVideoFrame(self):
        self.chatframe.setVisible(False)
        self.videoframe.setVisible(True)

    def showChatFrame(self):
        self.chatframe.setVisible(True)
        self.videoframe.setVisible(False)

    def client(self):
        global PORT
        global FORMAT
        global SERVER
        global client
        global username

        PORT = 5050
        FORMAT = "utf-8"
        SERVER = socket.gethostbyaddr('ec2-13-233-126-234.ap-south-1.compute.amazonaws.com')[0]
        #SERVER = '192.168.56.1'

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER, PORT))

        #receive_thread = threading.Thread(target=self.receive)
        #receive_thread.start() 

        # write_thread = threading.Thread(target=self.write)  
        # write_thread.start()

        # create the receive thread
        self.receive_thread = Receive()
        # connect its signal to the showMessages slot
        self.receive_thread.send_msg.connect(self.showMessages)
        self.receive_thread.send_users.connect(self.showOnlineUsers)
        # start the thread
        self.receive_thread.start()

    def write(self):
        message = f'{username} > {self.messagetxt.text()}'
        client.send(message.encode(FORMAT))
        self.messagetxt.setText("")

    @pyqtSlot(str)
    def showMessages(self,message):
        label = QLabel()
        label.setFixedWidth(840)
        label.setFixedHeight(50)
        label.setFont(QFont('',14))
        label.setText(message)
        label.setStyleSheet("background: rgba(255,255,255,0.6);border-radius:5px; padding:10px 10px")
        self.messagesLayout.addWidget(label)

    @pyqtSlot(list)
    def showOnlineUsers(self,onlineUsers):
        for i in reversed(range(self.usersLayout.count())): 
            self.usersLayout.itemAt(i).widget().deleteLater()
        for online in onlineUsers:
            user = QPushButton()
            user.setFixedHeight(50)
            user.setFixedWidth(200)
            user.setFont(QFont('',14))
            user.setText(online)
            user.setStyleSheet("background: rgba(255,255,255,0.6);border-radius:5px; padding:10px 10px")
            self.usersLayout.addWidget(user)

class Receive(QThread):
    send_msg = pyqtSignal(str)
    send_users = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        while self._run_flag:
            try:
                message = client.recv(1024).decode(FORMAT)
                if message == 'NICK':
                    client.send(username.encode(FORMAT))
                elif message == 'USERS':
                    onlineUsers = client.recv(1024)
                    onlineUsersList = pickle.loads(onlineUsers)
                    print("onlineUsersList - ",onlineUsersList)
                    self.send_users.emit(onlineUsersList)
                else:
                    self.send_msg.emit(message)              
            except:
                print("an error occured!")    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loginwindow = Application('dummy')
    widgets = QtWidgets.QStackedWidget()
    widgets.addWidget(loginwindow)
    widgets.setMinimumWidth(1200)
    widgets.setMinimumHeight(800)
    widgets.setWindowTitle("OLES-VideoChatApplication")
    widgets.show()
    app.exec_()
