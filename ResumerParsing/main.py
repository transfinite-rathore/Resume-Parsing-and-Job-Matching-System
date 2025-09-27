# from DataIngestion import read_pdf
from .DataIngestion import read_pdf
from .parsing import parse_resume
from .preprocessing import combine_text
# from cleaning import remove_stop_word
from .summarization import combine_data,summarize_data
from .encodding import *






resume_path=r"C:\Users\swata\OneDrive\Desktop\Python AI Project\ResumeParser\app\public\191550086_Swatantra_GLA_University.pdf"

# resume_docs=read_pdf(resume_path)
# # print(resume_docs)
# # print("--------------------------------------------------------------------------------")
# extracted_details=parse_resume(resume_docs)
# print(extracted_details)

def extracted_clean_resume(extracted_details):
    for i in extracted_details["details"].keys():
        combined_text=combine_text(extracted_details["details"][i]).lower()
        extracted_details["details"][i]=remove_stop_word(combined_text)
    return extracted_details


# extracted_data=extracted_clean_resume(extracted_details)
# combined_chunk_to_summarize=combine_data(extracted_data)

# job_description = """We are looking for a Machine Learning Engineer with experience in Python , SQL , AWS , and deploying deep learning models using TensorFlow ."""

def parsed_resume_details(resume_path):
    resume_docs=read_pdf(resume_path)
    extracted_details=parse_resume(resume_docs)
    return extracted_details

def resume_parsing(resume_path,job_desc):
    resume_docs=read_pdf(resume_path)
    extracted_details=parse_resume(resume_docs)
    extracted_data=extracted_clean_resume(extracted_details)
    combined_chunk_to_summarize=combine_data(extracted_data)


    matched_word_score=score_by_matched_keywords(job_desc,combined_chunk_to_summarize)
    encoded_score=encoding_score(job_desc,combined_chunk_to_summarize)
    return matched_word_score,encoded_score

# print(parsed_resume_details(resume_path))
# summary=summarize_data(combined_chunk_to_summarize)
# print(summary)
