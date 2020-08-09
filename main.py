import console
import fileIo
import httpIo as http
import module1.download as mod1

import json
from os import path, remove, rename
from subprocess import run

def main():
	config = loadConfig('config.json')
	console.introduce()
	discoveredUrl, videoTitle, error = mod1.urlAndTitle(
			console.getClipboardUrl(config['matchDomain']))
	if error:
		console.sayError(error)
		return

	safeTitle = fileIo.safeFilename(videoTitle)
	serverFileName = mod1.serverFilename(discoveredUrl)
	newName = f'{safeTitle} {serverFileName}'
	if path.exists(newName):
		console.sayError(f'file already exists: {newName}')
		return

	serverPath = mod1.serverPath(discoveredUrl)
	console.sayDlLocation(serverPath, serverFileName)
	console.sayTitle(safeTitle)

	try:
		mod1.download(http, console, config, discoveredUrl)
	except KeyboardInterrupt as _:
		remove(serverFileName)
		console.sayError('download aborted & removed')
		console.finish()
		return

	rename(serverFileName, newName)

	if console.askOpen(newName):
		run(['explorer', newName])

	console.finish()

def loadConfig(filename):
	with open(filename, 'r') as config:
		return json.load(config)

if __name__ == '__main__':
	fileIo.changePathToHere(__file__)
	console.startup(path.realpath(path.curdir))
	while True:
		try:
			main()
		except KeyboardInterrupt as _:
			console.finish()
			exit()