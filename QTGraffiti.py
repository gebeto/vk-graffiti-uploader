# -*- coding: utf-8 -*-

from PySide.QtGui import *
from PySide import QtCore
from gif2png import gifToPng, webpToPng
import requests, json
import QTLogin

class Uploader(QWidget):
	def __init__(self, ACCESS_TOKEN):
		super(Uploader, self).__init__()
		layout = QVBoxLayout(self)
		self.setWindowTitle("Uploader")
		self.setFixedWidth(200)

		# INIT
		user_lb = QLabel()
		selectFile_btn = QPushButton("Select image(s)")
		self.img = QLabel()
		self.uploadStatus = QLabel()
		self.loadBar = QProgressBar()

		# BINDING
		selectFile_btn.clicked.connect(self.selectFile)

		# ATTRIBUTES
		user_lb.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
		self.img.setVisible(False)
		self.loadBar.setVisible(False)

		# ADDING
		layout.addWidget(user_lb)
		layout.addWidget(selectFile_btn)
		layout.addWidget(self.img)
		layout.addWidget(self.uploadStatus)
		layout.addWidget(self.loadBar)
		
		# OTHER
		self.captcha_sid = ""
		self.needCaptcha = False
		self.FILE = None
		self.ACCESS_TOKEN = ACCESS_TOKEN
		print(requests.get("https://api.vk.com/method/users.get?name_case=nom&access_token=%s&v=5.53&lang=en"%self.ACCESS_TOKEN).json())
		self.USER = requests.get("https://api.vk.com/method/users.get?name_case=nom&access_token=%s&v=5.53&lang=en"%self.ACCESS_TOKEN).json()["response"][0]
		self.USER_ID = self.USER["id"]
		user_lb.setText("%s %s, ID: %s\n"%(self.USER["first_name"], self.USER["last_name"], self.USER_ID))

	def selectFile(self):
		self.uploadStatus.setText("")
		self.filePath = QFileDialog.getOpenFileNames(self, "Select image for uploading", "", "*.png *.gif *.webp")
		self.loadBar.setMaximum(len(self.filePath[0]))
		self.loadBar.setVisible(True)
		for file in self.filePath[0]:
			self.loadBar.setValue(self.loadBar.value()+1)
			if file:
				self.filePath = file
				if file[-3:] == "gif":
					gifToPng(file, file.split("\\")[-1][:-4])
					self.filePath = file.split("\\")[-1][:-3]+"png"
				elif file[-4:] == "webp":
					webpToPng(file, file.split("\\")[-1][:-5])
					self.filePath = file.split("\\")[-1][:-4]+"png"
				self.FILE = open(self.filePath, "rb")
				self.graffitiSend()
				self.FILE.close()
		self.loadBar.setValue(self.loadBar.value()+1)
		self.uploadStatus.setText("Everything Uploaded")
		
	def setCaptcha(self, url):
		Image = requests.get(url).content
		pix = QPixmap()
		pix.loadFromData(Image)
		pix = pix.scaled(180,180)
		self.img.setPixmap(pix)
		self.img.setVisible(True)
		
	def getUploadServer(self, type, data):
		url = "https://api.vk.com/method/docs.getUploadServer"
		data = data
		response = requests.post(url, data=data).json()
		return response["response"]["upload_url"]

	def upload(self,type):
		files = {"file": self.FILE}
		url = self.getUploadServer("graffiti",{
			"lang": "ru",
			"type": type,
			"access_token": self.ACCESS_TOKEN,
			"v": "5.84"
		})
		response = requests.post(url, files=files).json()
		return response["file"]

	def docsSave(self,type):
		url = "https://api.vk.com/method/docs.save"
		data = {
			"title": "graffiti.png",
			'tags': "граффити",
			"lang": "ru",
			"file": self.upload(type),
			"access_token": self.ACCESS_TOKEN,
			"v": "5.54"
		}
		r = requests.post(url, data=data).json()
		try:
			response = r["response"][0]
		except:
			self.captcha_sid = r['error']['captcha_sid']
			captcha_img = r['error']['captcha_img']
			self.setCaptcha(captcha_img)
			text, ok = QInputDialog.getText(self, 'Enter Captcha', 'Please enter captcha:')
			data.update({
				'captcha_sid': self.captcha_sid,
				'captcha_key': text
			})
			r = requests.post(url, data=data).json()
			response = r["response"][0]
		self.img.setVisible(False)
		return "doc%s_%s"%(response["owner_id"], response["id"])

	def graffitiSend(self):
		doc = self.docsSave("graffiti")
		self.FILE = open(self.filePath, "rb")
		self.docsSave("0")
		url = "https://api.vk.com/method/messages.send?user_id=%s&attachment=%s&access_token=%s&v=5.54"%(self.USER_ID, doc, self.ACCESS_TOKEN)
		response = requests.get(url).json()
		self.img.setPixmap(None)
		self.img.setVisible(False)

def main(ACCESS_TOKEN):
	app = QApplication([])
	w = Uploader(ACCESS_TOKEN)
	w.show()
	app.exec_()

try:
	ACCESS_TOKEN = json.load(open("VKdata.json","r"))["access_token"]
	main(ACCESS_TOKEN)
except:
	QTLogin.main()