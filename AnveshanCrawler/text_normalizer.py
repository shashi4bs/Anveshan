import contractions
from bs4 import BeautifulSoup
import unicodedata
import re
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.stem import PorterStemmer
import string
tokenizer = ToktokTokenizer()
stopword_list = nltk.corpus.stopwords.words('english')


def strip_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    [s.extract() for s in soup(['iframe', 'script'])]
    stripped_text = soup.get_text()
    stripped_text = re.sub(r'[\r|\n|\r\n]+', '\n', stripped_text)
    return stripped_text

def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

def expand_contractions(text):
    return contractions.fix(text)

def remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    return text

def remove_stopwords(text, is_lower_case=False):
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text

def normalize_corpus(corpus, html_stripping=True, contraction_expansion=True,
                     accented_char_removal=True, text_lower_case=True,
                     text_lemmatization=True, special_char_removal=True,
                     stopword_removal=True, remove_digits=True):
    normalized_corpus = []
    # normalize each document in the corpus
    for doc in corpus:
        # strip HTML
        if html_stripping:
            doc = strip_html_tags(doc)
        # remove accented characters
        if accented_char_removal:
            doc = remove_accented_chars(doc)
        # expand contractions
        if contraction_expansion:
             doc = expand_contractions(doc)
        # lowercase the text
        if text_lower_case:
            doc = doc.lower()
        # remove extra newlines
        doc = re.sub(r'[\r|\n|\r\n]+', ' ',doc)
        # lemmatize text
        #if text_lemmatization:
        #doc = lemmatize_text(doc)
        # remove special characters and\or digits
        if special_char_removal:
            # insert spaces between special characters to isolate them
            special_char_pattern = re.compile(r'([{.(-)!}])')
            doc = special_char_pattern.sub(" \\1 ", doc)
            doc = remove_special_characters(doc, remove_digits=remove_digits)
        # remove extra whitespace
        doc = re.sub(' +', ' ', doc)
        # remove stopwords
        if stopword_removal:
            doc = remove_stopwords(doc, is_lower_case=text_lower_case)
        normalized_corpus.append(doc)
    return [n.split() for n in normalized_corpus]


class Tokenizer(object):
    
    def __init__(self):
        self.tokenizer = ToktokTokenizer()
        self.stemmer = PorterStemmer()
        self.stopwords = nltk.corpus.stopwords.words('english')


    def processItem(self, content, removeStopWords=True):
        self.content = content.strip()
        self.tokens = self.tokenizer.tokenize(content)
        filtered_tokens = self.__removeStopWords()
        filtered_tokens = self.__removeSpecialChars(filtered_tokens)
        #perfrom stemming
        filtered_tokens = self.__token_stemming(filtered_tokens)
        self.filtered_tokens = self.__get_frequency(filtered_tokens)
        return self.filtered_tokens

    def __removeStopWords(self, is_lower_case=False):
        tokens = [token.strip() for token in self.tokens]
        if is_lower_case:
            filtered_tokens = [token for token in tokens if token not in self.stopwords]
        else:
            filtered_tokens = [token for token in tokens if token.lower() not in self.stopwords]
        #filtered_text = ' '.join(filtered_tokens)
        return filtered_tokens

    def __removeSpecialChars(self, filtered_tokens):
        punctuation_remover =  str.maketrans(dict.fromkeys(string.punctuation))
        special_chars = ['(', ')', '[', ']', '"', "'", ".", ","]
        print("type filtereed tokens", type(filtered_tokens))
        processed = []
        for token in filtered_tokens:
            if token not in special_chars:
                token = token.translate(punctuation_remover)
                token = token.strip()
                processed.append(token)
        return processed

    def __get_frequency(self, tokens):
        filtered_tokens = dict()
        for index in tokens:
            if index not in filtered_tokens.keys():
                filtered_tokens[index] = 1
            else:
                filtered_tokens[index] += 1

        return filtered_tokens

    def __token_stemming(self, tokens):
       return [self.stemmer.stem(token) for token in tokens] 
