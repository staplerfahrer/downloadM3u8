import sys
import re
import requests
import subprocess
from time import time, sleep
import concurrent.futures
import os
from functools import partial

# ...xxx.mp4.urlset/index-f1-v1-a1.m3u8
# or:
# ...xxx.mp4?val...
askUrl = lambda: input('Paste url> ')
askFilename = lambda: input('Save with prefix> ')
urlPathPrefix = lambda url: url.rpartition('/')[0]
urlToFilename = lambda url: re.search(r'/([^/]*?\.mp4)', url).group(1)
isPlayList = lambda url: '.urlset' in url
toList = lambda lst: [u for u in re.split(r'#EXT.*?,', lst) if len(u)]
askOpen = lambda fileName: 'y' == input(f'{fileName} DONE. Open? y/n> ')
maybePrint = lambda future, text, end='\n': print(text, end=end, flush=True) if future.done() else None
def pbf(last, progress, total, increase):
	now = time()
	pb = f'{100*progress//total*"●":○<100} {progress: >13,} B of {total:,} B   {increase/(now-last): >10,.0f} B/s{" "*20}'
	pb = '·'.join([pb[(x-1)*10:x*10] for x in range(1, 11)]) + pb[100:]
	return pb, now

def getPlayList(printIfReady, url):
	printIfReady('Downloading parts list...')
	return requests.get(url).text.replace('\n','').replace('#EXT-X-ENDLIST','')
def appendPart(out, num, url, printIfReady):
	chunkK = 64
	retry = True
	while retry:
		downloaded=0
		try:
			response = requests.get(url, stream=True)
			totalLength = int(response.headers.get('content-length'))
			last = time()
			for data in response.iter_content(chunkK*1024):
				downloaded+=len(data)
				out.write(data)
				pb, last = pbf(last, downloaded, totalLength, len(data))
				printIfReady(pb, end='\r')
				sleep(0.1)
			printIfReady(f'\nFinished {downloaded:,} B.')
			break
		except Exception as exc:
			retry = 'y' == input(f'This part failed to download ({exc}). Try again? y/n')
			printIfReady(f'Downloaded {downloaded:,} B, {"retrying..." if retry == "y" else "gave up."}')


with concurrent.futures.ThreadPoolExecutor() as executor:
	print('Get the quality_1080p url from browser console.')
	pastedUrl = askUrl()
	prefix = urlPathPrefix(pastedUrl)
	tempName = urlToFilename(pastedUrl)
	print(f'{prefix} --> {tempName}...')
	nameInputter = executor.submit(askFilename)
	printIfReady = partial(maybePrint, nameInputter)
	parts = toList(getPlayList(printIfReady, pastedUrl)) if isPlayList(pastedUrl) else [pastedUrl] 

	with open(tempName, 'wb') as out:
		for num, part in enumerate(parts, start=1):
			printIfReady(f'Downloading {num: >3} of {len(parts)}: {part[:30]}... ', end=None)
			url = prefix+'/'+part if isPlayList(pastedUrl) else part
			appendPart(out, num, url, printIfReady)

	newName = nameInputter.result() + ' ' + tempName
	os.rename(tempName, newName)
	if askOpen(newName):
		subprocess.run(['explorer', newName])
