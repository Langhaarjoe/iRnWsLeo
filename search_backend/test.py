from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
stemmer = EnglishStemmer()
stopwords = set(stopwords.words('english'))

document = {}
document_words = {}

character_list = [',',';',':','(',')','&','/','{','}','[',']','-','_','.']

with open('test.txt', 'r') as g:
    text = g.read()
    document[0] = text

for id in document:
    word_list = word_tokenize(document[id])
    swap_list = []
    for token in word_list:
        token = stemmer.stem(token)
        if (token in stopwords) or (token in character_list):
            continue
        swap_list.append(token)
    document_words[0] = swap_list

print(document_words)
