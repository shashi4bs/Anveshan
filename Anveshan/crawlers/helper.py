import re
from config import PAGE_CONTENT_LENGTH
from bs4 import BeautifulSoup

def replace_special_chars(text):
    special_chars = ['@', '[', ']', '(', ')', '-', '_']
    for spl_chr in special_chars:
        text = text.replace(spl_chr, '')
    return text



def filter_text_from_content(page, query):
    content = "".join(page["content"])
    #print(query.query)
    pattern = re.compile(query.query, re.IGNORECASE)
    content = content.strip()
    first_line = None
    text = None
    for line in content.split("."):
        if not first_line:
            if len(line) > PAGE_CONTENT_LENGTH:
                first_line = line[:PAGE_CONTENT_LENGTH] + "..."
            first_line = line
        text = pattern.search(line)
        if text:
            if len(line) > PAGE_CONTENT_LENGTH:
                line = line[:PAGE_CONTENT_LENGTH] + "..."
            return line
    return first_line

def processBody(body):
    #strip html tags
    content = strip_html_tags(body)
    #strip whitespaces
    content = content.strip()
    #replace \n by <space>
    content = content.replace('\n', ' ')
    #replace special chars
    content = replace_special_chars(content)
    content = content.strip()

    index = {}
    for c in content.split(' '):
        if c not in index:
            index[c] = 1
        else:
            index[c] += 1
    #print(index)
    return index
