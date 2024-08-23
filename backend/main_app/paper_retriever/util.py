import xml.etree.ElementTree as ET
import requests


def get_title_from_doi(doi: str):
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    return data['message']['title'][0]

def parse_arxiv_response(xml_data):
    # Parse the XML data
    root = ET.fromstring(xml_data)

    # Define namespaces
    namespaces = {
        'atom': 'http://www.w3.org/2005/Atom',
        'opensearch': 'http://a9.com/-/spec/opensearch/1.1/',
        'arxiv': 'http://arxiv.org/schemas/atom'
    }
    
    results = []

    # Extract individual entries
    for entry in root.findall('atom:entry', namespaces):
        entry_id = entry.find('atom:id', namespaces).text
        entry_title = entry.find('atom:title', namespaces).text
        entry_summary = entry.find('atom:summary', namespaces).text
        entry_published = entry.find('atom:published', namespaces).text
        
        # Authors
        authors = [author.find('atom:name', namespaces).text for author in entry.findall('atom:author', namespaces)]
        
        # DOI (if present)
        doi_element = entry.find('arxiv:doi', namespaces)
        doi = doi_element.text if doi_element is not None else None
        
        results.append({
            'id': entry_id,
            'title': entry_title,
            'summary': entry_summary,
            'published': entry_published,
            'authors': authors,
            'doi': doi
        })
    
    return results