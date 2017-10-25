import itertools
import networkx as nx
import nltk
import logging
from nltk.tokenize import word_tokenize
import math
from gensim.summarization import summarize
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import KeyedVectors

filename = 'glove/glove.6B.50d.txt.word2vec'
#model = KeyedVectors.load_word2vec_format(filename, binary=False)
# calculate: (king - man) + woman = ?
word = 'house'
sentence = 'home'
#result = model.similarity(word, sentence)


#word_vectors = KeyedVectors.load_word2vec_format(r'GoogleNews-vectors-negative300.bin', binary=True)
#result = word_vectors.similarity('word', 'sentence')


logger = logging.getLogger('BasicLogger')

def similarity(string_1, string_2):
    string_1_ = word_tokenize(string_1)
    string_2_ = word_tokenize(string_2)
    
    string_length_1 = len(string_1_)
    string_length_2 = len(string_2_)
    
    # +1 to avoid no common token problem
    similar_tokens = len(list(set(string_1_).intersection(string_2_)))
    
    similarity = similar_tokens / float(math.log(string_length_1) + math.log(string_length_2))
    return similarity


def build_graph(nodes):
    """Return a networkx graph instance.

    :param nodes: List of hashables that represent the nodes of a graph.
    """
    gr = nx.Graph()  # initialize an undirected graph
    gr.add_nodes_from(nodes)
    nodePairs = list(itertools.combinations(nodes, 2))

    # add edges to the graph (weighted by Levenshtein distance)
    for pair in nodePairs:
        firstString = pair[0]
        secondString = pair[1]
        sim = similarity(firstString, secondString)
        gr.add_edge(firstString, secondString, weight=sim)

    return gr


def extract_sentences(text, summary_length=50, clean_sentences=False, language='english'):

    sent_detector = nltk.data.load('tokenizers/punkt/'+language+'.pickle')
    sentence_tokens = sent_detector.tokenize(text.strip())
    graph = build_graph(sentence_tokens)
    calculated_page_rank = nx.pagerank(graph, weight='weight')
    sentences = sorted(calculated_page_rank, key=calculated_page_rank.get,
                       reverse=True)

    # return a 100 word summary
    summary = ' '.join(sentences)
    summary_words = summary.split()
    summary_words = summary_words[0:summary_length]
    dot_indices = [idx for idx, word in enumerate(summary_words) if word.find('.') != -1]
    if clean_sentences and dot_indices:
        last_dot = max(dot_indices) + 1
        summary = ' '.join(summary_words[0:last_dot])
    else:
        summary = ' '.join(summary_words)
    return summary

def text_summarize_library(text):
    summary = summarize(text, word_count=50)
    return summary

def text_summarize(text):
    doc_dic = []
    summary_dic = dict()
    for i in doc_dic:
        summary = extract_sentences(doc_dic[i])
        summary_dic[i] = summary
    return summary_dic

