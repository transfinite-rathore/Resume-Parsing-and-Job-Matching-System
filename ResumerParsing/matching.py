from .config import resume_sections,section_keywords

def section_matching(section_list):
    final_section=[]
    for i in section_list:
        section=i.split(" ")
        for words in section:
            if words.lower() in resume_sections:
                final_section.append(i.capitalize())
                break
    return final_section

def filter_sections(details,section_list):
    final_details={}
    for section_name,content in details.items():
        if section_name in section_list:
            final_details[section_name]=content
    return final_details

def update_section_names(details:dict):
    final_details={}
    for section_name,content in details.items():
        words=set(section_name.lower().split())
        for section,keyword in section_keywords.items():
            if(words & set(keyword)):
                final_details[section.capitalize()]=content
                break
    return final_details
        