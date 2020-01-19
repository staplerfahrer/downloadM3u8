from getDlUrl import urlAndTitle
import console
import httpIo as http

# Accepts 
# ...xxx.mp4.urlset/index-f1-v1-a1.m3u8
# or:
# ...xxx.mp4?val...
console.introduce()
pastedUrl, videoTitle = urlAndTitle(console.askUrl())

prefix = http.urlPathPrefix(pastedUrl)
serverFileName = http.urlToFilename(pastedUrl)

console.sayDlLocation(prefix, serverFileName)
console.sayTitle(videoTitle)

isPlayList = http.isPlayList(pastedUrl)
parts = http.toList(http.getPlayList(console, pastedUrl)) if isPlayList else [pastedUrl] 

with open(serverFileName, 'wb') as file:
	for num, part in enumerate(parts, start=1):
		console.sayPartDl(num, parts, part)
		url = prefix+'/'+part if isPlayList else part
		http.appendPart(file, num, url, console)

newName = videoTitle + ' ' + serverFileName

from os import rename
from subprocess import run
rename(serverFileName, newName)
if console.askOpen(newName):
	run(['explorer', newName])
