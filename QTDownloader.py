# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
from PySide.QtGui import *
import requests, json, os

class Ui_Window(object):
    def setupUi(self, Window):
        Window.setObjectName("Window")
        Window.resize(383, 213)
        self.verticalLayout = QtGui.QVBoxLayout(Window)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QVBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.stickers_lw = QtGui.QListWidget(Window)
        self.stickers_lw.setObjectName("stickers_lw")
        self.horizontalLayout.addWidget(self.stickers_lw)
        self.download_btn = QtGui.QPushButton(Window)
        self.download_btn.setObjectName("download_btn")
        self.horizontalLayout.addWidget(self.download_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Window)
        QtCore.QMetaObject.connectSlotsByName(Window)

    def retranslateUi(self, Window):
        Window.setWindowTitle(QtGui.QApplication.translate("Window", "Stickers Downloader", None, QtGui.QApplication.UnicodeUTF8))
        self.download_btn.setText(QtGui.QApplication.translate("Window", "Download", None, QtGui.QApplication.UnicodeUTF8))

class MainWindow(QWidget, Ui_Window):
    def __init__(self, ACCESS_TOKEN):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.ACCESS_TOKEN = ACCESS_TOKEN
        self.download_btn.setEnabled(0)
        self.stickers = self.getStickers()
        self.stickerKeys = self.stickers.keys()
        self.addItems(self.stickerKeys)
        self.stickers_lw.itemClicked.connect(self.itemClick)
        self.download_btn.clicked.connect(self.downloadStickerPack)

    def itemClick(self, text):
        # print text.text()
        self.sticker = text.text()
        print text.text()
        self.download_btn.setEnabled(1)

    def addItems(self, items):
        for each in items:
            self.stickers_lw.addItem(each)

    def downloadStickerPack(self):
    	import threading
        print self.sticker
        ids = self.stickers[self.sticker]
        name = self.sticker
        path = QFileDialog.getExistingDirectory(self, "Folder for saving stickers", "")
        if path:
            path = path + "\\" + name
        else:
            return 0
        name = path
        print path
        def download(ids, name):
            try:
                os.mkdir(name)
            except:
                pass
            print "Downloading...\n"
            for stickerId in ids:
                url = "https://vk.com/images/stickers/%s/512.png"%stickerId
                open(str(name)+"/"+str(stickerId)+".png", "wb").write(requests.get(url).content)
                print url
            print "Done!"
        threading.Thread(target=download, args=(ids, name)).start()

    def getStickers(self):
        url = "https://api.vk.com/method/store.getStockItems?lang=en&type=stickers&v=5.54&access_token=%s"%self.ACCESS_TOKEN
        stickers = {}
        response = requests.get(url).json()
        for each in response["response"]["items"]:
            try:
                # print each["product"]["title"]
                stickers.update({each["product"]["title"]: each["product"]["stickers"]["sticker_ids"]})
            except:
                pass
        return stickers

def main(ACCESS_TOKEN):
    app = QApplication([])
    w = MainWindow(ACCESS_TOKEN)
    w.show()
    app.exec_()
