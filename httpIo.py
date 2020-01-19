chunkK = 64
icg = 0.3

headers = {
	"Referer": "https://ci.phncdn.com/www-static/css/generated-header"
	".css?cache=2019122001", "User-Agent": "Mozilla/5.0 (Windows NT 1"
	"0.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/7"
	"9.0.3945.88 Safari/537.36"}

from time import time, sleep
from requests import get as rGet

def getPlayList(printIfReady, url):
	printIfReady('Downloading parts list...')
	return rGet(url, headers=headers).text.replace('\n','').replace('#EXT-X-ENDLIST','')
def appendPart(out, num, url, console):
	global chunkK, icg
	retry = True
	while retry:
		downloaded=0
		try:
			response = rGet(url, headers=headers, stream=True)
			totalLength = int(response.headers.get('content-length'))
			startedAt = time()
			for data in response.iter_content(chunkK*1024):
				downloaded+=len(data)
				out.write(data)
				slowMode = isSlow(startedAt, downloaded)
				pb = console.pBar(startedAt, downloaded, totalLength, Bps(downloaded, startedAt))
				console.markSlow(pb, slowMode)
				sleep(icg if slowMode else 0)
			console.sayFinished(downloaded)
			break
		except Exception as exc:
			retry = 'y' == console.askRetry(exc)
			console.sayRetry(downloaded, retry)

isSlow = lambda startedAt, downloaded: downloaded/(time()-startedAt)<10**5 
Bps = lambda delta, lastTime: delta/(time()-lastTime)