import pandas as pd
import numpy as np
import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from xvfbwrapper import Xvfb


master = pd.DataFrame()
N = 20 #number of pages to crawl --> max 20 :(
for k in range(1, N+1):
	print(k, 'out of:', N)
	url2 = 'https://www.trulia.com/NY/New_York/' + str(k) + '_p/'

	#hide browser popup
	display = Xvfb()
	display.start()

	driver = webdriver.Firefox()
	driver.get(url2)


	properties = WebDriverWait(driver, 15).until(EC.visibility_of_all_elements_located(('xpath', "//*[@class='Box__BoxElement-sc-1f5rw0h-0 fEsbLJ PropertyCard__PropertyCardContainer-m1ur0x-4 kYIQmo']")))


	lst = []
	links = []
	for i, value in enumerate(properties):
		lst.append(value.text)
		links.append(value.find_elements("xpath", "//*[@class='PropertyCard__StyledLink-m1ur0x-3 fiWGOD']")[i].get_attribute('href'))


	#REGEX
	string_col = []
	price_col = []
	bed_col = []
	bath_col = []
	feet_col = []
	add_col = []
	new_col = []
	company_col = []



	for g, value in enumerate(lst):
		string_col.append(value)
		price_col.append(re.sub('\D+', '', value.split('$')[1].splitlines()[0]))
		#bed_col.append(re.sub('[A-Za-z]', '', value.split('$')[1].splitlines()[1]))
		#bath_col.append(re.sub('[A-Za-z]', '', value.split('$')[1].splitlines()[2]))
		#feet_col.append(re.sub(',', '', re.sub(' sqft.*', '', value.split('$')[1].splitlines()[3])))
		add_col.append(''.join(value.split('$')[1].splitlines()[-3:-1]))
		new_col.append(bool(re.search('new', ''.join(value.split('$')[0].splitlines()).lower())))
		company_col.append(value.split('$')[1].splitlines()[-1][12:])

		if (value.split('$')[1].splitlines()[1]).lower() == 'studio':
			bed_col.append('0')
		elif (bool(re.search('bd', value.split('$')[1].splitlines()[1]))) == True:
			bed_col.append(re.sub('[A-Za-z]', '', value.split('$')[1].splitlines()[1]))
		else:
			bed_col.append(np.NaN)

		if (bool(re.search('ba', value.split('$')[1].splitlines()[2]))) == True:
			bath_col.append(re.sub('[A-Za-z]', '', value.split('$')[1].splitlines()[2]))
		else:
			bath_col.append(np.NaN)

		temp = [ i for i, word in enumerate(value.split('$')[1].splitlines()) if re.search('sqft', word.lower()) ]
		if len(temp) == 0:
			feet_col.append(np.NaN)
		else:
			feet_col.append(re.sub(',', '', re.sub(' sqft.*', '', value.split('$')[1].splitlines()[temp[0]])))





	df = pd.DataFrame({'price': price_col, 'bed': bed_col, 'bath': bath_col, 'feet': feet_col, 'address': add_col, 'new_flag': new_col, 'link': links, 'company': company_col , 'original_str': string_col})

	#master = pd.concat([master, df], axis=0)
	master = master.append(df)



	driver.quit()

	display.stop()


import datetime
today = datetime.datetime.today().strftime('%Y-%m-%d')
master.to_csv('NY_realestate' + str(today) + '.csv', index = True)






#######OLD

		#print(i.content)
		# try:
		# 	price_col.append(i.find_element('xpath', "//*[@class='Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 enhvQK iilDhj']").text)
		# except:
		# 	price_col.append(np.NaN)
		# try:
		# 	bed_col.append(i.find_element('xpath', "//*[@class='Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 csrRqu gUnlde' and @data-testid='property-beds']").text)
		# except:
		# 	bed_col.append(np.NaN)
		# try:
		# 	bath_col.append(i.find_element('xpath', "//*[@class='Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 csrRqu gUnlde' and @data-testid='property-baths']").text)
		# except:
		# 	bath_col.append(np.NaN)
		# try:
		# 	feet_col.append(i.find_element('xpath', "//*[@class='Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 csrRqu iilDhj' and @data-testid='property-floorSpace']").text)
		# except:
		# 	feet_col.append(np.NaN)
		# try:
		# 	add_col.append(i.find_element('xpath', "//*[@class='Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 csrRqu iilDhj' and @data-testid='property-address']").text)
		# except:
		# 	add_col.append(np.NaN)
		# try:
		# 	link_col.append(i.find_element('xpath', "//*[@class='PropertyCard__StyledLink-m1ur0x-3 fiWGOD']").get_attribute('href'))
		# except:
		# 	link_col.append(np.NaN)




	#prices = WebDriverWait(driver, 15).until(EC.visibility_of_all_elements_located(('xpath', "//*[@class='Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 enhvQK iilDhj']")))
	#beds = WebDriverWait(driver, 15).until(EC.visibility_of_all_elements_located(('xpath', "//*[@class='Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 csrRqu gUnlde' and @data-testid='property-beds']")))
	#baths = WebDriverWait(driver, 15).until(EC.visibility_of_all_elements_located(('xpath', "//*[@class='Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 csrRqu gUnlde' and @data-testid='property-baths']")))
	#feet = WebDriverWait(driver, 15).until(EC.visibility_of_all_elements_located(('xpath', "//*[@class='Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 csrRqu iilDhj' and @data-testid='property-floorSpace']")))
	#addresses = WebDriverWait(driver, 15).until(EC.visibility_of_all_elements_located(('xpath', "//*[@class='Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 csrRqu iilDhj' and @data-testid='property-address']")))
	#links = WebDriverWait(driver, 15).until(EC.visibility_of_all_elements_located(('xpath', "//*[@class='PropertyCard__StyledLink-m1ur0x-3 fiWGOD']")))




	#
	# price_col = []
	# for i in prices:
	# 	price_col.append(i.text)
	#
	# bed_col = []
	# for i in beds:
	# 	bed_col.append(i.text)
	#
	# bath_col = []
	# for i in baths:
	# 	bath_col.append(i.text)
	#
	# feet_col = []
	# for i in feet:
	# 	feet_col.append(i.text)
	#
	# add_col = []
	# for i in addresses:
	# 	add_col.append(i.text)
	#
	# link_col = []
	# for i in links:
	# 	link_col.append(i.get_attribute('href'))
	#
