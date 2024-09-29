from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def find_similar(input_sentence, data_db, num_similar=5):
    print(data_db)
    # data = ["Eu gosto do bolsonaro", "Eu gosto do lula", "Eu gosto de banana", "Eu gosto de fumar", "Eu odeio Bolsonaro"]
    stop_words = set(stopwords.words('portuguese'))
    corpus = []
    for item in data_db:
        sentence = item["cutedMessage"]
        sentence_tokens = word_tokenize(sentence.lower())
        sentence_tokens = [word for word in sentence_tokens if word.isalnum() and word not in stop_words]
        cleaned_sentence = ' '.join(sentence_tokens)
        corpus.append(cleaned_sentence)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    input_sentence_tokens = word_tokenize(input_sentence.lower())
    input_sentence_tokens = [word for word in input_sentence_tokens if word.isalnum() and word not in stop_words]
    input_sentence_cleaned = ' '.join(input_sentence_tokens)
    input_vector = vectorizer.transform([input_sentence_cleaned])

    cosine_similarities = cosine_similarity(input_vector, tfidf_matrix).flatten()
    related_docs_indices = cosine_similarities.argsort()[::-1]

    most_similar_sentences = []
    similarity_scores = []
    for i in range(min(num_similar, len(data_db))):
        index = related_docs_indices[i]
        most_similar_sentence = data_db[index]["cutedMessage"]
        message_id = data_db[index]["messageId"]
        similarity_score = cosine_similarities[index]
        most_similar_sentences.append((message_id, most_similar_sentence))
        similarity_scores.append(similarity_score)

    return most_similar_sentences, similarity_scores