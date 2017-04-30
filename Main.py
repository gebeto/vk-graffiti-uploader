from PySide.QtGui import *
import QTDownloader, QTLogin, QTGraffiti, QTAudioDownloader
import json, sys

class Main(QWidget):
	def __init__(self, ACCESS_TOKEN):
		super(Main, self).__init__()
		layout = QVBoxLayout(self)
		self.setWindowTitle("Menu")
		self.setFixedSize(200, 120)
		self.ACCESS_TOKEN = ACCESS_TOKEN

		downoader_btn = QPushButton("Sticker Downloader")
		uploader_btn = QPushButton("Graffiti Uploader")
		audio_downloader_btn = QPushButton("Audio Downloader")

		downoader_btn.clicked.connect(self.downloader)
		uploader_btn.clicked.connect(self.uploader)
		audio_downloader_btn.clicked.connect(self.audio_downloader)

		layout.addWidget(QLabel("Created by Slavik Nychkalo"))
		layout.addWidget(downoader_btn)
		layout.addWidget(uploader_btn)
		layout.addWidget(audio_downloader_btn)


	def downloader(self):
		self.down = QTDownloader.MainWindow(self.ACCESS_TOKEN)
		self.down.show()

	def uploader(self):
		self.down = QTGraffiti.Uploader(self.ACCESS_TOKEN)
		self.down.show()

	def audio_downloader(self):
		self.down = QTAudioDownloader.Downloader(self.ACCESS_TOKEN)
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