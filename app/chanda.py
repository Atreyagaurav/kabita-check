import re
import json
from enum import Enum

CHANDA_STR = "यमाता राजभान सलगं"
SEPERATOR_CHARS = " -,;१२३४५६७८९०'\""
ALL_CHARS = [
    SEPERATOR_CHARS, "Ii कखगघङ चछजझञ टठडढण तथदधन पफबभम यरलव शषस ह", "अइउऋ",
    "Ss आईएऐओऔऊ", "ाीेैोौूंः:!।", "िुँ", "्"
]
CHANDA_DATA_JSON = 'app/data/standard_names.json'
CHANDA_DATA_TXT = 'app/data/chanda-lists.txt'


class Swor(Enum):
    LONG = 'S'
    SHORT = 'I'
    ANY = 'O'

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if self.value == other.value:
            return True
        if (self is Swor.ANY) or (other is Swor.ANY):
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


def parse_exceptions(line):
    # exception rules for nepali kriyapad
    reg_pattern = r'[%s]्य[ोौ]' % ("|".join(ALL_CHARS[1]))
    line = re.sub(reg_pattern, 'S', line)
    # add others like this if req
    return line


def categorize(char):
    for i, cs in enumerate(ALL_CHARS):
        if char in cs:
            return Chars(i)
    return Chars.UNKNOWN


def tokenize(word, debug=False):
    cat = ((i, categorize(c), c) for i, c in enumerate(word))
    token = []
    for i, c, cw in cat:
        count = len(token)
        if debug:
            print(cw, c, ":", token_string(token))
        if c is Chars.SHORT1 or c is Chars.SHORT2:
            token.append((i, Swor.SHORT))
        elif c is Chars.LONG:
            token.append((i, Swor.LONG))
        elif c is Chars.LONG_ADD:
            if count > 0:
                token[count - 1] = (i, Swor.LONG)
            else:
                pass  # error
        elif c is Chars.SHORT_ADD:
            token[count - 1] = (i, token[count-1][1])
        elif c is Chars.SHORT_SUB:
            if count > 1:
                token.pop()
                token[count - 2] = (i, Swor.LONG)
            else:
                token.pop()
    return token


def print_word_tokens(word):
    prev = 0
    for i, val in tokenize(word):
        print(i, val, word[prev:i+1])
        prev = i+1


def extract_words(line):
    return re.split('|'.join(SEPERATOR_CHARS), line)


def tokenize_line(line, word_by_word=False):
    line = line.strip()
    if len(line) == 0 or line[0] == '#':
        return []

    # line = parse_exceptions(line)
    if word_by_word:
        words = extract_words(line)
        token = list(map(tokenize, words))
        return token

    return tokenize(line)


def token_string(token):
    return ''.join([str(t[1]) for t in token])


def get_si_string(line):
    return ''.join(filter(lambda x: x in 'SIO', line.upper()))


def get_chanda_name(rule):
    rule = get_si_string(rule)
    all_chanda = get_all_chanda()
    match = filter(lambda x: get_si_string(x[1]) == rule, all_chanda.items())
    name = map(lambda x: x[0], match)
    return '; '.join(name)


def get_all_chanda():
    all_chanda = dict()
    with open(CHANDA_DATA_TXT, 'r') as r:
        for line in r:
            if len(line) == 0 or line[0] == '#':
                continue
            data = line.split(';')
            if len(data)<3:
                continue
            name = data[1].strip()
            rule = data[0].strip()
            all_chanda[name] = rule
    with open(CHANDA_DATA_JSON, 'r') as r:
        names = json.load(r)
    for rule, name in names.items():
        if name not in all_chanda:
            all_chanda[name] = rule
    return all_chanda


if __name__ == '__main__':
    print("String: ", CHANDA_STR)
    print("Swors: ", token_string(tokenize_line(CHANDA_STR)))
