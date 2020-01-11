import sys
import re
import requests
import subprocess
from time import time, sleep
import concurrent.futures
import os
from functools import partial

headers = {
	"Referer": "https://ci.phncdn.com/www-static/css/generated-header"
	".css?cache=2019122001", "User-Agent": "Mozilla/5.0 (Windows NT 1"
	"0.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/7"
	"9.0.3945.88 Safari/537.36"}
chunkK = 64

# Accepts 
# ...xxx.mp4.urlset/index-f1-v1-a1.m3u8
# or:
# ...xxx.mp4?val...
askIcg = lambda icg: float(input('Inter-chunk gap [0.1]> ') or icg)
askUrl = lambda: input('Paste url> ')
askFilename = lambda: input('Save with prefix> ')
urlPathPrefix = lambda url: url.rpartition('/')[0]
urlToFilename = lambda url: re.search(r'/([^/]*?\.mp4)', url).group(1)
isPlayList = lambda url: '.urlset' in url
toList = lambda lst: [u for u in re.split(r'#EXT.*?,', lst) if len(u)]
askOpen = lambda fileName: 'y' == input(f'{fileName} DONE. Open? y/N> ')
maybePrint = lambda future, text, end='\n': print(text, end=end, flush=True) if future.done() else None
progressBarLength = lambda: len(progressBar(0,10**10,10**10,10**10)[0])
def progressBar(last, progress, total, increase):
	now = time()
	bar = f'{100*progress//total*"●":○<100} {progress: >13,} B of {total:,} B, {increase/(now-last): >10,.0f} B/s'
	bar = '·'.join([bar[(x-1)*10:x*10] for x in range(1, 11)]) + bar[100:]
	return bar, now
def getPlayList(printIfReady, url):
	printIfReady('Downloading parts list...')
	return requests.get(url, headers=headers).text.replace('\n','').replace('#EXT-X-ENDLIST','')
def appendPart(out, num, url, icg, printIfReady):
	retry = True
	while retry:
		downloaded=0
		try:
			response = requests.get(url, headers=headers, stream=True)
			totalLength = int(response.headers.get('content-length'))
			startedAt = time()
			for data in response.iter_content(chunkK*1024):
				downloaded+=len(data)
				out.write(data)
				pb, _ = progressBar(startedAt, downloaded, totalLength, downloaded)
				printIfReady(pb, end='\r')
				sleep(icg)
			printIfReady(f'\nFinished {downloaded:,} B.')
			break
		except Exception as exc:
			retry = 'y' == input(f'This part failed to download ({exc}). Try again? y/n')
			printIfReady(f'Downloaded {downloaded:,} B, {"retrying..." if retry == "y" else "gave up."}')

print("Get the quality_1080p url from browser console.".ljust(progressBarLength(), '_'))
icg = askIcg(0.1)
pastedUrl = askUrl()
prefix = urlPathPrefix(pastedUrl)
tempName = urlToFilename(pastedUrl)
print(f'{prefix} --> {tempName}...')
with concurrent.futures.ThreadPoolExecutor() as executor:
	nameInputter = executor.submit(askFilename)
	printIfReady = partial(maybePrint, nameInputter)
	parts = toList(getPlayList(printIfReady, pastedUrl)) if isPlayList(pastedUrl) else [pastedUrl] 
	with open(tempName, 'wb') as out:
		for num, part in enumerate(parts, start=1):
			printIfReady(f'Downloading {num: >3} of {len(parts)}: {part[:30]}... ', end=None)
			url = prefix+'/'+part if isPlayList(pastedUrl) else part
			appendPart(out, num, url, icg, printIfReady)

	newName = nameInputter.result() + ' ' + tempName
os.rename(tempName, newName)
if askOpen(newName):
	subprocess.run(['explorer', newName])
