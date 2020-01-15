import sys
import logging
import requests

from PySide2.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QWidget,
    QLabel
)
from PySide2.QtGui import (
    QPixmap
)


from .utils import save_config


class Login(QWidget):
    def __init__(self):
        super(Login, self).__init__()
        self.setWindowTitle("Login")
        self.m_layout = QVBoxLayout(self)
        self.loginLine = QLineEdit()
        self.passwordLine = QLineEdit()
        self.captchaImg = QLabel("")
        self.captchaLine = QLineEdit()
        self.f2aLine = QLineEdit()
        self.loginButton = QPushButton("Login")

        self.loginButton.clicked.connect(self.handle_login_button_click)

        self.m_layout.addWidget(QLabel("Plese Sign In your vk.com account\nAnd restart the program"))
        self.m_layout.addWidget(self.loginLine)
        self.m_layout.addWidget(self.passwordLine)
        self.m_layout.addWidget(self.captchaImg)
        self.m_layout.addWidget(self.captchaLine)
        self.m_layout.addWidget(self.f2aLine)
        self.m_layout.addWidget(self.loginButton)

        self.setFixedWidth(300)
        self.captchaImg.setVisible(False)
        self.captchaLine.setVisible(False)
        self.f2aLine.setVisible(False)

        self.session = requests.Session()
        self.needCaptcha = False
        self.need2fa = False
        self.captchaSid = ""

        logging.info("STARTED LOGIN")

    def handle_login_button_click(self):
        token = self.login()
        if token:
            save_config(access_token=token)
            sys.exit(0)

    def setCaptcha(self, url):
        Image = requests.get(url).content
        pix = QPixmap()
        pix.loadFromData(Image)
        pix = pix.scaled(180, 70)
        self.captchaImg.setPixmap(pix)

    def login(self):
        scope = "status,friends,photos,audio,video,docs,notes,pages,wall,groups,notifications,messages"
        url = "https://api.vk.com/oauth/token"
        email = self.loginLine.text()
        password = self.passwordLine.text()
        payload = {
            "password": password,
            "scope": scope,
            "grant_type": "password",
            "username": email,
            "v": "5.40",
            "2fa_supported": "1",
            "client_secret": "VeWdmVclDCtn6ihuP1nt",
            "client_id": "3140623"
        }

        if self.needCaptcha:
            payload.update({
                'captcha_sid': self.captchaSid,
                'captcha_key': str(self.captchaLine.text())
            })
        elif self.need2fa:
            payload.update({
                'code': str(self.f2aLine.text())
                })
        response = self.session.post(url, data=payload).json()
        logging.info(f"AUTH RESPONSE: {response}")
        try:
            return response["access_token"]
        except:
            logging.error(f"AUTH ERROR: {response}")
            if response["error"] == "need_captcha":
                self.setCaptcha(response["captcha_img"])
                self.captchaLine.setVisible(True)
                self.captchaImg.setVisible(True)
                self.needCaptcha = True
                self.captchaSid = response["captcha_sid"]
            elif response["validation_type"] == "2fa_app":
                self.f2aLine.setVisible(True)
                self.need2fa = True
            else:
                self.captchaImg.setText(response["error_description"])
                self.captchaLine.setVisible(False)


def main():
    from PySide2.QtWidgets import QApplication
    app = QApplication([])
    w = Login()
    w.show()
    app.exec_()


if __name__ == "__main__":
    main()
