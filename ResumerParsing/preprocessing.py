import re


def combine_text(words_array):
    details=""
    for i in words_array:
        details+=i+" "  
    return details.strip()