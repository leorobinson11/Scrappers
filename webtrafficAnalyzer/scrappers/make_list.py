import os, sys
from bs4 import  BeautifulSoup
import requests
import logging

def pullHTML(url):
    #requests html from a webpage and returns a beautiful soup object
    try:
        res = requests.get(url)
        return BeautifulSoup(res.text, "html.parser")
    except requests.exceptions.ConnectionError:
       logging.error(f'Requested url does not exist: {url}')
       return False

def makeCountryList(html):
    #generating a list of all the links for the list of newspappers for each county
    columns  = html.find_all("div", {"class": "row desktop"})
    for column in columns:
        for countrylink in column.find_all("a"):
            yield "https://usnpl.com" + countrylink['href']

def makeLinkList(country_links):
    #generating link lists for each country
    for country_link in country_links:
        #loading the html for the site with the list for every country
        chtml = pullHTML(country_link)
        table = chtml.find('table', {"class":"table table-sm"})
        with open(os.path.join('country_lists',country_link.split('=')[-1]+'.csv'), 'w') as file:
            for row in table.find_all('tr'):
                result = row.find_all('a')
                #if the row is'nt used for formating
                if len(result) != 0:
                    #getting only the hrefs
                    result = [res["href"] for res in result[1:]]
                    #generating blank spaces for where data on some of the sites is none existant
                    result = [res for res in result+['' for _ in range(4-len(result))]]
                    for index, res in enumerate(result):
                        file.write(res if index == 4 else res + ',')
                    file.write('\n')

def cleanLinkList():
    #removing invalid links from the list
    for country_links in os.listdir('country_lists'):
        #the file with the links
        with open(os.path.join('country_lists', country_links), 'r') as infile:
            #a new file for the filtered links
            with open(os.path.join('cleaned_lists', country_links), 'w') as outfile:
                for links in infile.readlines():
                    newlinks = links
                    for link in links.replace('\n','').split(','):
                        #if the link isnt none existant
                        if link != '' and not pullHTML(link):
                            #removing the invalid link from the file
                            newlinks = newlinks.replace(link,'')    
                    outfile.write(newlinks)
                        
            
if __name__ == "__main__":
    link = "https://usnpl.com"
    html = pullHTML(link)
    country_links = makeCountryList(html)
    makeLinkList(country_links)
    cleanLinkList()
    sys.exit('[+] finished')