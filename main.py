# -*- coding: utf-8 -*-

import json

from PySide2.QtWidgets import QApplication

import QTLogin
from QTGraffiti import Uploader


def main(ACCESS_TOKEN):
    app = QApplication([])
    w = Uploader(ACCESS_TOKEN)
    w.show()
    app.exec_()


try:
    file = open("VKdata.json", "r")
    file_data = json.load(file)
    ACCESS_TOKEN = file_data.get("access_token")
    print(ACCESS_TOKEN)
    main(ACCESS_TOKEN)
except:
    QTLogin.main()
