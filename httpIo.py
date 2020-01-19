from time import time, sleep
from requests import get as rGet
import re, json

chunkK = 64
icg = 0.3
def loadHeaders(filename):
	with open(filename, 'r') as headers:
		return json.load(headers)
headers = loadHeaders('headers.json')

def getPlayList(console, url):
	console.sayPartsList()
	return rGet(url, headers=headers).text.replace('\n','').replace('#EXT-X-ENDLIST','')
def appendPart(file, num, url, console):
	global chunkK, icg, headers
	retry = True
	while retry:
		bytesGot=0
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
				sleep(icg if slowStatus else 0)
			console.sayFinished(bytesGot)
			break
		except Exception as exc:
			retry = 'y' == console.askRetry(exc)
			console.sayRetry(bytesGot, retry)

isSlow = lambda startedAt, downloaded: Bps(downloaded, startedAt)<10**5 
Bps = lambda delta, lastTime: delta/(time()-lastTime)

urlPathPrefix = lambda url: url.rpartition('/')[0]
urlToFilename = lambda url: re.search(r'/([^/]*?\.mp4)', url).group(1)
isPlayList = lambda url: '.urlset' in url
toList = lambda lst: [u for u in re.split(r'#EXT.*?,', lst) if len(u)]
