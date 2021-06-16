from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import socket,cv2, pickle,struct
import sys

username = ""

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

  def showVideoFrame(self):
    self.chatframe.setVisible(False)
    self.videoframe.setVisible(True)

  def showChatFrame(self):
    self.chatframe.setVisible(True)
    self.videoframe.setVisible(False)

  

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