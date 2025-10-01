from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from .utils import *
import spacy

nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer('all-MiniLM-L6-v2') 

def score_by_matched_keywords(job_description,resume):
    matched_words=0
    job_description=remove_special_char(job_description)
    job_description=remove_stop_word(job_description)
    doc = nlp(job_description)
    total_words=0
    for token in doc:
        
        if(token.pos_!="PRON"):
            if(token.text.lower() in resume):
                matched_words+=1
            total_words+=1

    return (matched_words/total_words)*100
    

def encoding_score(job_description,resume):
    
    resume_encoding=model.encode(resume)
    job_description_encoding=model.encode(job_description)

    similarity_score = cosine_similarity([resume_encoding], [job_description_encoding])[0][0]
    ats_score = round(similarity_score * 100, 2)
    return ats_score
