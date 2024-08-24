import re

def extract_citation(text) -> list[str]:
    citation_pattern = r'\[\s*((\d+)(,\d+)*(\–\d+)*)\s*\]'
    matches = re.findall(citation_pattern, text)
    matches = [match[0] for match in matches]

    # Get the unique citations
    citations = []  
    for match in matches:
        parts = match.split(',')
        for part in parts:
            if '–' in part:
                start, end = part.split('–')
                citations.extend([i for i in range(int(start), int(end) + 1)])
            else:
                citations.append(int(part))

    results = sorted(list(set(citations)))
    results = [str(i) for i in results]
    return results