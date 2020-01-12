from selenium import webdriver
from time import time
'''
https://selenium-python.readthedocs.io/getting-started.html#simple-usage

chromedriver.exe:
https://sites.google.com/a/chromium.org/chromedriver/home
'''

def urlAndTitle(pageUrl):
	start = time()
	driver = webdriver.Chrome('./bin/chromedriver.exe')
	driver.set_window_size(100,100)
	#driver.minimize_window()#this seems slower...
	driver.get(pageUrl.partition('&')[0])
	
	qualityUrl = lambda variable: driver.execute_script(f'return typeof({variable}) !== "undefined" ? {variable} : ""') 
	qualities = ['quality_1080p','quality_720p','quality_480p','quality_360p','quality_240p']
	detected = [u for u in [qualityUrl(q) for q in qualities] if u]
	fromH1 = driver.find_element_by_xpath('//h1[@class="title"]/span').text
	title = ''.join(c for c in (fromH1 if fromH1 else driver.title).casefold() if c in 'abcdefghijklmnopqrstuvwxyz1234567890- ,')
	driver.close()
	print(f'Took {time()-start:.2f} s.')
	return detected[0], title

if __name__ == "__main__":
	print(urlAndTitle(input('paste url> ')))
	input('...')