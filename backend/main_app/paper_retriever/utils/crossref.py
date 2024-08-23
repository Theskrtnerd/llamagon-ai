import pandas as pd
import requests
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from paper_retriever.constants import CROSSREF_SEARCH_URL


def crossref_search(reference):
    params = {
        'query': reference
    }
    r = requests.get(CROSSREF_SEARCH_URL, params= params)    
    return r.json()['message']['items'][0]


def tfidf_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])    
    return similarity[0][0]


def retrieve_from_crossref(parsed_refs):
    arvix_search_results = {
        'cite_id': [],
        'tf-idf_score': [],
        'ref_title': [],
        'res_title': [],
        'URL': []
    }

    for ref in tqdm(parsed_refs):
        ref_text_title = ref["title"][0]

        search_result = crossref_search(ref_text_title)
        try:
            search_result_title = search_result['title'][0]
            search_result_url = search_result['URL']
            sim_score = tfidf_similarity(ref_text_title, search_result_title)
        except:
            search_result_title = ""
            search_result_url = ""
            sim_score = 0
        
        arvix_search_results['cite_id'].append(ref['cite_id'])
        arvix_search_results['ref_title'].append(ref_text_title)
        arvix_search_results['res_title'].append(search_result_title)
        arvix_search_results['tf-idf_score'].append(sim_score)
        arvix_search_results['URL'].append(search_result_url)

    retrieve_df = pd.DataFrame(arvix_search_results)

    return retrieve_df