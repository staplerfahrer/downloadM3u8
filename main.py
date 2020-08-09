import console
import fileIo
from getDlUrl import urlAndTitle
import httpIo as http

import json
import os
from os import rename
from subprocess import run

# Accepts 
# ...xxx.mp4.urlset/index-f1-v1-a1.m3u8
# or:
# ...xxx.mp4?val...
def main():
	config = loadConfig('config.json')
	console.introduce()
	pastedUrl, videoTitle, error = urlAndTitle(console.getClipboardUrl(config['matchDomain']))
	if not pastedUrl:
		console.sayError(error)
		return

	safeTitle = fileIo.safeFilename(videoTitle)
	serverFileName = http.urlToFilename(pastedUrl)
	newName = safeTitle + ' ' + serverFileName
	if os.path.exists(newName):
		console.sayError(f'File already exists: {newName}')
		return

	prefix = http.urlPathPrefix(pastedUrl)
	console.sayDlLocation(prefix, serverFileName)
	console.sayTitle(safeTitle)

	isPlayList = http.isPlayList(pastedUrl)
	partsList = http.toList(http.getPlayList(config['headers'], console, pastedUrl)) if isPlayList else [pastedUrl] 

	with open(serverFileName, 'wb') as file:
		for partNum, partUrl in enumerate(partsList, start=1):
			console.sayPartDl(partNum, partsList, partUrl)
			fullUrl = prefix+'/'+partUrl if isPlayList else partUrl
			http.downloadPart(config['headers'], file, partNum, fullUrl, console)

	rename(serverFileName, newName)
	if console.askOpen(newName):
		run(['explorer', newName])
	console.finish()

def loadConfig(filename):
	with open(filename, 'r') as config:
		return json.load(config)

if __name__ == "__main__":
	if (__file__):
		newDir = os.path.dirname(os.path.realpath(__file__))
		os.chdir(newDir)
	console.startup(os.path.realpath(os.path.curdir))
	while True:
		main()