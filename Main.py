from PySide.QtGui import *
import QTDownloader, QTLogin, QTGraffiti
import json, sys

class Main(QWidget):
	def __init__(self, ACCESS_TOKEN):
		super(Main, self).__init__()
		layout = QVBoxLayout(self)
		self.setWindowTitle("Menu")
		self.setFixedSize(200, 100)
		self.ACCESS_TOKEN = ACCESS_TOKEN

		downoader_btn = QPushButton("Sticker Downloader")
		uploader_btn = QPushButton("Graffiti Uploader")

		downoader_btn.clicked.connect(self.downloader)
		uploader_btn.clicked.connect(self.uploader)

		layout.addWidget(QLabel("Created by Slavik Nychkalo"))
		layout.addWidget(downoader_btn)
		layout.addWidget(uploader_btn)

		# try:
		# 	data = json.load(open("VKdata.json","r"))
		# 	self.ACCESS_TOKEN = data["access_token"]
		# except:
		# 	self.login()
		# 	data = json.load(open("VKdata.json","r"))
		# 	self.ACCESS_TOKEN = data["access_token"]


	def downloader(self):
		self.down = QTDownloader.MainWindow(self.ACCESS_TOKEN)
		self.down.show()

	def uploader(self):
		self.down = QTGraffiti.Uploader(self.ACCESS_TOKEN)
		self.down.show()

	def login(self):
		self.login = QTLogin.Login()
		self.login.show()


def main(ACCESS_TOKEN):
	app = QApplication([])
	w = Main(ACCESS_TOKEN)
	w.show()
	app.exec_()

try:
	ACCESS_TOKEN = json.load(open("VKdata.json","r"))["access_token"]
	main(ACCESS_TOKEN)
except:
	QTLogin.main()