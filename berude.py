import re
import time
import sys

import requests
from bs4 import BeautifulSoup

rude_words = [
    "elf-skin",
    "neat’s-tongue",
    "bull’s-pizzle",
    "stock-fish",
    "three-inch fool",
    "unable worm",
    "lily-livered",
    "tewkesbury mustard",
    "pigeon-livered",
    'blackguard',
    "scurvy companion",
    'blaggard',
    'scullions',
    'menial',
    'scoundrel',
    'cox-comb',
    'knave',
    'churl',
    'doxy',
    'glos pautonnier',
    'skamelar',
    'mandrake mymmerkin',
    'hedge-born',
    'cumberground'
]


def find_rude_rhyme(word, cache):
    # takes a word and finds rude rhyme, returns rude subsititue or None if none found
    result = cache.get(word, word)
    if result == word:
        return result
    return f'\x1b[1m{result}\x1b[0m'


def get_all_rhymes(word):
    candidate = (re.sub(r'[^\w]', ' ', word)).split()[-1]
    json_output = requests.get("https://api.datamuse.com/words", params={'rel_rhy': candidate}).json()
    rhyming_words = []
    for rhyme in json_output:
        rhyming_words.append(rhyme['word'])
    return rhyming_words


def get_sonnets():
    result = requests.get("http://lib.ru/SHAKESPEARE/sonnets.txt")
    html = result.content
    soup = BeautifulSoup(html, features="lxml")
    text = soup.get_text()
    textlist = text.split("\n")
    textiter = iter(textlist)
    sonnet = False
    while not sonnet:
        line = next(textiter)
        if "Sonnet " in line:
            sonnet = True
    next(textiter)
    return textiter

def load_sonnet(textiter):
    poem = []
    while True:
        line = next(textiter)
        if "Sonnet " not in line:
            poem.append(line)
        else:
            break
    poem.pop()

    poemsplit = [x.split(" ") for x in poem if x.strip()]
    return poemsplit


def replace_words(sonnet, cache):
    for ix, line in enumerate(sonnet):
        word = line[-1][:-1]
        rude_version = find_rude_rhyme(word, cache)

        sonnet[ix][-1] = rude_version + line[-1][-1]
    return sonnet


def main():
    textiter = get_sonnets()
    # print(re quests.get("https://api.datamuse.com/words", params={'rel_rhy': 'cat'}).json())
    print("PRECACHING...")
    cache = {}
    for word in rude_words:
        for rhyme in get_all_rhymes(word):
           cache[rhyme] = word

    while True:
        print("---")
        sonnet = load_sonnet(textiter)
        rude_sonnet = replace_words(sonnet, cache)
        joined = "\n".join(" ".join(l) for l in rude_sonnet)
        if '\x1b' in joined:
            print(joined)
            input()


if __name__ == '__main__':
    sys.exit(main())
