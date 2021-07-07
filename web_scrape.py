from selenium import webdriver
from bs4 import BeautifulSoup 
import pandas as pd
import time


# using this mehhod it will generate the inside link of the given article 
# then scraping the is done for link and abastract
def generate_and_extract_abstract(pmid):

    custom_url_web_paper = "https://pubmed.ncbi.nlm.nih.gov/"
    custom_url_web_paper = custom_url_web_paper+pmid+"/"

    soup_paper, browser = driver_connect(custom_url_web_paper, 10)
    
    for record in soup_paper.find_all('main', attrs = {'class' : "article-details"}):
        doi_link = record.find('span', attrs = {'class' : 'citation-doi'})
        abstract = record.find('div', attrs = {'class' : 'abstract-content selected'})
    
    browser.quit()
    try:
        doi_link = doi_link.text
    except:
        doi_link = "None"

    try:
        abstract =abstract.text
    except:
        abstract = "None"
    
    return doi_link.text, abstract.text, custom_url_web_paper
    
# this is method which is get the chrome driver and loading url of the given website
def driver_connect(url_need_to_get, time_vari):

    driver = webdriver.Chrome('chromedriver_win32/chromedriver')
    driver.get(url_need_to_get)
    time.sleep(time_vari)
    content = driver.page_source
    soup = BeautifulSoup(content)
    

    return soup, driver

# this is the main driving method
def main_driver_function():
    titles = []
    authers = []
    doi_links = []
    publication_types = []
    abstracts = []
    site_paper_link = []

    # this link should be varied for site to stite also attributes should be configers 
    # which match the site classes and tags
    soup, driver = driver_connect("https://pubmed.ncbi.nlm.nih.gov/?term=quantum+machanical+applications+in+canser+research&filter=simsearch1.fha&filter=pubt.review", 20)
    for a in soup.find_all(attrs = {'class' : 'full-docsum'}):
            
        title = a.find('a', attrs = {'class' : 'docsum-title'})
        auther = a.find('span', attrs = {'class' : 'docsum-authors full-authors'})
        publication_type = a.find('span', attrs = {'class' : 'publication-type spaced-citation-item citation-part'})

        pmid = a.find('span', attrs = {'class' : 'docsum-pmid'})
        pmid = pmid.text

        # inside link details grabbing 
        doi_link, abstract, paper_url= generate_and_extract_abstract(pmid)

        title = title.text
        auther = auther.text
        publication_type = publication_type.text

        # adding grabed data to the list which is used in dataframe
        titles.append(title)
        authers.append(auther)
        publication_types.append(publication_type)
        doi_links.append(doi_link)
        site_paper_link.append(paper_url)
        abstracts.append(abstract)

    df = pd.DataFrame({'Titel_name' : titles, 'authers' : authers, 'publicatio_type' : publication_types, 'paper_links' : doi_links, \
        'abstracts' : abstracts, 'pub_med_url' : site_paper_link})
    print(df)
    df.to_csv('results/extract.csv', index = True, encoding='utf-8')
    
    #close the browser after work done
    driver.quit()


if __name__ == '__main__':

    main_driver_function()