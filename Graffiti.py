# -*- coding: utf-8 -*-

import requests, sys, webbrowser, vk, json

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
	print "VK Graffiti uploader by Slavik Nychkalo v1.01\n"
	LOGIN = ""
	PASSWORD = ""
	try:
		data = json.load(open("VKdata.json","r"))
		LOGIN = data["login"]
		PASSWORD = data["password"]
	except:
		print "VK.COM Authorization"
		LOGIN = raw_input("Login: ")
		PASSWORD = raw_input("Password: ")
	ACCESS_TOKEN = vk.login(LOGIN, PASSWORD)
	json.dump({
			"login": LOGIN,
			"password": PASSWORD
		}, open("VKdata.json","w"))
	USER = requests.get("https://api.vk.com/method/users.get?name_case=nom&access_token=%s&v=5.53&lang=en"%ACCESS_TOKEN).json()["response"][0]
	USER_ID = USER["id"]
	print "%s %s, ID: %s\n"%(USER["first_name"], USER["last_name"], USER_ID)
	FILE = open(raw_input("File Path(Drag PNG image to console): "), "rb") #open("graffiti.png", "rb")
	graffitiSend(str(USER_ID), "doc") #graffitiSend("122248315", "doc")
	raw_input("Success!")
except:
	raw_input("Failed!")
