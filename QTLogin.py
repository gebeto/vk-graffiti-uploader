from PySide.QtGui import *
import requests, sys, json

class Login(QWidget):
	def __init__(self):
		super(Login, self).__init__()
		self.setWindowTitle("Login")
		self.Mlayout = QVBoxLayout(self)
		self.loginLine = QLineEdit()
		self.passwordLine = QLineEdit()
		self.captchaImg = QLabel("")
		self.captchaLine = QLineEdit()
		self.loginButton = QPushButton("Login")

		def btn():
			token = self.login()
			if token:
				json.dump({"access_token": token}, open("VKdata.json", "w"))
				sys.exit(0)
		self.loginButton.clicked.connect(btn)

		self.Mlayout.addWidget(QLabel("Plese Sign In your vk.com account\nAnd restart the program"))
		self.Mlayout.addWidget(self.loginLine)
		self.Mlayout.addWidget(self.passwordLine)
		self.Mlayout.addWidget(self.captchaImg)
		self.Mlayout.addWidget(self.captchaLine)
		self.Mlayout.addWidget(self.loginButton)

		self.setFixedWidth(200)
		self.captchaImg.setVisible(False)
		self.captchaLine.setVisible(False)

		self.session = requests.Session()
		self.needCaptcha = False
		self.captchaSid = ""

	def setCaptcha(self, url):
		Image = requests.get(url).content
		pix = QPixmap()
		pix.loadFromData(Image)
		pix = pix.scaled(180,70)
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
		response = self.session.post(url, data=payload).json()
		try:
			return response["access_token"]
		except:
			if response["error"] == "need_captcha":
				self.setCaptcha(response["captcha_img"])
				self.captchaLine.setVisible(True)
				self.captchaImg.setVisible(True)
				self.needCaptcha = True
				self.captchaSid = response["captcha_sid"]
			else:
				self.captchaImg.setText(response["error_description"])
				self.captchaLine.setVisible(False)


def main():
	app = QApplication([])
	w = Login()
	w.show()
	app.exec_()

if __name__ == "__main__":
	main()