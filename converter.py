import os
import requests
from bs4 import BeautifulSoup
from requests_toolbelt.multipart.encoder import MultipartEncoder


def get_converter_data(image, image_type):
	multipart = MultipartEncoder(fields={
		'new-image': ('new-image', image, 'image/gif'),
		'new-image-url': ('new-image-url')
	})
	response = requests.post(
		"https://s5.ezgif.com/{0}".format(image_type),
		data=multipart,
		headers={
			"Content-Type": multipart.content_type
		}
	)
	soup = BeautifulSoup(response.text, 'html.parser')
	link_name = soup.find_all('input')[0]['value']
	token = soup.find_all('input')[1]['value']
	return link_name, token
	

def convert(image, image_type):
	link_name, token = get_converter_data(image, image_type)
	r = requests.post(
		"https://s5.ezgif.com/{0}/{1}?ajax=true".format(image_type, link_name),
		data={
			"file": link_name,
			"token": token
		}
	)
	soup = BeautifulSoup(r.text, "html.parser")
	link_name_png = soup.find_all(attrs={"class": "save"})[0]["href"]
	r = requests.get(link_name_png)
	return r.content


def gif_to_png(image_path):
	return convert(open(image_path, "rb"), "gif-to-apng")

	
def webp_to_png(image_path):
	return convert(open(image_path, "rb"), "webp-to-png")


def default(image_path):
	return open(image_path, "rb").read()


def converter(image_path):
	ext = image_path.split(os.path.extsep)[-1]
	f = globals().get("{}_to_png".format(ext), default)
	# f = globals().get("{}_to_png".format(ext))
	return f(image_path)

