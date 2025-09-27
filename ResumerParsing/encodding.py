from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from .utils import *
import spacy

nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast and effective
# model = SparseEncoder("naver/splade-cocondenser-ensembledistil")

def score_by_matched_keywords(jd,resume):
    matched_words=0
    jd=remove_special_char(jd)
    jd=remove_stop_word(jd)
    # pos_tags = pos_tag(jd)
    doc = nlp(jd)
    total_words=0
    for token in doc:
        
        if(token.pos_!="PRON"):
            if(token.text.lower() in resume):
                # print(f"{token.text.lower()}: {token.pos_}")
                matched_words+=1
            total_words+=1

    return (matched_words/total_words)*100
    



# formatted_resume = """
#         Education:
#         - B.Tech in Computer Science Engineering, GLA University (2019–Present)
#         - Intermediate, Sacred Heart School, CBSE (2016–2018)

#         Experience:
#         - ML Trainee, Internshala (06/2021 – 07/2022)
#         - TensorFlow 2 Training, Coursera (05/2021 – 06/2021)

#         Projects:
#         - SVHN housing number classification using CNN vs MLP
#         - Titanic dataset classification with 5 ML models

#         Skills:
#         Python, Java, SQL, TensorFlow, Machine Learning, Deep Learning

#         Achievements:
#         Gold badge in Python (HackerRank), HackWithInfy finalist, SIH 2022
#         """

job_description = """We are looking for a Machine Learning Engineer with experience in Python , SQL , AWS , and deploying deep learning models using TensorFlow ."""


def encoding_score(jd,resume):
    
    resume_encoding=model.encode(resume)
    jd_encoding=model.encode(jd)

    similarity_score = cosine_similarity([resume_encoding], [jd_encoding])[0][0]
    ats_score = round(similarity_score * 100, 2)
    return ats_score

# print(score_by_matched_keywords(job_description,formatted_resume.lower()))
# print("All good")
