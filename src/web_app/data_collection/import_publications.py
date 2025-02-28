from controllers.publication import import_publications_from_online, include_publications
from controllers.researcher import get_all_researchers
from services.db_service import get_db
from utils.web_scrapping_publications import get_publication_data
import pandas as pd


def import_publications_for_all_researchers():
    csv_file_path = 'researchers_db.csv'
    df = pd.read_csv(csv_file_path, encoding='utf-8', header=None, names=['researcher_id','orcid_id', 'f', 'd', 'p'])
    all_publications = []
    for index, row in df.iterrows():
        orcid_id = row['orcid_id'].strip()
        publications = get_publication_data([{"orcid_id": orcid_id}])
        for pub in publications:
            pub["researcher_id"] = row['researcher_id']
        all_publications.extend(publications)
    df_publications = pd.DataFrame(all_publications)
    df_publications.to_csv('publications.csv', index=False)


if __name__ == '__main__':
    import_publications_for_all_researchers()
