import csv
import requests
from bs4 import BeautifulSoup
import sys


def main():

    # prepare output file
    outfile = open("./upslinks.csv", "w")
    writer = csv.writer(outfile)
    writer.writerow(
        ["CenterID", "CenterURL", "Subpage Name", "Subpage URL"])  # first row, of headers

    # iterate through URLs, from file that's taken in via the command line
    infile = open(sys.argv[1])
    infile.readline()  # throw out the first line with headers

    for line in infile:

        row = line.split(',')
        centerID = row[0]
        pageURL = row[1].replace("\n", "")

        print("processing store ", centerID)

        all_rows = soupStuff(centerID, pageURL)  # do the beautiful soup things
        writer.writerows(all_rows)  # write data to outfile

    outfile.close()


def soupStuff(centerID, pageURL):

    response = requests.get(pageURL)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    # print(soup.prettify())
    footerA = soup.findAll("div", {"class": "footerColumn"})
    if (len(footerA) > 3):
        print("Number of footer elements higher than expected for store ",
              centerID)  # this store doesn't match the pattern
    footer = footerA[1]

    prod_services = footer.findAll('h4')[0]

    all_rows = []
    first_row = []
    first_row.append(centerID), first_row.append(pageURL)
    first_row.append(prod_services.a.contents[0]), first_row.append(
        prod_services.a.get('href'))
    all_rows.append(first_row)  # well this is dumb

    for listItem in footer.findAll('li'):
        this_row = []
        this_row.append(centerID), this_row.append(pageURL)
        this_row.append(listItem.a.contents[0])  # subpage name
        this_row.append(listItem.a.get('href'))  # subpage URL
        all_rows.append(this_row)

    return all_rows


if __name__ == "__main__":
    main()  # do it
