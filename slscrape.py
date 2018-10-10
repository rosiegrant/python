import csv
import requests
from bs4 import BeautifulSoup
import sys


def main():

    # prepare output file
    outfile = open("./slscrape.csv", "w")
    writer = csv.writer(outfile)
    writer.writerow(
        ["CenterID", "CenterURL", "Subpage Name", "Subpage URL"])  # first row, of headers

    # iterate through URLs, from file that's taken in via the command line
    infile = open(sys.argv[1])
    infile.readline()  # throw out the first line with headers

    for line in infile:

        row = line.split(',')
        # print(row)
        entityId = row[0]
        pageURL = row[2].replace("\n", "")
        # print("pageURL", pageURL)
        print("processing store ", entityId)

       	# soupStuff(entityId, pageURL)  # do the beautiful soup things

       # allRows = soupStuff(entityId, pageURL)  # do the beautiful soup things
       # writer.writerows(allRows)  # write data to outfile

    soupStuff("1234", "http://www.seniorlifestyle.com/property/sheridan-mason/")
    outfile.close()


def soupStuff(entityId, pageURL):

    response = requests.get(pageURL)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    # print(soup.prettify())

    # get business name and phone number
    span9 = soup.findAll("div", {"class": "span9"}) #find all divs whose class is span9
    if (len(span9) == 0):
        print("Can't find any span9 column classes",
              entityId)  # this store doesn't match the pattern
    nap = span9[0]
    name = nap.find('h2').text
    # print(name)
    phone = nap.find(itemprop="telephone").text
    # print(phone)

    # get rate
    rate = soup.find(itemprop="priceRange").text
    # print(rate)

    # get services 
    # for service in soup.find(text='providing').parent.find_next_sibling():
    # 	print(service.text)

    # About main title
    about = soup.find(itemtype="http://schema.org/Organization", id="about")
    mainTitle = about.h1.text
    # print(mainTitle)

    h4s = about.findAll('h4')
    ps = about.findAll('p')

    h4length = len(h4s)
    pslength = len(ps)

    # sib = about.h4.next_sibling;
    # while sib == 'p':
    # 	print(sib)
    # 	sib = sib.next_sibling;
    for header in h4s:
    	sib = header.find_next_sibling()
    	print(header)
    	pcount = 0;
    	while sib and sib.name == 'p': #get all ps that are adjacent to that h4
    		print(sib)
    		sib = sib.find_next_sibling()
    		pcount+=1
    	print(pcount)
    	if pcount == 0:
    		print("E M P T Y HEADER")	




    # services = soup.find(text='providing').findNext('ul').li
    # services = soup.find(text='providing').findAll('ul').li
    # prodservColumn = footerColumns[1]
    # prodservItem = prodservColumn.find_all(
    #     'h4')[0]

    # if ("Products" not in prodservItem.a.contents[0]):
    #     print("Whoops! Store ", entityId,
    #           "doesn't have product and services where we expected it. Skipping this store.")
    #     print(prodservItem.a.contents[0])
    #     return {}

    # allRows = []
    # firstRow = []
    # firstRow.append(entityId), firstRow.append(pageURL)
    # firstRow.append(prodservItem.a.contents[0]), firstRow.append(
    #     prodservItem.a.get('href'))
    # allRows.append(firstRow)  # well this is dumb

    # for listItem in prodservColumn.findAll('li'):
    #     thisRow = []
    #     thisRow.append(entityId), thisRow.append(pageURL)
    #     thisRow.append(listItem.a.contents[0])  # subpage name
    #     thisRow.append(listItem.a.get('href'))  # subpage URL
    #     allRows.append(thisRow)

    # return allRows


if __name__ == "__main__":
    main()  # do it
