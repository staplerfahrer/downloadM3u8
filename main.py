import json
from os import path, remove, rename
from subprocess import run

import console
import fileIo
import httpIo as http

def main(module):
	config = loadConfig('config.json')
	console.introduce()
	url = console.waitFor('Waiting for URL', console.getClipboardUrl, config['matchDomain'])
	discoveredUrl, videoTitle, error = console.waitFor('Discovering', module.urlAndTitle, url)
	if error:
		console.sayError(error)
		return

	safeTitle = fileIo.safeFilename(videoTitle)
	serverFileName = module.serverFilename(discoveredUrl)
	newName = f'{safeTitle} {serverFileName}'
	if path.exists(newName):
		console.sayError(f'file already exists: {newName}')
		return

	serverPath = module.serverPath(discoveredUrl)
	console.sayDlLocation(serverPath, serverFileName)
	console.sayTitle(safeTitle)

	try:
		module.download(http, console, config, discoveredUrl)
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
			import module1.download as currentModule
			main(currentModule)
		except KeyboardInterrupt as _:
			console.finish()
			exit()
