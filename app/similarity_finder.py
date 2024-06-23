from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def find_similar(input_sentence, num_similar=5, data_db=[]):
    # data = ["Eu gosto do bolsonaro", "Eu gosto do lula", "Eu gosto de banana", "Eu gosto de fumar", "Eu odeio Bolsonaro"]
    stop_words = set(stopwords.words('portuguese'))
    corpus = []
    for sentence in data_db:
        sentence_tokens = word_tokenize(sentence.lower())
        sentence_tokens = [word for word in sentence_tokens if word.isalnum() and word not in stop_words]
        sentence = ' '.join(sentence_tokens)
        corpus.append(sentence)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    input_sentence_tokens = word_tokenize(input_sentence.lower())
    input_sentence_tokens = [word for word in input_sentence_tokens if word.isalnum() and word not in stop_words]
    input_sentence = ' '.join(input_sentence_tokens)
    input_vector = vectorizer.transform([input_sentence])

    cosine_similarities = cosine_similarity(input_vector, tfidf_matrix).flatten()
    related_docs_indices = cosine_similarities.argsort()[::-1]

    most_similar_sentences = []
    similarity_scores = []
    for i in range(num_similar):
        most_similar_sentence = data_db[related_docs_indices[i]]
        similarity_score = cosine_similarities[related_docs_indices[i]]
        most_similar_sentences.append(most_similar_sentence)
        similarity_scores.append(similarity_score)

    return most_similar_sentences, similarity_scores