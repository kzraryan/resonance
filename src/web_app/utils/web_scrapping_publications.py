import requests
import urllib.parse
import re


def strip_xml_tags(text_only):
    """
    1. Parses and strips out XML/HTML tags (e.g., <jats:sec>, <jats:title>).
    2. Replaces multiple spaces/newlines with a single space.
    3. Trims leading/trailing whitespace.
    """

    # 1) Remove tags by parsing and extracting text
    text_only = re.sub(r'<[^>]*>', ' ', text_only)

    # 2) Replace multiple whitespace (spaces, newlines, tabs) with a single space
    text_only = re.sub(r"\s+", " ", text_only)

    # 3) Trim leading and trailing whitespace
    clean_text = text_only.strip()

    return clean_text


def get_crossref_metadata(doi: str):
    """
    Query Crossref by DOI for metadata, including the abstract (if available).
    Returns a dict with keys like: title, abstract, authors, publisher, published.
    """
    # Normalize the DOI (remove protocol, etc.)
    if doi is None:
        return None
    doi = doi.strip()
    if doi.startswith("http"):
        # e.g. "https://doi.org/10.1000/xyz123"
        # Extract just the "10.1000/xyz123" portion
        doi = doi.split("doi.org/")[-1]

    # URL-encode the DOI to handle special characters
    encoded_doi = urllib.parse.quote(doi)
    url = f"https://api.crossref.org/works/{encoded_doi}"

    r = requests.get(url)
    if r.status_code != 200:
        return None

    # 'message' field contains the actual metadata
    data = r.json().get("message", {})
    metadata = {
        "title": None,
        "abstract": None,
        "doi": doi,
        "year": None,
    }

    # Title may be a list in Crossref
    if data.get("title"):
        metadata["title"] = data["title"][0] if len(data["title"]) > 0 else None

    # Extract publication year from one of the possible fields.
    year = None
    if "published-print" in data and "date-parts" in data["published-print"]:
        date_parts = data["published-print"]["date-parts"]
        if date_parts and len(date_parts[0]) >= 1:
            year = date_parts[0][0]
    elif "published-online" in data and "date-parts" in data["published-online"]:
        date_parts = data["published-online"]["date-parts"]
        if date_parts and len(date_parts[0]) >= 1:
            year = date_parts[0][0]
    elif "issued" in data and "date-parts" in data["issued"]:
        date_parts = data["issued"]["date-parts"]
        if date_parts and len(date_parts[0]) >= 1:
            year = date_parts[0][0]

    metadata["year"] = year

    # Abstract is sometimes present under "abstract"
    if data.get("abstract"):
        metadata["abstract"] = strip_xml_tags(data["abstract"])

    return metadata


def get_orcid_works(orcid_id: str):
    """
    Fetches all "works" (i.e., publications) from the given ORCID iD.
    Returns a list of dicts with keys: 'title', 'year', 'doi'.
    """
    url = f"https://pub.orcid.org/v3.0/{orcid_id}/record"
    headers = {"Accept": "application/json"}  # ORCID requires JSON accept header
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"ORCID API error: {response.status_code}")
        return []

    data = response.json()

    # Navigate to the works array
    # data["activities-summary"]["works"]["group"] is typically a list of works
    works_data = data.get("activities-summary", {}).get("works", {}).get("group", [])

    results = []
    for w in works_data:
        # Each group has one or more "work-summary" items. We usually take the first as a representative.
        work_summary = w.get("work-summary", [])[0]
        if not work_summary:
            continue

        # Title
        title_info = work_summary.get("title", {})
        title_value = None
        if "title" in title_info and title_info["title"]:
            title_value = title_info["title"].get("value")


        # Extract DOI from the external IDs
        doi = None
        external_ids = work_summary.get("external-ids", {}).get("external-id", [])
        for eid in external_ids:
            if eid.get("external-id-type", "").lower() == "doi":
                doi = eid.get("external-id-value")
                break

        results.append({
            "title": title_value,
            "doi": doi
        })

    return results


def get_publication_data(orcid_ids):
    all_publication_data = []
    for orcid_id in orcid_ids:
        works = get_orcid_works(orcid_id["orcid_id"])
        print(f"Works for {orcid_id['orcid_id']}: len={len(works)}")
        for work in works:
            publication_data = get_crossref_metadata(work["doi"])
            if publication_data is None or publication_data["abstract"] is None:
                continue
            all_publication_data.append(
                {
                    "orcid_id": orcid_id["orcid_id"],
                    "title": publication_data['title'],
                    "abstract": publication_data['abstract'],
                    "year": publication_data['year'],
                    "doi": publication_data['doi']
                }
            )

    return all_publication_data