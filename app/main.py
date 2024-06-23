from flask import Blueprint, request, jsonify
from app.preprocessor import pre_processor
from app.similarity_finder import find_similar
from app.spacy_finder import encontrar_frases_similares
# from db import fetch_data_from_db

minha_funcao = Blueprint('minha_funcao', __name__)

@minha_funcao.route('/encontrar', methods=['POST'])
def encontrar():
    data = request.get_json()
    minha_string = data['minha_string']

    frases_banco_dados = [
    {"phrase": "Eu gosto do bolsonaro", "messageId": 1},
    {"phrase": "Eu gosto do lula", "messageId": 2},
    {"phrase": "Eu gosto de banana", "messageId": 3},
    {"phrase": "Eu gosto de fumar", "messageId": 4},
    {"phrase": "Eu odeio Bolsonaro", "messageId": 5}
    ]
    # query = f"SELECT frase FROM tabela WHERE condicao = '{data}'"  # Substitua pela sua consulta SQL real

    # db_results = fetch_data_from_db(query)

    # if db_results:
    #     frases_banco_dados = [result['frase'] for result in db_results]
    # else:
    #     frases_banco_dados = []

    input_sentence = pre_processor(minha_string)
    resultados = encontrar_frases_similares(input_sentence, frases_banco_dados)
    resultados_tfidf, _ = find_similar(input_sentence, frases_banco_dados)

    response_data = {'mensagem': f'String recebida: {minha_string}. String pré-processada: {input_sentence}'}
    print(resultados)
    return jsonify(resultados)
