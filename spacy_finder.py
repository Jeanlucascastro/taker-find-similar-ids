import spacy


def encontrar_frases_similares(frase_entrada, frases_banco_dados):
    # Carregar o modelo do idioma
    nlp = spacy.load("pt_core_news_sm")

    # Processar a frase de entrada
    doc1 = nlp(frase_entrada)

    # Processar as frases do banco de dados e calcular a similaridade
    resultados = []
    for frase in frases_banco_dados:
        doc2 = nlp(frase)
        similaridade = doc1.similarity(doc2)
        resultados.append((frase, similaridade))

    # Ordenar os resultados por similaridade
    resultados = sorted(resultados, key=lambda x: x[1], reverse=True)

    # Retornar os resultados
    return resultados
