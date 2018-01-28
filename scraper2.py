import requests
from bs4 import BeautifulSoup


def main():
    url = 'http://theupsstorelocal.com/5635'
    response = requests.get(url)
    html = response.content
    # print(html)

    soup = BeautifulSoup(html, "html.parser")
    # print(soup.prettify())
    footer = soup.findAll("div", {"class": "footerColumn"})[
        1]
    # print(footer)

    prodAndServ = footer.findAll('h4')[0]
    # print(prodAndServ)

    for listItem in footer.findAll('li'):
        print("an item", listItem.a.get('href'))
        print("an item", listItem.a.contents[0])
        # try:
        #     for link in listItem.findall('a'):
        #         print(link)[0]
        # except:
        #     print("error")

    # 	for  in row.findAll('td'):
    # 		print row.prettify()

    # outfile = open("./upslinks.csv", "wb")
    #     writer = csv.writer(outfile)
    #     writer.writerow(
    #         ["CenterID", "CenterURL", "Subpage Name", "Subpage URL"])

if __name__ == "__main__":
    main()
