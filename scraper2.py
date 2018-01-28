import requests
from BeautifulSoup import BeautifulSoup

def main ():
	url = 'https://theupsstorelocal.com'
	response = requests.get(url)
	html = response.content
	print html

	soup = BeautifulSoup(html)
	print soup.prettify()
	# table = soup.find('tbody', attrs={'class': 'stripe'})
	# for row in table.findAll('tr'):
	# 	for cell in row.findAll('td'):
	# 		print row.prettify()

if __name__ == "__main__": main()