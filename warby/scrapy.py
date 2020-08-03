import csv
import requests
from bs4 import BeautifulSoup
import sys


def main():

    # prepare output file
    outfile = open("./warby5.csv", "w")
    writer = csv.writer(outfile)
    url = sys.argv[1] #get URL from the command line

    allRows = soupUrlStuff(url) # get all the page for each product
    i = 0 #keep track of id
    for row in allRows: # for each page, collect the images for that product
        print("row 0: " + row[0])
        imageSet = soupStuffImage(row[0]) # pass the url
        imageSet.append(row[1]) # add the name to this row
        id = "product-" + str(i)
        imageSet.append(id) # id 
        imageSet.append("en")
        imageSet.append("product")
        i = i+1
        writer.writerow(imageSet)  # write data to outfile
    outfile.close()

def soupStuffImage(pageURL):
    response = requests.get(pageURL)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    allImages = soup.findAll("img", {'class': 'c-product-slide--product-image__image'})
    imageSet = []
    for i in allImages:
        srcSet = i['srcset']
        singleImage = srcSet.split(",")[6].split(" ")[0][2:] # get the largest image from the list
        print("adding " + singleImage + " image")
        singleImage = "https://" + singleImage
        imageSet.append(singleImage) # append to array
    return imageSet # return all images for this product

def soupUrlStuff(pageURL):
    response = requests.get(pageURL)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    atags = soup.findAll("a", {'class': 'c-reset-frame-gallery-v2__image'})
    allRows = []
    for atag in atags:
        thisRow = []
        link = "https://www.warbyparker.com" + atag['href']
        thisRow.append(link)
        name = atag['href'].split("/")[3] # get the name of the product
        thisRow.append(name)
        allRows.append(thisRow)

    print(len(allRows));
    return allRows


if __name__ == "__main__":
    main()  # do it
