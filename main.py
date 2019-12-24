import sys
import re
import requests
import subprocess
from time import time
import threading

# ...xxx.mp4.urlset/index-f1-v1-a1.m3u8
# or:
# ...xxx.mp4?val...
askUrl = lambda: input('Paste url > ')
askFilename = lambda: input('Save as  > ')
urlPathPrefix = lambda url: url.rpartition('/')[0]
formatFilename = lambda saveAs, partsListUrl: saveAs + re.search(r'/([^/]*?\.mp4)', partsListUrl).group(1)
isPlayList = lambda url: '.urlset' in url
toList = lambda lst: [u for u in re.split(r'#EXT.*?,', lst) if len(u)]
askOpen = lambda: 'y' == input(f'{fileName} DONE. Open? y/n > ')
def getPlayList(url):
	print('Downloading parts list...')
	return requests.get(url).text.replace('\n','').replace('#EXT-X-ENDLIST','')
def appendPart(out, num, url):
	retry = True
	while retry:
		try:
			response = requests.get(url, stream=True)
			totalLength = int(response.headers.get('content-length'))
			print(f'part size: {totalLength:,} B')
			downloaded=0
			print(100*'.', end='\r', flush=True)
			last = time()
			for data in response.iter_content(1024*1024):
				downloaded+=len(data)
				out.write(data)
				print(f'{100*downloaded//totalLength*"#":.<100} {downloaded: >13,} B   {len(data)/(time()-last): >10,.0f} B/s{" "*20}', end='\r', flush=True)
				last = time()
			print(100*'#', flush=True)
			break
		except Exception as exc:
			retry = 'y' == input(f'This part failed to download ({exc}). Try again? y/n')

print('Get the quality_1080p url from browser console.')
pastedUrl = askUrl()
saveAs = askFilename()
prefix = urlPathPrefix(pastedUrl)
fileName = formatFilename(saveAs, pastedUrl)
print(f'{prefix} --> {fileName}...')
parts = toList(getPlayList(pastedUrl)) if isPlayList(pastedUrl) else [pastedUrl] 

with open(fileName, 'wb') as out:
	for num, part in enumerate(parts, start=1):
		print(f'Downloading {num: >3} of {len(parts)}: {part[:30]}... ', end='')
		url = prefix+'/'+part if isPlayList(pastedUrl) else part
		appendPart(out, num, url)

if askOpen():
        subprocess.run(['explorer', fileName])
