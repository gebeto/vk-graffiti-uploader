# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
from PySide.QtGui import *
import requests, json, os
import threading
import downloader

class Ui_Window(object):
	def setupUi(self, Window):
		Window.setObjectName("Window")
		Window.resize(400, 400)
		self.verticalLayout = QtGui.QVBoxLayout(Window)
		self.verticalLayout.setObjectName("verticalLayout")
		self.horizontalLayout = QtGui.QVBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.music_lw = QtGui.QListWidget(Window)
		self.music_lw.setObjectName("stickers_lw")
		self.horizontalLayout.addWidget(self.music_lw)

		self.download_btn = QtGui.QPushButton(Window)
		self.download_btn.setObjectName("download_btn")
		self.horizontalLayout.addWidget(self.download_btn)

		self.download_song_progress = QtGui.QProgressBar()
		self.download_song_progress.setValue(0)
		self.horizontalLayout.addWidget(self.download_song_progress)

		self.download_playlist_btn = QtGui.QPushButton(Window)
		self.download_playlist_btn.setObjectName("download_playlist_btn")
		self.horizontalLayout.addWidget(self.download_playlist_btn)

		self.download_playlist_progress = QtGui.QProgressBar()
		self.download_playlist_progress.setValue(0)
		self.horizontalLayout.addWidget(self.download_playlist_progress)

		self.verticalLayout.addLayout(self.horizontalLayout)

		self.retranslateUi(Window)
		QtCore.QMetaObject.connectSlotsByName(Window)

	def retranslateUi(self, Window):
		Window.setWindowTitle(QtGui.QApplication.translate("Window", "Audio Downloader", None, QtGui.QApplication.UnicodeUTF8))
		self.download_btn.setText(QtGui.QApplication.translate("Window", "Download", None, QtGui.QApplication.UnicodeUTF8))
		self.download_playlist_btn.setText(QtGui.QApplication.translate("Window", "Download Playlist", None, QtGui.QApplication.UnicodeUTF8))

class Downloader(QWidget, Ui_Window):
	def __init__(self, ACCESS_TOKEN):
		super(Downloader, self).__init__()
		self.setupUi(self)
		self.song = None
		self.music = []
		self.musicKeys = []
		self.ACCESS_TOKEN = ACCESS_TOKEN
		self.download_playlist_btn.setEnabled(0)

		self.music_lw.itemClicked.connect(self.item_click_handler)
		self.download_playlist_btn.clicked.connect(self.download_playlist)
		# self.download_btn.clicked.connect(self.download_song)

		threading.Thread(target=self.load_music).start()

	def load_music(self):
		self.music = self.get_music()
		self.musicKeys = self.music.keys()
		self.add_items(self.musicKeys)

		self.download_playlist_progress.setMaximum(len(self.musicKeys))
		self.download_playlist_btn.setEnabled(1)


	def item_click_handler(self, text):
		self.song = text.text()
		self.download_btn.setText("Download")
		self.download_btn.setEnabled(1)

	def add_items(self, items):
		for each in items:
			item = QtGui.QListWidgetItem(each)
			self.music_lw.addItem(item)
			# print self.music_lw.takeItem(0)

	def download_playlist(self):
		name = self.song
		path = QFileDialog.getExistingDirectory(self, "Folder for saving stickers", "")
		if not path:
			return
		self.download_btn.setText("Downloading...")
		self.th = threading.Thread(target=downloader.download, args=(self, self.music, path))
		self.th.start()

	def get_music(self):
		url = "https://api.vk.com/method/audio.get?owner_id=-28785120&lang=ru&v=5.65&access_token=%s"%self.ACCESS_TOKEN
		music = {}
		response = requests.get(url, headers={
			"User-Agent": "com.vk.vkclient/48 (unknown, iOS 10.2, iPhone, Scale/2.000000)",
		}).json()
		print response
		for each in response["response"]["items"]:
			try:
				music.update({each["artist"] + " - " + each["title"]: each["url"]})
			except:
				pass
		return music

def main(ACCESS_TOKEN):
	app = QApplication([])
	w = Downloader(ACCESS_TOKEN)
	w.show()
	app.exec_()


if __name__ == "__main__":
	main(json.load(open('VKdata.json'))["access_token"])