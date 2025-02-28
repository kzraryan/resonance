import pandas as pd
from utils.generate_metadata_from_research import generate_publication_metadata

def generate_metadata_from_multiple_research(csv_file_path):
    df = pd.read_csv(csv_file_path, encoding='utf-8', header=None, names=['pid', 'r', 'doi', 'title', 'abstract', 'year'])

    all_publication_metadata = []
    for index, row in df.iterrows():
        print(index)
        publication_metadata = generate_publication_metadata(row['abstract'])
        publication_metadata["publication_id"] = row['pid']
        all_publication_metadata.append(publication_metadata)
    df_publications = pd.DataFrame(all_publication_metadata)
    df_publications.to_csv('publication_metadata_32.csv', index=False)

if __name__ == '__main__':
    csv_file_path = 'publications_db.csv'
    generate_metadata_from_multiple_research(csv_file_path)