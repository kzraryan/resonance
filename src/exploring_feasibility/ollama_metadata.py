import json
from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model="deepseek-r1:latest"
)

# Directly call the LLM with a single prompt that requests JSON.
prompt_text = """
    You are an expert research analyst. The goal is to create tags for grouping multiple publications on multiple categories.
    Instruction:
        Look at the paper abstract and give me one or two keyword based information (like PubMed MeSH term) you can find based on the following categories and return a json formated string: 
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
        If any information does not exist for a key, keep it empty. DO NOT make things up. 
        
        ENSURE the output is valid JSON.
        {
          "research_domain": "one_or_two_keywords"
        }
    Abstract:
        Background:
        Chemotherapy-induced nausea and vomiting (CINV) are the two most frightful and unpleasant side effects of chemotherapy. CINV is accountable for poor treatment outcomes, treatment failure, or even death. It can affect patients' overall quality of life, leading to many social, economic, and clinical consequences.
        
        Objective:
        This study compared the performances of different data mining models for predicting the risk of CINV among the patients and developed a smartphone app for clinical decision support to recommend the risk of CINV at the point of care.
        
        Methods:
        Data were collected by retrospective record review from the electronic medical records used at the University of Missouri Ellis Fischel Cancer Center. Patients who received chemotherapy and standard antiemetics at the oncology outpatient service from June 1, 2010, to July 31, 2012, were included in the study. There were six independent data sets of patients based on emetogenicity (low, moderate, and high) and two phases of CINV (acute and delayed). A total of 14 risk factors of CINV were chosen for data mining. For our study, we used five popular data mining algorithms: (1) naive Bayes algorithm, (2) logistic regression classifier, (3) neural network, (4) support vector machine (using sequential minimal optimization), and (5) decision tree. Performance measures, such as accuracy, sensitivity, and specificity with 10-fold cross-validation, were used for model comparisons. A smartphone app called CINV Risk Prediction Application was developed using the ResearchKit in iOS utilizing the decision tree algorithm, which conforms to the criteria of explainable, usable, and actionable artificial intelligence. The app was created using both the bulk questionnaire approach and the adaptive approach.
        
        Results:
        The decision tree performed well in both phases of high emetogenic chemotherapies, with a significant margin compared to the other algorithms. The accuracy measure for the six patient groups ranged from 79.3% to 94.8%. The app was developed using the results from the decision tree because of its consistent performance and simple, explainable nature. The bulk questionnaire approach asks 14 questions in the smartphone app, while the adaptive approach can determine questions based on the previous questions' answers. The adaptive approach saves time and can be beneficial when used at the point of care.
        
        Conclusions:
        This study solved a real clinical problem, and the solution can be used for personalized and precise evidence-based CINV management, leading to a better life quality for patients and reduced health care costs.
"""

raw_response = llm(prompt_text)

print("Raw response:", raw_response)
