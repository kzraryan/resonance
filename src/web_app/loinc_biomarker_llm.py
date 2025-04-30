import re
import pandas as pd
from utils.constants import VECTOR_EMBED_MODEL, LOINC_VECTOR_DATABASE_NAME, QDRANT_URL, METADATA_LLM_MODEL
from langchain_ollama import OllamaLLM

def parse_think_and_number(text: str):
    """
    Extracts the text inside <think>...</think> and the number that follows.
    Returns (inside_think, number_as_float) or (None, None) if no match is found.
    """
    pattern = re.compile(r"<think>(.*?)</think>\s*([\d.]+)", flags=re.DOTALL)
    match = pattern.search(text)
    print(match)
    if match:
        inside_think = match.group(1).strip()
        number_str = match.group(2).strip()
        return inside_think, float(number_str)
    return None, None

def generate_publication_metadata(content):
    llm = OllamaLLM(
        model=METADATA_LLM_MODEL
    )
    prompt_text = """
        You are an expert medical laboratory coding expert. The goal is to provide user a confidence level between 0 to 1 of
         how likely given LOINC is needed to calculate the given BIOMARKER.
         The user will provide LOINC and BIOMARKER, your response SHOULD ONLY BE A NUMBER between 0 to 1."""

    prompt_text += content

    raw_response = llm.invoke(prompt_text)

    return raw_response

bm = 'loinc_biomarker_match.csv'
bm_df = pd.read_csv(bm)

df = bm_df[bm_df['SCORE'] > 0.62]
df['LLM_REASON'] = ''
df['LLM_SCORE'] = 0.0

counted = 0
df = df.reset_index(drop=True)
for index, row in df.iterrows():
    print(f'Processing {index} of {len(df)}')
    llm_result = generate_publication_metadata(f'LOINC:{row["LONG_COMMON_NAME"]}  BIOMARKER:{row["BIOMARKER"]}')
    print(llm_result)
    reason, score = parse_think_and_number(llm_result)
    # print(reason, score)
    df.loc[index,'LLM_REASON'] = reason if reason else llm_result
    df.loc[index,'LLM_SCORE'] = score
    counted+=1
    # if counted >5:
    #     break

df.to_csv('loinc_biomarker_llm2.csv', index=False)