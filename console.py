introduce = lambda: print('Paste the web page url below'.ljust(pBarLen(), '_'))
askUrl = lambda: input('Paste url> ')
askFilename = lambda: input('Save with prefix> ')
sayDlLocation = lambda prefix, tempName: print(f'{prefix} --> {tempName}...')
sayTitle = lambda title: print(title)
sayPartsList = lambda: print('Downloading parts list...')
sayPartDl = lambda num, parts, part: print(f'Downloading {num: >3} of {len(parts)}: {part[:80]}... ', end=None)
askOpen = lambda fileName: 'y' == input(f'{fileName} DONE. Open? y/N> ')

pBarLen = lambda: len(pBar(0,10**10,10**10,10**10))
def pBar(last, progress, total, Bps):
	bar = f'{100*progress//total*"●":○<100} {progress: >13,} B of {total:,} B, {Bps: >10,.0f} B/s'
	bar = '·'.join([bar[(x-1)*10:x*10] for x in range(1, 11)]) + bar[100:]
	return bar

markSlow = lambda pb, slowMode: print(pb+(' *slow*' if slowMode else '       '), end='\r')
sayFinished = lambda downloaded: print(f'\nFinished {downloaded:,} B.')
askRetry = lambda exc: input(f'This part failed to download ({exc}). Try again? y/n')
sayRetry = lambda downloaded, retry: print(f'Downloaded {downloaded:,} B, {"retrying..." if retry == "y" else "gave up."}')
