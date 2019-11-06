from __future__ import print_function
import os
import errno
from HTMLParser import HTMLParser
import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
import codecs


ARTS_LIST = 'arts-select-chinese-japanese.list'
NUMBER_TO_DOWNLOAD = -1     # set to -1 to download all

# The URL for the artifact from Bigquery is a webpage, which contains a link
# to download the original image.  This class parses for the download link

class MetArtHTMLParser(HTMLParser):
    # Look for the image link in the http page and download the original image
    def handle_starttag(self, tag, attrs):
        #printf(attrs)
        if tag == 'a':
            try: 
                if ('gtm__download__image' == attrs[1][1]):
                    for attr in attrs:
                        if (attr[0] == 'href'):
                        #selectedOrDefaultDownload
                            art_url = attr[1].split("'")[0]
                        # Return the URL to download the original image
                        try:
                            self.data = art_url  
                        except:
                            print("no data")
            except IndexError:
                print("index error")
            # Look for the keyword selectedOrDefaultDownload in an href

with open(ARTS_LIST) as f:
    arts_to_download = f.readlines()
    arts_to_download = [x.strip() for x in arts_to_download]
    f.close()

myparser = MetArtHTMLParser()

for item in arts_to_download:
    # Parse the line to get the culture label and the webpage for the artifact
    pick = item.split("',")
    culture = pick[1].replace(" u'", "")
    webpage = pick[2].replace(" u'", "").replace("')", "")
    print(culture, webpage)

    # Download the webpage and parse for the image URL
    url = webpage
    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, features='html.parser')
    print(type(soup))
    driver.quit()
    #print(soup.text)

    # find all a attributes
    heds = soup.find_all("a", class_="gtm__download__image")
    print(type(heds))

    urls = []
    for h in heds:
        urlstring = str(h.attrs['href'])
        urls.append(urlstring)
    
    print(urls)

    encoding = "UTF-8"
    #with codecs.open("output1.html", "w", encoding='utf8') as file:
    #    file.write(str(soup))

    #with open("output1.html", "r") as file:    
    #    html_page = file.read()
        #print(html_page)
    
    try:
        
        #myparser.feed(soup.text)
        # Create a directory with the culture as name if it doesn't exist yet
        # (remove characters that are not valid for directory name)
        culture = culture.replace(",", "")
        culture = culture.replace("/", " ")
        download_dir = 'data/met_art/' + culture

        try:
            os.makedirs(download_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        # Download the image into the directory
        try:
            download_path = download_dir + '/' + urls[0].split("/")[-1]
        except:
            print("3")

        image_file = open(download_path, 'wb')

        # Convert the url to the %-encoded format since it may be
        # in other format like utf-8

        image_url = urllib2.quote(urls[0].encode(encoding), '/:')
        print("image to download:  ", image_url)
        response = urllib2.urlopen(image_url)
        image_file.write(response.read())
        image_file.close()
    except:
        print("Error, skipping url: ", webpage)
