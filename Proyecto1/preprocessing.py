# Instalación de librerias
import pandas as pd
import numpy as np
import sys
import nltk
import re, string, unicodedata
#import contractions
import inflect
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer

from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer
from eli5.sklearn import InvertableHashingVectorizer
from joblib import load
# librería Natural Language Toolkit, usada para trabajar con textos 
import nltk
def remove_non_ascii(words):
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words

def to_lowercase(words):
    new_words = []
    for word in words:
        new_words.append(word.lower())
    return new_words

def remove_punctuation(words):
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

def replace_numbers(words):
    p = inflect.engine()
    new_words = []
    for word in words:
      try:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)
      except:
        pass
    return new_words

def remove_stopwords(words):
    stop_words = set(stopwords.words('english'))
    new_words = []
    for word in words:
      if word not in stop_words:
        new_words.append(word)
    return new_words

def preprocessing(w):
    words = w.split(" ")
    words = to_lowercase(words)
    words = replace_numbers(words)
    words = remove_stopwords(words)
    words = remove_punctuation(words)
    words = remove_non_ascii(words)
    return words

def stem_words(words):
  stemmer = LancasterStemmer()
  stems = []
  for word in words:
      stem = stemmer.stem(word)
      stems.append(stem)
  return stems
"""Stem words in list of tokenized words"""

def lemmatize_verbs(words):
  lemmatizer = WordNetLemmatizer()
  lemmas = []
  for word in words:
      lemma = lemmatizer.lemmatize(word, pos='v')
      lemmas.append(lemma)
  return lemmas

"""Lemmatize verbs in list of tokenized words"""

def stem_and_lemmatize(words):
    stems = stem_words(words)
    lemmas = lemmatize_verbs(stems)
    return lemmas
def process(string):
    pp = preprocessing(string)
    pp = stem_and_lemmatize(pp)
    tokenizador = load("html/static/assets/tokenizador.joblib")
    
    df = pd.DataFrame([string], columns=["processed"])
    data = tokenizador.fit_transform(df["processed"])
    return data