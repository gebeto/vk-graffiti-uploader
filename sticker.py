import requests, sys, webbrowser, vk

def getUploadServer():
	url = "https://api.vk.com/method/docs.getUploadServer"
	data = {
		"lang": "ru",
		"type": "graffiti",
		"access_token": ACCESS_TOKEN,
		"v": "5.54"
	}
	response = requests.post(url, data=data).json()["response"]["upload_url"]
	# print response
	return response

def upload():
	files = {"file": FILE}
	url = getUploadServer()
	response = requests.post(url, files=files).json()["file"]
	# print response
	return response

def docsSave():
	url = "https://api.vk.com/method/docs.save"
	data = {
		"title": "graffiti.png",
		"lang": "ru",
		"file": upload(),
		"access_token": ACCESS_TOKEN,
		"v": "5.54"
	}
	response = requests.post(url, data=data).json()["response"][0]
	# print "doc%s_%s"%(response["owner_id"], response["id"])
	return "doc%s_%s"%(response["owner_id"], response["id"])

def graffitiSend(userId, doc):
	doc = docsSave()
	url = "https://api.vk.com/method/messages.send?user_id=%s&attachment=%s&access_token=%s&v=5.54"%(userId, doc, ACCESS_TOKEN)
	response = requests.get(url).json()
	print response

try:
	LOGIN = raw_input("Login: ")
	PASSWORD = raw_input("Password: ")
	ACCESS_TOKEN = vk.login(LOGIN, PASSWORD)
	FILE = open(raw_input("File Path: "), "rb") #open("graffiti.png", "rb")
	graffitiSend(raw_input("User ID: "), "doc") #graffitiSend("122248315", "doc")
except:
	print "sticker.exe <LOGIN> <PASSWORD> <FILE> <USER_ID>"

# vk.login("slavik1314@gmail.com", "emetup69")