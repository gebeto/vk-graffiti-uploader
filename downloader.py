import requests


def download(self, music, path):
	path += "\\"
	for i, song in enumerate(music.keys()):
		url = music[song]
		try:
			download_file(self, url, path + song + ".mp3")
			self.download_playlist_progress.setValue(i)
			self.update()
		except:
			pass


def download_file(self, url, filename):
	self.download_song_progress.setValue(0)
	self.download_btn.setText(filename.split('\\')[-1])

	percentage = 0
	file = ""
	size = int(requests.head(url).headers["Content-Length"])
	
	self.download_song_progress.setMaximum(100)

	downloaded_length = 0
	chunk = size / 40
	open(filename, "wb").close()
	while downloaded_length <= size:
		if size - downloaded_length < chunk:
			headers = {"Range": "bytes=%s-%s" % (downloaded_length + 1, size)}
			# file += requests.get(url, headers=headers).content
			open(filename, "ab").write(requests.get(url, headers=headers).content)
			break
		else:
			downloaded_length += chunk
			headers = {"Range": "bytes=%s-%s" % (downloaded_length - chunk + 1, downloaded_length)}
			# file += requests.get(url, headers=headers).content
			open(filename, "ab").write(requests.get(url, headers=headers).content)
		percentage += 100.0 / 40.0
		self.download_song_progress.setValue(int(percentage))
		self.update()
		print int(percentage)

	# open(filename, "wb").write(file)
	# del file