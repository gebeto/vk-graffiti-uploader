import requests
import logging

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QProgressBar,
    QInputDialog,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QWidget,
    QLabel
)
from PySide2.QtGui import (
    QPixmap
)

from converter import converter
from utils import read_config


class Uploader(QWidget):
    def __init__(self, ACCESS_TOKEN):
        super(Uploader, self).__init__()
        layout = QVBoxLayout(self)
        self.setWindowTitle("Uploader")
        self.setFixedWidth(300)

        # INIT
        user_info_label = QLabel()
        select_file_btn = QPushButton("Select image(s)")
        self.img = QLabel()
        self.uploadStatus = QLabel()
        self.loadBar = QProgressBar()

        # BINDING
        select_file_btn.clicked.connect(self.select_file)

        # ATTRIBUTES
        user_info_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.img.setVisible(False)
        self.loadBar.setVisible(False)

        # ADDING
        layout.addWidget(user_info_label)
        layout.addWidget(select_file_btn)
        layout.addWidget(self.img)
        layout.addWidget(self.uploadStatus)
        layout.addWidget(self.loadBar)

        # OTHER
        self.captcha_sid = ""
        self.needCaptcha = False
        self.ACCESS_TOKEN = ACCESS_TOKEN
        response = requests.get(
            "https://api.vk.com/method/users.get?name_case=nom&access_token={access_token}&v=5.53&lang=en".format(
                access_token=self.ACCESS_TOKEN
            )
        ).json()
        self.user = response["response"][0]
        user_info_label.setText("%(first_name)s %(last_name)s, ID: %(id)s\n" % self.user)
        self.FILE = None
        logging.info("STARTED UPLOADER")

    def select_file(self):
        self.uploadStatus.setText("")
        self.file_path, masks = QFileDialog.getOpenFileNames(self, "Select image for uploading", "", "*.png *.gif *.webp")
        logging.info(f"SELECTED {len(self.file_path)} IMAGES")
        self.loadBar.setMaximum(len(self.file_path))
        self.loadBar.setVisible(True)
        for file in self.file_path:
            self.loadBar.setValue(self.loadBar.value() + 1)
            if file:
                self.FILE = converter(file)
                logging.info(f"SENDING IMAGE {file}")
                self.graffiti_send()
                logging.info(f"SENDED IMAGE {file}")
        self.loadBar.setValue(self.loadBar.value() + 1)
        self.uploadStatus.setText("Everything Uploaded")
        logging.info(f"ALL IMAGES UPLOADED")

    def set_captcha(self, url):
        Image = requests.get(url).content
        pix = QPixmap()
        pix.loadFromData(Image)
        pix = pix.scaled(180, 180)
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
        resp = requests.post(url, data=data).json()
        try:
            response = resp["response"][0]
        except Exception:
            logging.error("DOC SAVE ERROR: {response}")
            self.captcha_sid = resp['error']['captcha_sid']
            captcha_img = resp['error']['captcha_img']
            self.set_captcha(captcha_img)
            text, ok = QInputDialog.getText(self, 'Enter Captcha', 'Please enter captcha:')
            data.update({
                'captcha_sid': self.captcha_sid,
                'captcha_key': text
            })
            resp = requests.post(url, data=data).json()
            response = resp["response"][0]
        self.img.setVisible(False)
        return "doc%(owner_id)s_%(id)s" % response

    def graffiti_send(self):
        doc = self.docs_save("graffiti")
        self.docs_save("0")
        url = "https://api.vk.com/method/messages.send?user_id=%(user_id)s&attachment=%(doc)s&access_token=%(access_token)s&v=5.54" % {
            "access_token": self.ACCESS_TOKEN,
            "user_id": self.user["id"],
            "doc": doc,
        }
        response = requests.get(url).json()
        logging.info(f"GRAFFITI SEND RESPONSE: {response}")
        self.img.setPixmap(None)
        self.img.setVisible(False)


def main():
    config = read_config()
    ACCESS_TOKEN = config.get("access_token")
    from PySide2.QtWidgets import QApplication
    app = QApplication([])
    w = Uploader(ACCESS_TOKEN)
    w.show()
    app.exec_()


if __name__ == "__main__":
    main()
