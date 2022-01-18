import re
import nltk
import string
from nltk.corpus import stopwords
from pymystem3 import Mystem


nltk.download('stopwords')
rs = stopwords.words('russian')
rs.extend(['…', '«', '»', '...'])


def remove_punctuation(text: str) -> str:
    return ''.join([ch if ch not in string.punctuation else ' ' for ch in text])


def remove_numbers(text: str) -> str:
    return ''.join([ch if not ch.isdigit() else ' ' for ch in text])


def remove_row(text: str) -> str:
    return text.replace(r'\r', '').replace(r'\n', '')


def remove_spaces(text: str) -> str:
    return re.sub(r'\s+', ' ', text, flags=re.I)


def lemmatize_text(text: str) -> str:
    """
    Лемматизация текста, т.е начальные слова забуду -> забывать
    """
    mystem = Mystem()
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in rs and token != " "]
    text = " ".join(tokens)
    return text

def make_correct(text: str) -> str:
    """Применить все методы для подготовки текста"""
    text = remove_spaces(remove_numbers(remove_row(remove_punctuation(text.lower()))))
    return lemmatize_text(text)