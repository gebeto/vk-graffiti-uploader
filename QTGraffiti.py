# -*- coding: utf-8 -*-

from PySide.QtGui import *
from PySide import QtCore
from converter import converter
import requests
import json


class Uploader(QWidget):
	def __init__(self, ACCESS_TOKEN):
		super(Uploader, self).__init__()
		layout = QVBoxLayout(self)
		self.setWindowTitle("Uploader")
		self.setFixedWidth(200)

		# INIT
		user_lb = QLabel()
		select_file_btn = QPushButton("Select image(s)")
		self.img = QLabel()
		self.uploadStatus = QLabel()
		self.loadBar = QProgressBar()

		# BINDING
		select_file_btn.clicked.connect(self.select_file)

		# ATTRIBUTES
		user_lb.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
		self.img.setVisible(False)
		self.loadBar.setVisible(False)

		# ADDING
		layout.addWidget(user_lb)
		layout.addWidget(select_file_btn)
		layout.addWidget(self.img)
		layout.addWidget(self.uploadStatus)
		layout.addWidget(self.loadBar)
		
		# OTHER
		self.captcha_sid = ""
		self.needCaptcha = False
		self.ACCESS_TOKEN = ACCESS_TOKEN
		print(requests.get("https://api.vk.com/method/users.get?name_case=nom&access_token=%s&v=5.53&lang=en"%self.ACCESS_TOKEN).json())
		self.USER = requests.get("https://api.vk.com/method/users.get?name_case=nom&access_token=%s&v=5.53&lang=en"%self.ACCESS_TOKEN).json()["response"][0]
		self.USER_ID = self.USER["id"]
		user_lb.setText("%s %s, ID: %s\n"%(self.USER["first_name"], self.USER["last_name"], self.USER_ID))
		self.FILE = None

	def select_file(self):
		self.uploadStatus.setText("")
		self.file_path = QFileDialog.getOpenFileNames(self, "Select image for uploading", "", "*.png *.gif *.webp")
		self.loadBar.setMaximum(len(self.file_path[0]))
		self.loadBar.setVisible(True)
		for file in self.file_path[0]:
			self.loadBar.setValue(self.loadBar.value()+1)
			if file:
				self.FILE = converter(file)
				self.graffiti_send()
		self.loadBar.setValue(self.loadBar.value()+1)
		self.uploadStatus.setText("Everything Uploaded")
		
	def set_captcha(self, url):
		Image = requests.get(url).content
		pix = QPixmap()
		pix.loadFromData(Image)
		pix = pix.scaled(180,180)
		self.img.setPixmap(pix)
		self.img.setVisible(True)
		
	def get_upload_server(self, data):
		url = "https://api.vk.com/method/docs.getUploadServer"
		response = requests.post(url, data=data).json()
		return response["response"]["upload_url"]

	def upload(self, upload_type):
		files = {
			"file": ("graffiti.png", self.FILE, "image/png", {"Expires": "0"})
		}
		url = self.get_upload_server({
			"lang": "ru",
			"type": upload_type,
			"access_token": self.ACCESS_TOKEN,
			"v": "5.84"
		})
		response = requests.post(url, files=files).json()
		return response["file"]

	def docs_save(self, upload_type):
		url = "https://api.vk.com/method/docs.save"
		data = {
			"title": "graffiti.png",
			'tags': "граффити",
			"lang": "ru",
			"file": self.upload(upload_type),
			"access_token": self.ACCESS_TOKEN,
			"v": "5.54"
		}
		r = requests.post(url, data=data).json()
		try:
			response = r["response"][0]
		except:
			self.captcha_sid = r['error']['captcha_sid']
			captcha_img = r['error']['captcha_img']
			self.set_captcha(captcha_img)
			text, ok = QInputDialog.getText(self, 'Enter Captcha', 'Please enter captcha:')
			data.update({
				'captcha_sid': self.captcha_sid,
				'captcha_key': text
			})
			r = requests.post(url, data=data).json()
			response = r["response"][0]
		self.img.setVisible(False)
		return "doc%s_%s"%(response["owner_id"], response["id"])

	def graffiti_send(self):
		doc = self.docs_save("graffiti")
		self.docs_save("0")
		url = "https://api.vk.com/method/messages.send?user_id=%s&attachment=%s&access_token=%s&v=5.54"%(self.USER_ID, doc, self.ACCESS_TOKEN)
		response = requests.get(url).json()
		self.img.setPixmap(None)
		self.img.setVisible(False)

