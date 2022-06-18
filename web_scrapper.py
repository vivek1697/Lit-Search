from urllib.request import Request, urlopen
from zoneinfo import available_timezones
from bs4 import BeautifulSoup as bs
import pandas as pd
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
    
    
def web_scrapper():
    url = 'https://pubmed.ncbi.nlm.nih.gov/35700704/'
    page = bs(urlopen(url))
 
    article_details = page.find("div",{"id":"article-details"})
    date = article_details.find("span", {"class":"cit"}).text.strip().split(';')[0]
    heading = article_details.find("h1", {"class":"heading-title"}).text.strip()
    journal = article_details.find("span", {"class":"journal"}).text.strip()
    abstract = article_details.find("div", {"id":"enc-abstract"}).text.strip()
    mesh_terms = article_details.find("div", {"id":"mesh-terms"}).text.strip()
    available_mesh_terms = []
    if mesh_terms:
        
        for term in mesh_terms.split('\n'):
            if term.strip():
                if term != 'MeSH terms':
                    available_mesh_terms.append(term.strip())
        
    print(available_mesh_terms)
            
    df = pd.DataFrame({
        'Date': date,
        'heading': heading,
        'journal': journal,
        'abstract': abstract,
        'Mesh-terms' : [available_mesh_terms]
    })

    return print(df)

web_scrapper()