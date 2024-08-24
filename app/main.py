from flask import Blueprint, request, jsonify
from app.preprocessor import pre_processor
from app.similarity_finder import find_similar
from app.spacy_finder import encontrar_frases_similares
from app.db import fetch_data_from_db

minha_funcao = Blueprint('minha_funcao', __name__)

@minha_funcao.route('/encontrar', methods=['POST'])
def encontrar():
    data = request.get_json()
    minha_string = data['minha_string']
    node_message_id = data.get('node_message_id')

    # frases_banco_dados = [
    # {"cuted_message": "Eu gosto do bolsonaro", "message_id": 1},
    # {"cuted_message": "Eu gosto do lula", "message_id": 2},
    # {"cuted_message": "Eu gosto de banana", "message_id": 3},
    # {"cuted_message": "Eu gosto de fumar", "message_id": 4},
    # {"cuted_message": "Eu odeio Bolsonaro", "message_id": 5}
    # ]

    # Query para buscar dados no banco de dados
    query = f"""
        SELECT cm.cuted_message, cm.message_id
        FROM cut_message cm
        JOIN cut_node_message cnm ON cm.id = cnm.cut_message_id
        WHERE cnm.node_message_id = {node_message_id}
        AND cm.deleted = false;
    """

    frases_banco_dados = fetch_data_from_db(query)
    print(frases_banco_dados)


    input_sentence = pre_processor(minha_string)
    resultados = encontrar_frases_similares(input_sentence, frases_banco_dados)
    resultados_tfidf, _ = find_similar(input_sentence, frases_banco_dados)

    response_data = {'mensagem': f'String recebida: {minha_string}. String pré-processada: {input_sentence}'}
    print(resultados)
    return jsonify(resultados)
