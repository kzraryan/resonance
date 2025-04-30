import pandas as pd

bm = 'loinc_biomarker_llm2.csv'
bm_df = pd.read_csv(bm)

mask = bm_df["LLM_SCORE"].isna()

bm_df.loc[mask, "LLM_SCORE"] = (
    bm_df.loc[mask, "LLM_REASON"]
    .str.strip()  # Remove trailing spaces/newlines
    .str.extract(r'(\d+(?:\.\d+)?$)', expand=False)  # Capture trailing float
    .astype(float)
)
print(bm_df.loc[mask])

bm_df.to_csv('loinc_biomarker_llm3.csv', index=False)