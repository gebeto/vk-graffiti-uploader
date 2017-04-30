# -*- coding: utf-8 -*-

from PySide.QtGui import *
from PySide import QtCore
import requests, json
from pprint import pprint

class Uploader(QWidget):
	def __init__(self, ACCESS_TOKEN):
		super(Uploader, self).__init__()
		layout = QVBoxLayout(self)
		self.setWindowTitle("Uploader")
		self.setFixedWidth(200)

		# INIT
		user_lb = QLabel()
		selectFile_btn = QPushButton("Select PNG image")
		self.img = QLabel()
		self.upload_btn = QPushButton("Upload")
		self.uploadStatus = QLabel()

		# BINDING
		selectFile_btn.clicked.connect(self.selectFile)
		self.upload_btn.clicked.connect(self.graffitiSend)

		# ATTRIBUTES
		user_lb.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
		self.img.setVisible(False)
		self.upload_btn.setEnabled(False)

		# ADDING
		layout.addWidget(user_lb)
		layout.addWidget(selectFile_btn)
		layout.addWidget(self.upload_btn)
		layout.addWidget(self.img)
		layout.addWidget(self.uploadStatus)

		# OTHER
		self.FILE = None
		self.ACCESS_TOKEN = ACCESS_TOKEN
		# self.ACCESS_TOKEN = json.load(open("VKdata.json","r"))["access_token"]
		self.USER = requests.get("https://api.vk.com/method/users.get?name_case=nom&access_token=%s&v=5.53&lang=en"%self.ACCESS_TOKEN).json()["response"][0]
		self.USER_ID = self.USER["id"]
		user_lb.setText("%s %s, ID: %s\n"%(self.USER["first_name"], self.USER["last_name"], self.USER_ID))

	def selectFile(self):
		self.upload_btn.setText("Upload")
		self.uploadStatus.setText("")
		self.filePath = QFileDialog.getOpenFileName(self, "Select image for uploading", "", "*.png")[0]
		if self.filePath:
			self.FILE = open(self.filePath, "rb")
			self.upload_btn.setEnabled(True)
			self.setImage()

	def setImage(self):
		pix = QPixmap(self.filePath)
		pix = pix.scaled(180,180)
		self.img.setPixmap(pix)
		self.img.setVisible(True)

	def getUploadServer(self):
		url = "https://api.vk.com/method/docs.getUploadServer"
		data = {
			"lang": "ru",
			"type": "graffiti",
			"access_token": self.ACCESS_TOKEN,
			"v": "5.54"
		}
		response = requests.post(url, data=data).json()
		# print response
		return response["response"]["upload_url"]

	def upload(self):
		files = {"file": self.FILE}
		url = self.getUploadServer()
		response = requests.post(url, files=files).json()
		# print response
		return response["file"]

	def docsSave(self):
		url = "https://api.vk.com/method/docs.save"
		data = {
			"title": "graff1iti.png",
			"lang": "ru",
			"file": self.upload(),
			"access_token": self.ACCESS_TOKEN,
			"v": "5.54"
		}
		response = requests.post(url, data=data).json()["response"][0]
		pprint(response)
		# return "doc%s_%s"%(response["owner_id"], response["id"])
		return (response["owner_id"], response["id"])

	def graffitiSend(self):
		owner_id, doc_id = self.docsSave()
		url = "https://api.vk.com/method/messages.send?user_id=%s&attachment=%s&access_token=%s&v=5.54"%(owner_id, "doc" + str(owner_id) + "_" + str(doc_id), self.ACCESS_TOKEN)
		# print self.USER_ID
		# url = "https://api.vk.com/method/docs.add?owner_id=%s&doc_id=%s&access_token=%s&v=5.64"%(owner_id, doc_id, self.ACCESS_TOKEN)
		response = requests.get(url).json()
		# print response
		pprint(response)
		self.uploadStatus.setText("Done: " + str(response))
		self.upload_btn.setText("Uploaded!")

def main(ACCESS_TOKEN):
	app = QApplication([])
	w = Uploader(ACCESS_TOKEN)
	w.show()
	app.exec_()
