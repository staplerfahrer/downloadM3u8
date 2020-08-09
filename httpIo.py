from time import time, sleep
from requests import get as rGet
import re

chunkK = 64
slowLimit = 2*10**5
icg = 0.3

def getM3u8PlayList(headers, console, url):
	console.sayPartsList()
	return rGet(url, headers=headers).text.replace('\n','').replace('#EXT-X-ENDLIST','')

def downloadPart(headers, file, num, url, console):
	global chunkK, icg
	retry = True
	bytesGot = 0
	while retry:
		bytesGot = 0
		try:
			response = rGet(url, headers=headers, stream=True)
			totalLength = int(response.headers.get('content-length'))
			startedAt = time()
			for data in response.iter_content(chunkK*1024):
				bytesGot+=len(data)
				file.write(data)
				slowStatus = isSlow(startedAt, bytesGot)
				pb = console.pBar(startedAt, bytesGot, totalLength, Bps(bytesGot, startedAt))
				console.markSlow(pb, slowStatus)
				# allow traffic for other applications
				# if the connection is slow
				sleep(icg if slowStatus else 0)
			break
		except Exception as exc:
			retry = 'y' == console.askRetry(exc)
			console.sayRetry(bytesGot, retry)
	console.sayFinished(bytesGot, totalLength)
	return bytesGot

isSlow = lambda startedAt, downloaded: Bps(downloaded, startedAt)<slowLimit 
Bps = lambda delta, lastTime: delta/(time()-lastTime)

isPlayList = lambda url: '.urlset' in url
toList = lambda lst: [u for u in re.split(r'#EXT.*?,', lst) if len(u)]
