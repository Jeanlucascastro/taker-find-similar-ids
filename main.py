from flask import Flask, request, jsonify
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from spacy_finder import encontrar_frases_similares

app = Flask(__name__)


@app.route('/encontrar', methods=['POST'])
def minha_funcao():
    data = request.get_json()
    minha_string = data['minha_string']

    input_sentence = pre_processor(
        minha_string)  # chamando a função preProcessar() passando a string recebida como argumento
    # Aqui você pode fazer o processamento desejado com a string pré-processada

    data = ["Eu gosto do bolsonaro", "Eu gosto do lula", "Eu gosto de banana", "Eu gosto de fumar",
            "Eu odeio Bolsonaro"]
    resultados = encontrar_frases_similares(input_sentence, data)

    # Exibir os resultados
    for resultado in resultados:
        print(resultado[0])

    similar_encontrado = find_similar(input_sentence)
    response_data = {'mensagem': 'String recebida: ' + minha_string + '. String pré-processada: ' + input_sentence}

    print("string")
    for elemento in similar_encontrado:
        print(elemento)

    return jsonify(response_data)


def pre_processor(input_sentence):
    nltk.download('stopwords')
    nltk.download('punkt')
    stop_words = set(stopwords.words('portuguese'))
    input_sentence_tokens = word_tokenize(input_sentence.lower())
    input_sentence_tokens = [word for word in input_sentence_tokens if word.isalnum() and word not in stop_words]
    input_sentence = ' '.join(input_sentence_tokens)
    return input_sentence


def find_similar(input_sentence, num_similar=5):
    data = ["Eu gosto do bolsonaro", "Eu gosto do lula", "Eu gosto de banana", "Eu gosto de fumar",
            "Eu odeio Bolsonaro"]
    stop_words = set(stopwords.words('portuguese'))
    corpus = []
    for sentence in data:
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
        most_similar_sentence = data[related_docs_indices[i]]
        similarity_score = cosine_similarities[related_docs_indices[i]]
        most_similar_sentences.append(most_similar_sentence)
        similarity_scores.append(similarity_score)

    return most_similar_sentences, similarity_scores


if __name__ == '__main__':
    app.run()
