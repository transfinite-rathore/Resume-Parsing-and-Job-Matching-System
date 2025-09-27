from transformers import pipeline
from .utils import combine_data


    
    
def summarize_data(combine_chunk:str):
    # print(combine_chunk)
    # print("------------------------------------")
    formatted_resume = """
        Education:
        - B.Tech in Computer Science Engineering, GLA University (2019–Present)
        - Intermediate, Sacred Heart School, CBSE (2016–2018)

        Experience:
        - ML Trainee, Internshala (06/2021 – 07/2022)
        - TensorFlow 2 Training, Coursera (05/2021 – 06/2021)

        Projects:
        - SVHN housing number classification using CNN vs MLP
        - Titanic dataset classification with 5 ML models

        Skills:
        Python, Java, SQL, TensorFlow, Machine Learning, Deep Learning

        Achievements:
        Gold badge in Python (HackerRank), HackWithInfy finalist, SIH 2022
        """
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(formatted_resume, max_length=400, min_length=40)
    return summary