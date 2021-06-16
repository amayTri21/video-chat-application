from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import socket
import sys

class Application(QMainWindow):
  def __init__(self,master):
    self.master = master
    super(Application,self).__init__()
    loadUi("application.ui",self)

    self.loginframe.setVisible(True)
    self.chatframe.setVisible(False)
    self.videoframe.setVisible(False)
    self.sidemenu.setVisible(False)

    self.loginbtn.clicked.connect(self.login)
    self.chatbtn.clicked.connect(self.showChatFrame)
    self.videobtn.clicked.connect(self.showVideoFrame)

  def login(self):
    global username
    username = self.username.text()
    if self.username.text():
      self.loginframe.setVisible(False)
      self.chatframe.setVisible(True)
      self.sidemenu.setVisible(True)
    else: self.username.text("Please enter your name.")
    self.client()

  def showVideoFrame(self):
    self.chatframe.setVisible(False)
    self.videoframe.setVisible(True)

  def showChatFrame(self):
    self.chatframe.setVisible(True)
    self.videoframe.setVisible(False)  

  def client(self):
    global username
    s = socket.socket()
    host = socket.gethostbyaddr('ec2-65-1-91-15.ap-south-1.compute.amazonaws.com')[0]
    port = 9999

    s.connect((host, port))
    data = s.send(str.encode(username))

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