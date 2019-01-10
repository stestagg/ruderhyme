import re
import sys
import requests

rude_words = [
    "elf-skin",
    "neat’s-tongue",
    "bull’s-pizzle",
    "stock-fish",
    "three-inch fool",
    "unable worm",
    "lily-livered",
    "Tewkesbury mustard",
    "pigeon-livered",
    "scurvy companion"
]

def find_rude_rhyme(word, cache):
   # takes a word and finds rude rhyme, returns rude subsititue or None if none found
   return cache.get(word, word)

def get_all_rhymes(word):
    candidate = (re.sub(r'[^\w]', ' ', word)).split()[-1]
    json_output = requests.get("https://api.datamuse.com/words", params={'rel_rhy': candidate}).json()
    rhyming_words = []
    for rhyme in  json_output:
        rhyming_words.append(rhyme['word'])
    return rhyming_words

def main():
    # print(re quests.get("https://api.datamuse.com/words", params={'rel_rhy': 'cat'}).json())
    cache = {}
    for word in rude_words:
        for rhyme in get_all_rhymes(word):
            cache[rhyme] = word
    print(cache)
    sonnett = load_sonnett(cache)
    




if __name__ == '__main__':
    sys.exit(main())