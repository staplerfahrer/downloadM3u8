import math
import clipboard
from time import sleep

introduce = lambda: print('Auto-download resource from web page URL'.ljust(pBarLen(), '_'))
askUrl = lambda: input('Paste the page URL> ')
# askFilename = lambda: input('Save with prefix> ')
sayError = lambda error: print(f'Failed to get information: ({error}).')
sayDlLocation = lambda prefix, tempName: print(f'Downloading from [{prefix}] to temporary file [{tempName}]...')
sayTitle = lambda title: print(f'Resource title [{title}]')
sayPartsList = lambda: print('Downloading m3u8 playlist...')
sayPartDl = lambda num, parts, part: print(f'Downloading part {num: >3} of {len(parts)}: {part[:80]}...', end=None)
askOpen = lambda fileName: 'y' == input(f'Finished downloading [{fileName}]. Open? y/N> ')

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

def getClipboardUrl():
	while True:
		txt = clipboard.getClipboardText()
		if txt and txt[:8] == 'https://':
			clipboard.emptyClipBoard()
			return txt
		sleep(0.1)