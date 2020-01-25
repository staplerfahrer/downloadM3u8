from getDlUrl import urlAndTitle
import console
import httpIo as http
import fileIo

# Accepts 
# ...xxx.mp4.urlset/index-f1-v1-a1.m3u8
# or:
# ...xxx.mp4?val...
console.introduce()
pastedUrl, videoTitle = urlAndTitle(console.askUrl())
safeTitle = fileIo.safeFilename(videoTitle)

prefix = http.urlPathPrefix(pastedUrl)
serverFileName = http.urlToFilename(pastedUrl)

console.sayDlLocation(prefix, serverFileName)
console.sayTitle(safeTitle)

isPlayList = http.isPlayList(pastedUrl)
partsList = http.toList(http.getPlayList(console, pastedUrl)) if isPlayList else [pastedUrl] 

with open(serverFileName, 'wb') as file:
	for partNum, partUrl in enumerate(partsList, start=1):
		console.sayPartDl(partNum, partsList, partUrl)
		fullUrl = prefix+'/'+partUrl if isPlayList else partUrl
		bytesGot = http.downloadPart(file, partNum, fullUrl, console)

newName = safeTitle + ' ' + serverFileName

from os import rename
from subprocess import run
rename(serverFileName, newName)
if console.askOpen(newName):
	run(['explorer', newName])
console.finish()