import csv
import requests
from bs4 import BeautifulSoup
import sys


def main():
    url = 'http://theupsstorelocal.com/5635'

    for line in open(sys.argv[1]):
        row = line.split(',')  # returns a list ["1","50","60"]
        CenterID = row[0]
        pageURL = row[1]

    response = requests.get(pageURL)
    html = response.content
    # print(html)

    soup = BeautifulSoup(html, "html.parser")
    # print(soup.prettify())
    footer = soup.findAll("div", {"class": "footerColumn"})[
        1]
    # print(footer)

    prod_services = footer.findAll('h4')[0]
    # print(prodAndServ)

    all_rows = []
    first_row = []
    first_row.append(prod_services.a.contents[0]), first_row.append(
        prod_services.a.get('href'))
    all_rows.append(first_row)  # well this is dumb

    for listItem in footer.findAll('li'):
        this_row = []
        this_row.append(listItem.a.contents[0])
        this_row.append(listItem.a.get('href'))
        # print("an item", listItem.a.get('href'))
        # print("an item", listItem.a.contents[0])
        all_rows.append(this_row)

    outfile = open("./upslinks.csv", "w")
    writer = csv.writer(outfile)
    writer.writerow(["CenterID", "CenterURL", "Subpage Name", "Subpage URL"])
    writer.writerows(all_rows)


if __name__ == "__main__":
    main()
