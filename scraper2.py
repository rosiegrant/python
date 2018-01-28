import requests
from bs4 import BeautifulSoup


def main():
    url = 'http://theupsstorelocal.com/5635'
    response = requests.get(url)
    html = response.content
    # print(html)

    soup = BeautifulSoup(html, "html.parser")
    print(soup.prettify())
    footer = soup.findAll("div", {"class": "footerColumn"})[
        1]
    print(footer)

    # footer = soup.find("footerColumn")[1]
    # for row in table.findAll('tr'):
    # 	for cell in row.findAll('td'):
    # 		print row.prettify()

    # outfile = open("./upslinks.csv", "wb")
    #     writer = csv.writer(outfile)
    #     writer.writerow(
    #         ["CenterID", "CenterURL", "Subpage Name", "Subpage URL"])

if __name__ == "__main__":
    main()
