from .matching import *
from .utils import *

def parsed_details(docs_words,section_list):
    section_map={}
    for i in range(len(section_list)):
        if(i==len(section_list)-1):
            start_idx=docs_words.index(section_list[i])
            section_map[section_list[i].capitalize()]=docs_words[start_idx+1:]
        else:
            start_idx=docs_words.index(section_list[i])
            end_idx=docs_words.index(section_list[i+1])
            section_map[section_list[i].capitalize()]=docs_words[start_idx+1:end_idx]
    
    return section_map


def clean(text):
    docs=text.strip()
    docs=remove_special_char(docs)
    docs=remove_extra_space(docs)
    return docs



def parse_resume(text):
    email=extract_email(text)
    number=extract_phone(text)
    links=extract_links(text)
    platform_links=extract_git_linkedin_link(links=links)
    cleaned_docs=clean(text)
    cleaned_docs=remove_links(cleaned_docs)
    name=extract_names(cleaned_docs)
    resume_array=split_based_on_newlines(cleaned_docs)
    
    alpha_word_list=find_section(resume_array)
    
    section_list=section_matching(alpha_word_list)
    details=parsed_details(resume_array,alpha_word_list)
    updated_details=filter_sections(details=details,section_list=section_list)
    final_details=update_section_names(details=updated_details)

    return {
        "name":name,
        "email":email,
        "number":number,
        "linkedin_links":platform_links[0],
        "git_link":platform_links[1],
        "details":final_details
    }