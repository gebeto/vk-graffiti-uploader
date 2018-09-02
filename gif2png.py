import requests
from bs4 import BeautifulSoup
from requests_toolbelt.multipart.encoder import MultipartEncoder

def cnvert(inGif,name,type):
	m = MultipartEncoder(
	fields={
				'new-image': ('new-image', open(inGif, 'rb'), 'image/gif'),
				'new-image-url': ('new-image-url')
			}
		)
	r = requests.post('https://s5.ezgif.com/%s'%type, data=m,
					  headers={'Content-Type': m.content_type})
	soup = BeautifulSoup(r.text, 'html.parser')
	link_name = soup.find_all('input')[0]['value']
	token = soup.find_all('input')[1]['value']
	r = requests.post("https://s5.ezgif.com/{0}/{1}?ajax=true".format(type, link_name), data={'file': link_name, 'token': token})
	soup = BeautifulSoup(r.text, 'html.parser')
	link_name_png = soup.find_all(attrs={'class':"save"})[0]['href']
	r = requests.get(link_name_png)
	with open(name+".png", 'wb') as fd:
		fd.write(r.content)
	return True

def gifToPng(inGif,name):
	cnvert(inGif,name,"gif-to-apng")
	
def webpToPng(inGif,name):
	cnvert(inGif,name,"webp-to-png")