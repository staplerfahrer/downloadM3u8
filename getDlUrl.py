'''
https://selenium-python.readthedocs.io/getting-started.html#simple-usage

chromedriver.exe:
https://sites.google.com/a/chromium.org/chromedriver/home
'''
from selenium import webdriver
import sys, os

def urlAndTitle(pageUrl):
	# options to prevent printing "DevTools listening on ..."
	options = webdriver.ChromeOptions()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome('./bin/chromedriver.exe', options=options)
	driver.set_window_size(100,100)
	driver.get(pageUrl.partition('&')[0])
	
	detected = [u for u in [qualityUrl(driver, q) for q in qualities()] if u]
	title = ''.join(c for c in (driver.title).casefold() if c in safeFilenameChars())
	driver.close()
	return detected[0], title

qualities = lambda: ['quality_1080p','quality_720p','quality_480p','quality_360p','quality_240p']
safeFilenameChars = lambda: 'abcdefghijklmnopqrstuvwxyz1234567890- ,'
qualityUrl = lambda driver, variable: driver.execute_script(f'return typeof({variable}) !== "undefined" ? {variable} : ""') 

if __name__ == "__main__":
	print(urlAndTitle(input('paste url> ')))
	input('...')