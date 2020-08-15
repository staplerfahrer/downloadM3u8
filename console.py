import math
import clipboard
from time import sleep

startup = lambda cwd: print(f'Current working directory: {cwd}')
introduce = lambda: print('Auto-download resource from web page URL'.ljust(pBarLen(), '_'))
sayError = lambda error: print(f'\nSomething\'s happened: {error}\n')
sayClipboard = lambda clp: print(f'New clipboard text: {clp}')
sayCapture = lambda clp: print(f'Analyzing URL: {clp}')
sayDlLocation = lambda prefix, tempName: print(f'Downloading from [{prefix}] to temporary file [{tempName}]...')
sayTitle = lambda title: print(f'Resource title [{title}]')
sayPartsList = lambda: print('Downloading m3u8 playlist...')
sayPartDl = lambda num, parts, part: print(f'Downloading part {num: >3} of {len(parts)}: {part[:80]}...', end=None)
askOpen = lambda fileName: 'y' == input(f'Finished downloading [{fileName}].\nOpen? y/N> ')

pBarLen = lambda: len(pBar(0,10**10,10**10,10**10))
def pBar(last, progress, total, Bps):
	bar = f'{100*progress//total*"●":○<100} {progress: >13,} B of {total:,} B, {Bps: >10,.0f} B/s'
	bar = '·'.join([bar[(x-1)*10:x*10] for x in range(1, 11)]) + bar[100:]
	return bar

markSlow = lambda pb, slowMode: print(pb+(' *slow*' if slowMode else '       '), end='\r')
sayFinished = lambda downloaded, ofTotal: print(f'\nFinished this part, {downloaded:,} B of {ofTotal:,} B ({math.floor(downloaded*100/ofTotal):.0f} %).')
askRetry = lambda exc: input(f'This part failed to download ({exc}). Try again? y/n')
sayRetry = lambda downloaded, retry: print(f'Downloaded {downloaded:,} B, {"retrying..." if retry == "y" else "gave up."}')
finish = lambda: print('_'*pBarLen())
isMatch = lambda domain, url: url and url[:8] == 'https://' and domain in url

def getClipboardUrl(matchDomain):
	clp = ''
	while True:
		sleep(0.1)
		if clipboard.getClipboardText() == clp:
			continue
		clp = clipboard.getClipboardText()
		sayClipboard(clp)
		if isMatch(matchDomain, clp):
			clipboard.emptyClipBoard()
			return clp