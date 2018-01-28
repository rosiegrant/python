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

        allRows = soupStuff(centerID, pageURL)  # do the beautiful soup things
        writer.writerows(allRows)  # write data to outfile

    outfile.close()


def soupStuff(centerID, pageURL):

    response = requests.get(pageURL)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    # print(soup.prettify())
    footerColumns = soup.findAll("div", {"class": "footerColumn"})
    if (len(footerColumns) > 3):
        print("Number of footer elements higher than expected for store ",
              centerID)  # this store doesn't match the pattern

    prodservColumn = footerColumns[1]
    prodservItem = prodservColumn.find_all(
        'h4')[0]

    if ("Products" not in prodservItem.a.contents[0]):
        print("Whoops! Store ", centerID,
              "doesn't have product and services where we expected it. Skipping this store.")
        print(prodservItem.a.contents[0])
        return {}

    allRows = []
    firstRow = []
    firstRow.append(centerID), firstRow.append(pageURL)
    firstRow.append(prodservItem.a.contents[0]), firstRow.append(
        prodservItem.a.get('href'))
    allRows.append(firstRow)  # well this is dumb

    for listItem in prodservColumn.findAll('li'):
        thisRow = []
        thisRow.append(centerID), thisRow.append(pageURL)
        thisRow.append(listItem.a.contents[0])  # subpage name
        thisRow.append(listItem.a.get('href'))  # subpage URL
        allRows.append(thisRow)

    return allRows


if __name__ == "__main__":
    main()  # do it
