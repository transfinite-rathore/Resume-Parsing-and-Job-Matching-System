import re
from nltk.corpus import stopwords
import spacy

nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words('english'))

def extract_names(text):
    names=text.replace("\n"," ").split(" ")[:2]
    return f'{names[0]} {names[1]}'


def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group() if match else None

def extract_phone(text):
    match = re.search(r'\+91[\s-]*\d{10}', text)
    return match.group() if match else None

def extract_links(text):
    return re.findall(r'(\S*\.com/\S*)', text)

def extract_git_linkedin_link(links:list):
    git_link=""
    linkedin_link=""
    for i in links:
        if(("linkedin.com" in i) and len(linkedin_link)==0):
            linkedin_link=i
        elif(("github.com" in i) and len(git_link)==0):
            matched_link=re.match(r"(https://github\.com/[^/]+/)", i)
            if(matched_link):
                git_link=matched_link.group(1)
        else:
            continue
        if(len(git_link)!=0 and len(linkedin_link)!=0):
            break
    return (linkedin_link,git_link)

def remove_links(text):
    return re.sub(r'(https?://[^\s]+|www\.[^\s]+)'," ",text)

def remove_extra_space(text):
    return re.sub(r" +"," ",text)

def remove_special_char(text):
    return re.sub(r"[&*./(),%$#@!_-]",' ', text)


def remove_stop_word(text):
    final_text=""
    for i in text.split():
        if i not in stop_words:
            final_text+=i+" "
    return final_text

def split_based_on_newlines(text):
    return [i.strip() for i in text.split("\n") if len(i)>2]

def combine_text(words_array):
    details=""
    for i in words_array:
        details+=i+" "  
    return details.strip()

def combine_data(text:dict):
    chunk_to_summarize=""
    for i in text["details"].keys():
        chunk_to_summarize+=text["details"][i]+" "
    return chunk_to_summarize

def find_section(text):
    return [i for i in text if i.isupper() and len(i)>2]