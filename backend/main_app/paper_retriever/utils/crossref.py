import pandas as pd
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from paper_retriever.constants import CROSSREF_SEARCH_URL


def crossref_search(reference):
    params = {
        'query': reference
    }
    r = requests.get(CROSSREF_SEARCH_URL, params= params)   
    try:
        output = r.json()['message']['items'][0]
    except:
        print(f"Error: {r.json()}")
        return None
    return output


def tfidf_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])    
    return similarity[0][0]


def retrieve_from_crossref(parsed_refs):
    arxiv_search_results = {
        'cite_id': [],
        'tf-idf_score': [],
        'ref_title': [],
        'res_title': [],
        'URL': [],
        'abstract': [],
        'arxiv_id': []
    }

    for ref in tqdm(parsed_refs):
        print("-------------------------------")
        print(ref)
        print("-------------------------------")
        try:
            ref_text_title = ref["title"][0]
            search_result = crossref_search(ref_text_title)
            search_result_title = search_result['title'][0]
            search_result_url = search_result['URL']
            sim_score = tfidf_similarity(ref_text_title, search_result_title)
            arxiv_id = ""
            if 'arxiv' in ref.keys():
                arxiv_id = ref['arxiv'][0]
            elif 'date' in ref.keys():
                arxiv_id = ref['date'][0].split("/")[1].split(",")[0]
            if arxiv_id != "":
                search_result_url = "https://arxiv.org/pdf/" + arxiv_id
                sim_score = 1
        except:
            ref_text_title = ""
            search_result_title = ""
            search_result_url = ""
            sim_score = 0

        try:
            abstract = get_abstract(search_result_url)
        except:
            abstract = ""
        
        arxiv_search_results['cite_id'].append(ref['cite_id'])
        arxiv_search_results['ref_title'].append(ref_text_title)
        arxiv_search_results['res_title'].append(search_result_title)
        arxiv_search_results['tf-idf_score'].append(sim_score)
        arxiv_search_results['URL'].append(search_result_url)
        arxiv_search_results['abstract'].append(abstract)
        arxiv_search_results['arxiv_id'].append(arxiv_id)

    retrieve_df = pd.DataFrame(arxiv_search_results)
    return retrieve_df


def get_abstract(doi_url: list[str]):

    # Set the headers for the request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'Referer': 'http://dx.doi.org/',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'
    }

    # Sample DOI
    # doi_urls = [
    #         "http://dx.doi.org/10.5201/ipol.2011.my-asift",
    #         "http://dx.doi.org/10.1109/cvpr.2012.6247842",
    #         "http://dx.doi.org/10.5201/ipol.2013.87",
    #         "http://dx.doi.org/10.1109/iccv.1999.790410",
    #         "http://dx.doi.org/10.1023/b:visi.0000029664.99615.94",
    #         "http://dx.doi.org/10.1007/11744023_34",
    # ]

    response = requests.get(doi_url)
    url = response.url
    # print(f"\n\n\nOriginal URL: {doi_url}")
    # print(f"Response URL: {url}")
    response = requests.get(url, headers=headers)

    # Parse the HTML and locate the <h2> tag that contains "Abstract"
    soup = BeautifulSoup(response.text, 'html.parser')
    h2_tags = soup.find_all('h2')
    abstract_heading = None
    for tag in h2_tags:
        if "abstract" in tag.get_text().lower():
            abstract_heading = tag
            break      

    # Extract the next sibling that contains the abstract text
    if abstract_heading:
        abstract_content = abstract_heading.find_next_sibling()
        if abstract_content:
            # Check if the abstract is split into multiple paragraphs
            paragraphs = abstract_content.find_all('p')
            if paragraphs:
                abstract_text = "\n\n".join(p.get_text(strip=True) for p in paragraphs)
            else:
                # Otherwise, assume the abstract is a single block of text
                abstract_text = abstract_content.get_text(strip=True)
            print(f"Abstract found: {abstract_text[:50]}.")
            return abstract_text
        else:
            print("Abstract content not found.")
            return None
    else:
        print("Abstract heading not found.")
        return None