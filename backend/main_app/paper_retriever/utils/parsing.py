from pypdf import PdfReader
import re
import json
import subprocess
from paper_retriever.utils.preprocess import clean_text
from paper_retriever.constants import ANYSTYPE_PATH, CITE_ID_TYPE


def parse_pdf2text(pdf_path):
    reader = PdfReader(pdf_path)
    number_of_pages = len(reader.pages)
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text() + "\n"

    return pdf_text


def parse_references_and_citations(text):    
    # Find the reference section
    text = clean_text(text)
    reference_section = re.search(r'References([\s\S]*)', text, re.IGNORECASE)
    if reference_section:
        references = reference_section.group()
    else:
        return "References section not found."
    
    # Extract individual references
    patterns = [r'\[\d+\].*?(?=\[\d+\]|\Z)',                                # For [1] ... [2] ... [3] ...    
                r'\n[0-9]{1,2}\.\s.*?(?=\n[0-9]{1,2}\.\s|\Z)'               # For 1. ... 2. ... 3. ...
    ]
    reference_list = []
    cite_id_type = None
    for i in range(len(patterns)):
        matches = re.findall(patterns[i], references, re.DOTALL)
        if matches:
            reference_list = [ref.replace('\n', '') for ref in matches]
            cite_id_type = CITE_ID_TYPE[i]
            break   

    return reference_list, cite_id_type


def parse_references(reference_list, cite_id_type, work_dir):
    if cite_id_type == None:
        return []
    
    file_path = f"{work_dir}/refs.txt"
    with open(file_path, "w") as f:
        for ref in reference_list:
            f.write(ref[4:] + '\n')

    process = subprocess.Popen([ANYSTYPE_PATH, 'parse', file_path], 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE,
                           text=True)

    stdout, stderr = process.communicate()

    if stderr:
        raise NameError(stderr)

    parsed_refs = json.loads(stdout)

    for i, ref in enumerate(reference_list):
        if cite_id_type == "square_brackets":
            parsed_refs[i]["cite_id"] = ref[1:ref.find(']')]
        elif cite_id_type == "periods":
            parsed_refs[i]["cite_id"] = ref[0:ref.find('.')]
        else:
            parsed_refs[i]["cite_id"] = str(i + 1)        

    return parsed_refs