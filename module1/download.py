'''
https://selenium-python.readthedocs.io/getting-started.html#simple-usage

chromedriver.exe:
https://sites.google.com/a/chromium.org/chromedriver/home
'''
from selenium import webdriver
import re
import sys, os

qualities = lambda: ['quality_1080p','quality_720p','quality_480p','quality_360p','quality_240p']
qualityUrl = lambda driver, variable: driver.execute_script(f'return typeof({variable}) !== "undefined" ? {variable} : ""') 
serverPath = lambda url: url.rpartition('/')[0]
urlToFilename = lambda url: re.search(r'/([^/]*?\.mp4)', url).group(1)

# Goal: to accept urls like 
# 	...xxx.mp4.urlset/index-f1-v1-a1.m3u8
# or:
# 	...xxx.mp4?val...
def urlAndTitle(pageUrl):
	options = webdriver.ChromeOptions()
	options.add_argument('--window-size=100,100')
	# options to prevent printing "DevTools listening on ..."
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome('./bin/chromedriver.exe', options=options)
	driver.get(pageUrl.partition('&')[0])
	
	videoUrls = [url for url in [
			qualityUrl(driver, qualityName) for qualityName in qualities()
		] if url]
	title = driver.title
	driver.close()
	if len(videoUrls):
		return videoUrls[0], title, ''
	else:
		return '', '', title

def download(http, console, config, isPlayList, serverFileName, partsList, serverPath):
	with open(serverFileName, 'wb') as file:
		for partNum, partUrl in enumerate(partsList, start=1):
			console.sayPartDl(partNum, partsList, partUrl)
			fullUrl = f'{serverPath}/{partUrl}' if isPlayList else partUrl
			http.downloadPart(config['headers'], file, partNum, fullUrl, console)

