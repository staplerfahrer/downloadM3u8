from selenium import webdriver
'''
https://selenium-python.readthedocs.io/getting-started.html#simple-usage

chromedriver.exe:
https://sites.google.com/a/chromium.org/chromedriver/home
'''

def urlAndTitle(pageUrl):
	driver = webdriver.Chrome('./bin/chromedriver.exe')
	driver.get(pageUrl.partition('&')[0])
	qualityUrl = lambda variable: driver.execute_script(f'return typeof({variable}) !== "undefined" ? {variable} : ""') 
	qualities = ['quality_1080p','quality_720p','quality_480p','quality_360p','quality_240p']
	detected = [u for u in [qualityUrl(q) for q in qualities] if u]
	title = ''.join(c for c in driver.find_element_by_xpath('//h1[@class="title"]/span').text.casefold() if c in 'abcdefghijklmnopqrstuvwxyz1234567890- ,')
	driver.close()
	return detected[0], title

if __name__ == "__main__":
	print(urlAndTitle(input('paste url> ')))
	input('...')