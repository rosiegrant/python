import csv
import requests
from bs4 import BeautifulSoup
import sys


def main():

    # prepare output file
    outfile = open("./slscrape.csv", "w")
    writer = csv.writer(outfile)
    writer.writerow(
        ["Entity ID", "Client URL", "Business Name", "Phone","Rate","Services", "About Main Title", "About Header 1", 
        	"About Description 1", "About Header 2", "About Description 2", "About Header 3", "About Description 3", 
        	"About Header 4", "About Description 4", "About Header 5", "About Description 5"])  # Add headers to output file

    # iterate through URLs, from file that's taken in via the command line, first argument
    infile = open(sys.argv[1])
    infile.readline()  # throw out the first line with headers

    for line in infile:

        row = line.split(',')
        entityId = row[0]
        pageURL = row[2].replace("\n", "")
        print("processing store ", entityId)
        writer.writerow(soupStuff(entityId, pageURL))


       # allRows = soupStuff(entityId, pageURL)  # do the beautiful soup things
       # writer.writerows(allRows)  # write data to outfile

    # writer.writerow(soupStuff("1234", "http://www.seniorlifestyle.com/property/morningside-house-leesburg/"))
    outfile.close()


def soupStuff(entityId, pageURL):

    response = requests.get(pageURL)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")

    thisRow = [] # Start assembling the row that will be added to the output file
    thisRow.append(entityId), thisRow.append(pageURL)

    # Get Business Name and Phone Number
    span9 = soup.findAll("div", {"class": "span9"}) # find all divs who have the span9 class
    if (len(span9) == 0 or span9[0].find('h2') is None):
        print("Error for ", entityId)  
        thisRow.append("Error found, sorry!") # This store doesn't match the pattern, abort and return an empty row with an error
        return thisRow

    nap = span9[0]
    name = nap.find('h2') # business name
    if name: thisRow.append(name.text) 
    else: thisRow.append(" ") # no name found

    phone = nap.find(itemprop="telephone") # phone number
    if phone: thisRow.append(phone.text) 
    else: thisRow.append(" ") # no phone found

    # Get Rate
    rate = soup.find(itemprop="priceRange")
    if rate: thisRow.append(rate.text)
    else: thisRow.append(" ") # no rate found

    # Get Services, store in a pipe delimited cell 
    # TODO: there's always a trailing pipe, fix that
    services = ""
    for service in soup.find(text='providing').parent.find_next_sibling():
    	services = services + service.text + " | " 
    thisRow.append(services)

    # Get About Main Title
    about = soup.find(itemtype="http://schema.org/Organization", id="about")
    mainTitle = about.h1.text
    thisRow.append(mainTitle)


    # Content
    h4s = about.findAll('h4')
    for header in h4s:
    	sib = header.find_next_sibling()
    	thisRow.append(header.text) # About Header n
    	pcount = 0;
    	content = ""
    	while sib and sib.name == 'p': # Get all <p>s that are adjacent to the current <h4>
    		content = content + " " + sib.text # Append all <p>s together
    		sib = sib.find_next_sibling()
    		pcount+=1
    	thisRow.append(content)

    # print(thisRow)
    print("Made it!")
    return(thisRow)




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
