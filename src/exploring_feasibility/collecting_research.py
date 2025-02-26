import requests

def get_author_id_by_name(name, limit=5):
    """
    Search author by name on Semantic Scholar and return the first matching author ID.
    """
    base_url = "https://api.semanticscholar.org/graph/v1/author/search"
    params = {
        "query": f'{name}',
        "limit": limit,
        "fields": 'affiliations',
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    print(data)
    if data.get('data'):
        return data['data'][0]['authorId']
    return None

def get_author_papers(author_id, fields="title,abstract,year", limit=50):
    """
    Get the author's papers with fields like title, abstract, year.
    """
    base_url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers"
    params = {
        "fields": fields,
        "limit": limit
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data.get('data', [])


# Example usage:
if __name__ == "__main__":
    professor_name = "Praveen Rao"
    author_id = get_author_id_by_name(professor_name)
    if author_id:
        papers = get_author_papers(author_id)
        index = 0
        for paper in papers:
            index+=1
            title = paper.get('title')
            abstract = paper.get('abstract', 'No abstract available')
            year = paper.get('year')
            print(f"{index}: {title} ({year})\nAbstract: {abstract}\n")
    else:
        print(f"No author found for {professor_name}")
