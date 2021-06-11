import pandas as pd
from matplotlib import pyplot as plt
import json
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
nltk.download('stopwords')
stemmer = SnowballStemmer("english")

nltk.download('stopwords')
tokenizer = nltk.tokenize.WhitespaceTokenizer()
wnl = WordNetLemmatizer()

mystop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", 
                "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", 
                "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", 
                "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", 
                "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", 
                "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", 
                "after", "above", "below", "to", "from", "in", "out", "on", "off", "over", "under", 
                "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", 
                "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", 
                "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

def normalized_text(text):
    if text.endswith('.'):
        text = text[:-1]
    return text.lower().strip()

def lemmatize_text_keep_sw(text):
    return [stemmer.stem(word) for word in tokenizer.tokenize(text)]

def lemmatize_text(text):
    if len([stemmer.stem(word) for word in tokenizer.tokenize(text) if word not in mystop_words]) == 0:
        print(text)
    return [stemmer.stem(word) for word in tokenizer.tokenize(text) if word not in mystop_words]

def reject(word_list, sentence):
    return word_found(word_list, sentence) | word_found_instruction(word_list)

def word_found(word_list, sentence):
    num=0
    # the intuition is that if the word overlap is one, it's considered as invalid answer only if the answer itself is only one word.
    sentence = " "+sentence
    for w in word_list:
        if ' '+w+' ' in sentence:
            num+=1
    if num == 1 and len(word_list) ==1:
        return True
    elif num>=2:
        print(word_list, sentence)
        return True
    else:
        return False


def word_found_instruction(word_list):
    words = " ".join(word_list)
    if "easily answered" in words:
        return True
    if "relevant question grammatically" in words:
        return True
    if "grammatically incorrect" in words:
        return True
    if "answer question" in words:
        return True
    if "find question valid" in words:
        return True
    if "context sentences" in words:
        return True
    sentence = "The goal is to generate a set of questions that are not explicitly answered in the context sentences but can be answered easily by humans using their commonsense or general understanding of the World. We are trying to assess if our question is valid for the given context based on below mentioned criteria. In this task, you will be answering if the question is valid by a 'Yes', 'No', or 'Maybe'. In case you do not find the question valid, you will be required to write a question that meets the criteria discussed below. If the question seems ok, you will be required to provide a word or short phrase as an answer."
    if words in sentence.lower():
        print(words)
        return True
    return False
