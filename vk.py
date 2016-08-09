import json
import requests
import os
import sys

BASE = "https://api.vk.com/oauth/token"

def login(email,password):
	scope = "status,friends,photos,audio,video,docs,notes,pages,wall,groups,notifications,messages"

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

	session = requests.Session()
	session.post(BASE, data=payload)
	r = session.post(BASE, data=payload)
	resp = json.loads(r.text)
	try:
		print resp["access_token"]
	except:
		#print resp
		sid = resp["captcha_sid"]
		fname = resp["captcha_sid"]+".jpg"
		open(fname,"wb").write(requests.get(resp['captcha_img']).content)
		os.system(fname)
		captcha = payload
		key = raw_input("Enter captcha: ")
		os.system("del "+fname)
		captcha.update({
			'captcha_sid': sid,
			'captcha_key': key
			})
		r = session.post(BASE, data=captcha)
		resp = json.loads(r.text)
		try:
			return resp["access_token"]
			# open("token.txt","w").write(resp["access_token"])
			print "Success Login!"
			raw_input("Token is saved in file TOKEN.TXT in folder with script.")
		except:
			try:
				print resp["error_description"]
				sys.exit(1)
			except:
				print "Incorrect captha!"
				sys.exit(1)

# login(raw_input("Enter Email or Number: "), raw_input("Enter Password: "))