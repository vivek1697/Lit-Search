from urllib.request import Request, urlopen
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
    
    df = pd.DataFrame()
    
    page_ids = full_web_page_scrapper()
    for id in page_ids:
        url = 'https://pubmed.ncbi.nlm.nih.gov/{}/'.format(id)
        print(url)
        page = bs(urlopen(url), "html.parser")
 
        article_details = page.find("div",{"id":"article-details"})
        date = article_details.find("span", {"class":"cit"}).text.strip().split(';')[0]
        heading = article_details.find("h1", {"class":"heading-title"}).text.strip()
        journal = article_details.find("span", {"class":"journal"}).text.strip()
        try:
            abstract = article_details.find("div", {"id":"enc-abstract"}).text.strip()
        except:
            nested_abstracts = article_details.find("div", {"id":"enc-abstract"})
            print(nested_abstracts)
            if nested_abstracts:
                for nested_abstract in nested_abstracts.split('\n'):
                    abstract = abstract + nested_abstract.strip()
                       
        try:
            mesh_terms = article_details.find("div", {"id":"mesh-terms"}).text.strip()
        except:
            mesh_terms = None
        available_mesh_terms = []
        if mesh_terms:
            
            for term in mesh_terms.split('\n'):
                if term.strip():
                    if term != 'MeSH terms':
                        available_mesh_terms.append(term.strip())
        new_df = pd.DataFrame({
            'Date': date,
            'heading': heading,
            'journal': journal,
            'abstract': abstract,
            'Mesh-terms' : [available_mesh_terms]
        })
        df = pd.concat([df, new_df])   
    
    return print(df)

def full_web_page_scrapper():
    
    url = 'https://pubmed.ncbi.nlm.nih.gov/trending/'
    page = bs(urlopen(url), "html.parser")
    page_ids = []
    full_page = page.find("div",{"class":"search-results-chunk results-chunk"})
    for id in full_page['data-chunk-ids'].split(','):
        page_ids.append(id)
    print(page_ids)
    
    return page_ids

web_scrapper()
