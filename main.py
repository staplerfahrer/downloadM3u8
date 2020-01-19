import sys, os
import re
import subprocess
from getDlUrl import urlAndTitle
import console
import httpIo as http


# Accepts 
# ...xxx.mp4.urlset/index-f1-v1-a1.m3u8
# or:
# ...xxx.mp4?val...
urlPathPrefix = lambda url: url.rpartition('/')[0]
urlToFilename = lambda url: re.search(r'/([^/]*?\.mp4)', url).group(1)
isPlayList = lambda url: '.urlset' in url
toList = lambda lst: [u for u in re.split(r'#EXT.*?,', lst) if len(u)]
maybePrint = lambda future,text,end='\n': print(text,end=end,flush=True) if future.done() else None

console.introduce()
pastedUrl, title = urlAndTitle(console.askUrl())
prefix = urlPathPrefix(pastedUrl)
tempName = urlToFilename(pastedUrl)
print(f'{prefix} --> {tempName}...')
print(title)

printIfReady = print
parts = toList(http.getPlayList(printIfReady, pastedUrl)) if isPlayList(pastedUrl) else [pastedUrl] 
with open(tempName, 'wb') as out:
	for num, part in enumerate(parts, start=1):
		printIfReady(f'Downloading {num: >3} of {len(parts)}: {part[:80]}... ', end=None)
		url = prefix+'/'+part if isPlayList(pastedUrl) else part
		http.appendPart(out, num, url, console)

newName = title + ' ' + tempName

os.rename(tempName, newName)
if console.askOpen(newName):
	subprocess.run(['explorer', newName])
