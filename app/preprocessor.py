import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def pre_processor(input_sentence):
    nltk.download('stopwords')
    nltk.download('punkt')
    stop_words = set(stopwords.words('portuguese'))
    input_sentence_tokens = word_tokenize(input_sentence.lower())
    input_sentence_tokens = [word for word in input_sentence_tokens if word.isalnum() and word not in stop_words]
    input_sentence = ' '.join(input_sentence_tokens)
    return input_sentence