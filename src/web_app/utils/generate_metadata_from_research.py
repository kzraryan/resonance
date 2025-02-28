import re
import json
from langchain_ollama import OllamaLLM

from models.models import PublicationMetadata
from utils.constants import METADATA_LLM_MODEL

def get_required_keys_from_model() -> list:
    """
    Returns a list of column names from PublicationMetadata that are used for tags.
    Excludes columns that are not part of the tag set.
    """
    # Define columns to exclude (adjust if needed)
    exclude = {"id", "publication_id"}
    return [col.name for col in PublicationMetadata.__table__.columns if col.name not in exclude]

def extract_json_from_response(response: str) -> dict:
    """
    Extract JSON content from an LLM response that contains a JSON code block.

    It looks for a block delimited by triple backticks with an optional 'json' marker.
    If parsing fails or if some keys (as defined in the PublicationMetadata model) are missing,
    it returns a dictionary with all required keys (missing keys are set to an empty string).

    Args:
        response (str): The raw response string from the LLM.

    Returns:
        dict: A dictionary containing all required PublicationMetadata keys.
    """
    result = {}
    try:
        # Look for a JSON code block delimited by triple backticks with an optional "json" marker.
        pattern = r"```json\s*(\{.*?\})\s*```"
        match = re.search(pattern, response, re.DOTALL)
        if match:
            json_text = match.group(1)
            result = json.loads(json_text)
        else:
            # Fallback: try to parse the entire response as JSON.
            result = json.loads(response)
    except Exception:
        # If parsing fails, start with an empty dictionary.
        result = {}

    # Ensure all required keys from the model are present; assign empty string if missing.
    required_keys = get_required_keys_from_model()
    output = {}
    for key in required_keys:
        if key not in result:
            output[key] = ""
        else:
            # If the value is a list, take the first element; otherwise leave it as is.
            if isinstance(result[key], list):
                result[key] = result[key][0] if result[key] else ""
            else:
                output[key] = result[key]
    return result


def generate_publication_metadata(content)->dict:
    llm = OllamaLLM(
        model=METADATA_LLM_MODEL
    )
    prompt_text = """
        You are an expert research analyst. The goal is to create tags for grouping multiple publications on multiple categories.
        Instruction:
            Look at the paper abstract and give me 1-3 keyword based information (like PubMed MeSH term) you can find based on the following categories and return a json formated string: 
            The JSON output should contain the following keys with the instructions/examples below:
              - research_domain: One or two keywords representing the research domain (e.g., "Oncology", "Neuroscience").
              - llm_usage: One or two keywords indicating LLM usage (e.g., "GPT-4").
              - which_deep_learning_usage: Keywords on deep learning usage (e.g., "CNN", "Transformer").
              - which_machine_learning: Keywords for machine learning methods (e.g., "SVM", "RandomForest").
              - datasets: Keywords for dataset names (e.g., "TCGA", "ImageNet").
              - data_category: Keywords describing the data category (e.g., "Genomics", "Radiology").
              - dataset_size: Keywords indicating dataset size (e.g., "Large", "Small").
              - data_type: Keywords for the data type (e.g., "Tabular", "Imaging").
              - specific_algorithms: Keywords for specific algorithms (e.g., "ResNet", "K-means").
              - programming_languages: Keywords for programming languages (e.g., "Python", "R").
              - programming_libraries: Keywords for libraries (e.g., "TensorFlow", "scikit-learn").
              - funding: Keywords indicating funding status (e.g., "NIH", "No funding").
              - timeline: Keywords for timeline (e.g., "Long-term", "Short-term").
              - problem_type: Keywords for the problem type (e.g., "Classification", "Regression").
              - ethical_considerations: Keywords for ethical considerations (e.g., "IRB").
              - type_of_study: Keywords for study type (e.g., "Prospective", "Retrospective").
              - code_and_reproducibility: Keywords indicating code availability or reproducibility (e.g., "Open-source", "Not reproducible").
              - benchmarking: Keywords indicating benchmarking (e.g., "State-of-art", "Baseline").
            If any information does not exist for a key, keep it empty. DO NOT make things up. Give me ONLY ONE keyword per category, DO NOT provide array.

            ENSURE the output is valid JSON.
            {
              "research_domain": "one_or_two_keywords"
            }
        Abstract: """
    prompt_text += content

    raw_response = llm.invoke(prompt_text)
    publication_metadata = extract_json_from_response(raw_response)

    return publication_metadata
