def bm25(query, document, index):
    average_d = 0
    k = 1.2
    b = 0.75
    scores = []
    for i in query:
        average_d += index[i][document]['length']
    average_d = average_d / len(query)
    tmp_scores = []
    for i in query:
        upper = index[i]['idf']*index[i][document]*(k+1)
        lower = index[i][document]+k*(1-b+(b*(index[i][document]['length']/average_d)))
        tmp_scores.append(upper/lower)
    return (sum(tmp_scores))


def bm25_lib():
    """
    gensim library has a bm25 modul which can be used
    :return:
    """
    pass