import re
import json
from enum import Enum


CHANDA_STR = "यमाता राजभान सलगं"
SEPERATOR_CHARS = " -,;१२३४५६७८९०'\""
CHANDA_DATA_FILE = 'app/data/standard_names.json'


class Swor(Enum):
    LONG = 'S'
    SHORT = 'I'
    ANY = 'X'

    def __str__(self):
        return self.value

    def __equals__(self,other):
        if self.value == other.value:
            return True
        if self is Swor.ANY or other is Swor.ANY:
            return True
        return False


class Chars(Enum):
    IGNORE = 0
    SHORT1 = 1
    SHORT2 = 2
    LONG = 3
    LONG_ADD = 4
    SHORT_ADD = 5
    SHORT_SUB = 6
    UNKNOWN = -1


def categorize(char):
    chars = [
        SEPERATOR_CHARS, "कखगघङ चछजझञ टठडढण तथदधन पफबभम यरलव शषस ह", "अइउऋ",
        "आईएऐओऔऊ", "ाीेैोौूंः:!।", "िुँ", "्"
    ]
    for i, cs in enumerate(chars):
        if char in cs:
            return Chars(i)
    return Chars.UNKNOWN


def tokenize(word):
    cat = (categorize(c) for c in word)
    token = []
    for c in cat:
        count = len(token)
        if c is Chars.SHORT1 or c is Chars.SHORT2:
            token.append(Swor.SHORT)
        elif c is Chars.LONG:
            token.append(Swor.LONG)
        elif c is Chars.LONG_ADD:
            if count > 0:
                token[count - 1] = Swor.LONG
            else:
                pass  # error
        elif c is Chars.SHORT_ADD:
            pass
        elif c is Chars.SHORT_SUB:
            if count > 1:
                token.pop()
                token[count - 2] = Swor.LONG
            else:
                token.pop()
    return token


def extract_words(line):
    return re.split('|'.join(SEPERATOR_CHARS), line)


def tokenize_line(line, word_by_word=False):
    line = line.strip()
    if len(line) == 0 or line[0] == '#':
        return []

    words = extract_words(line)
    if word_by_word:
        token = tuple(map(tokenize,
                          words))
        if len(words)>0 and len(token[-1])>0:
            token[-1][-1] = Swor('S')
        return token
    
    token = []
    for word in words:
            token += tokenize(word)
    if len(token)>0:
        token[-1] = Swor('S')
    return token


def token_string(token):
    return ''.join([str(t) for t in token])


def get_chanda_name(rule):
    with open(CHANDA_DATA_FILE,'r') as r:
        names = json.load(r)
    return names.get(rule,'UNKNOWN')


if __name__ == '__main__':
    print("String: ", CHANDA_STR)
    print("Swors: ", token_string(tokenize_line(CHANDA_STR)))
