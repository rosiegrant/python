import csv
import requests
from bs4 import BeautifulSoup
import sys


def main():

    # Prepare output file
    # outfile = open("./slscrape.csv", "w")
    outfile = open(sys.argv[2], "w")
    writer = csv.writer(outfile)
    writer.writerow(
        ["Entity ID", "Client URL", "Business Name", "Phone","Rate","Services", "About Main Title", "About Header 1", 
        	"About Description 1", "About Header 2", "About Description 2", "About Header 3", "About Description 3", 
        	"About Header 4", "About Description 4", "About Header 5", "About Description 5"])  # Add headers to output file

    # Iterate through URLs, from file that's taken in via the command line, first argument
    infile = open(sys.argv[1])
    infile.readline()  # Throw out the first line with headers

    for line in infile:

        row = line.split(',')
        entityId = row[0]
        pageURL = row[2].replace("\n", "")
        print("processing store ", entityId)
        writer.writerow(soupStuff(entityId, pageURL))

    # for testing a single URL:
    # writer.writerow(soupStuff("1234", "http://www.cadenceattheglenva.com/"))
    outfile.close()


def soupStuff(entityId, pageURL):

    # Assemble the row that will be added to the output file
    thisRow = [] 
    thisRow.append(entityId), thisRow.append(pageURL)

    # Get the page
    response = requests.get(pageURL)
    if response.status_code is not 200:
    	thisRow.append("Unable to reach site, status code is not 200")
    	return thisRow

    html = response.content
    soup = BeautifulSoup(html, "html.parser")

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
    mainTitle = about.h1
    if mainTitle: thisRow.append(mainTitle.text)
    else: thisRow.append(" ") #no title found


    # Get Content
    h4s = about.findAll('h4')
    for header in h4s:
    	sib = header.find_next_sibling()
    	thisRow.append(header.text) # About Header n
    	content = ""
    	while sib and sib.name == 'p': # Get all <p>s that are adjacent to the current <h4>
    		content = content + " " + sib.text # Append all <p>s together
    		sib = sib.find_next_sibling()
    	thisRow.append(content)

    # print(thisRow)
    print("Made it!")
    return(thisRow)


if __name__ == "__main__":
    main()  # booyah
