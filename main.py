# -*- coding: utf-8 -*-

from PySide.QtGui import *
from QTGraffiti import Uploader
import QTLogin


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