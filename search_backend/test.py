import re
from iRnWsLeo.search_backend.create_index import index_files

test_string = "How much wood could a wood chuck chuck if a wood chuck would chuck wood"
search_word = "wood"

for match in re.finditer('([^ ]*? |)%s( [^ ]*|)' % search_word, test_string):
    print("entire match: %s" % match.group(0))
    print("prev word: %s" % match.group(1))
    print("next word: %s" % match.group(2))


for key, value in index_files().items():
    print(key, value)