import requests
import re
from bs4 import BeautifulSoup


class mailFinder:
	headers = {
		'User-agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'
	}


	def googleForLinks(self, query, googlePage):
		try:
			page = BeautifulSoup(requests.get('https://google.com/search?q=' + query + '&start=' + str(googlePage * 10), headers=self.headers, timeout=10).text, "lxml")
		except:
			return []

		websites = []

		for result in page.select('.tF2Cxc'):
			websites.append(result.select_one('.yuRUbf a')['href'])
		
		return websites


	def collectMailAdresses(self, link):
		page = BeautifulSoup(requests.get(link, headers=self.headers).text, "lxml")
		mailAdresses = []
		regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

		for potentialAdress in page.find_all(href=True):
			potentialAdress = potentialAdress['href'].replace('mailto:', '')

			try:
				if (potentialAdress != 'None' and re.fullmatch(regex, potentialAdress)):
					mailAdresses.append(potentialAdress)
			except:
				pass

		return mailAdresses

query = input('Google query: ')
pageLimit = input('MAX amount of Google pages: ')
_mailFinder = mailFinder()
results = []
print('\n')


for pageCounter in range(int(pageLimit)):
	links = _mailFinder.googleForLinks(query=query, googlePage=pageCounter)

	for link in links:
		collectedMailAdresses = _mailFinder.collectMailAdresses(link=link)
		results.extend(x for x in collectedMailAdresses if x not in results)
		print('Page ' + str(pageCounter + 1) + ' | Found ' + str(len(results)) + ' adresses', end="\r")


print('\n\n')
for result in results:
	print(result)