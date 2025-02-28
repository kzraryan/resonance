"""

Usage:

This script reads a CSV file containing researcher data and imports the researchers into the database.
The CSV file should have headers like "orcid_id" and "full_name".
"""

import csv
import sys
import logging
from services.db_service import get_db
from controllers.researcher import create_researcher, get_researcher_by_orcid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


def import_researchers(csv_file_path: str):
    """Read researchers from a CSV file and import them into the database."""
    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            with next(get_db()) as db:
                for row in reader:
                    orcid_id = row.get("orcid_id", "").strip()
                    full_name = row.get("full_name", "").strip()
                    department = row.get("department", "").strip()
                    position = row.get("position", "").strip()

                    if not orcid_id or not full_name:
                        logger.warning("Skipping row with missing orcid_id or full_name.")
                        continue

                    existing = get_researcher_by_orcid(db, orcid_id)
                    if existing:
                        logger.info(f"Researcher with ORCID {orcid_id} already exists, skipping.")
                    else:
                        researcher = create_researcher(db, orcid_id, full_name, department, position)
                        logger.info(f"Created researcher: {researcher.full_name} (ORCID: {researcher.orcid_id})")
    except FileNotFoundError:
        logger.error(f"File not found: {csv_file_path}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == '__main__':
    csv_file_path = 'researchers.csv'
    import_researchers(csv_file_path)
