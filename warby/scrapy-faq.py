import csv
import requests
from bs4 import BeautifulSoup
import sys


def main():

    # prepare output file
    outfile = open("./warby-faq.csv", "w")
    writer = csv.writer(outfile)
    url = sys.argv[1] #get URL from the command line

    allRows = soupUrlStuff(url) # get all the page for each product
    for row in allRows: # for each page, collect the images for that product
    #     print("row 0: " + row[0])
    #     imageSet = soupStuffImage(row[0])
    #     imageSet.append(row[1])
    #     print(imageSet)
        writer.writerow(row)  # write data to outfile
    outfile.close()

def soupUrlStuff(pageURL):
    response = requests.get(pageURL)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    pageBody = soup.findAll("div", {'class': '0 1 2 3'})
    allRows = []
    for i in pageBody: 
        children = i.findChildren("div", recursive=False)
        for previous, current in zip(children[::2], children[1::2]):
            thisRow= []
            print(previous)
            print(current)
            print('\n')
            thisRow.append(previous)
            thisRow.append(current)
            allRows.append(thisRow)
    return allRows
    
    # for atag in atags:
    #     thisRow = []
    #     link = "https://www.warbyparker.com" + atag['href']
    #     thisRow.append(link)
    #     name = atag['href'].split("/")[3]
    #     thisRow.append(name)
    #     print(name)
    #     print(thisRow)
    #     allRows.append(thisRow)

    # print(len(allRows));
    return allRows


if __name__ == "__main__":
    main()  # do it
