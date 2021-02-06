import re
import json
from enum import Enum

CHANDA_STR = "यमाताराजभानसलगं"
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


class Chanda:
    def __init__(self, rule, name=None, gans=None):
        self.rule = rule
        self.si = get_si_string(rule)
        self.length = len(self.si)
        self.rule_tokens = tokenize(rule)
        self.gans = token_gan(self.si, gans)
        if not name:
            name = get_chanda_name(rule)
        self.name = name.strip()

    def check(self, tokens):
        token = [t[1] for t in tokens]
        return token == self.rule_tokens

    def jsonize(self):
        return dict(
            name=self.name,
            rule=self.rule,
            length=self.length,
            gans=self.gans,
            index=self.name[0]
        )


class Line:
    def __init__(self, value):
        self.value = value
        self.tokens = tokenize_line(value)
        self.si = token_string(self.tokens)
        self.length = len(self.si)

    def match(self, chanda):
        return chanda.check(self.tokens)


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


def get_all_gan():
    gans = tokenize(CHANDA_STR)
    prev = 0
    all_gans = dict()
    for i in range(len(gans)-2):
        gan, rule = CHANDA_STR[prev], token_string(gans[i:i+3])
        all_gans[rule] = gan
        prev = gans[i][0] + 1
    return all_gans


def token_gan(token, gans=None):
    if not gans:
        gans = get_all_gan()
    if isinstance(token, str):
        rule = get_si_string(token)
    else:
        rule = token_string(token)
    gan_str = ''
    while len(rule) > 0:
        if len(rule) >= 3:
            gan_str += gans[rule[:3]] + ' '
            rule = rule[3:]
        else:
            gan_str += 'गु.' if rule[0] == 'S' else 'ल.'
            rule = rule[1:]
    return gan_str.strip()


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
    gans = get_all_gan()
    with open(CHANDA_DATA_TXT, 'r') as r:
        for line in r:
            if len(line) == 0 or line[0] == '#':
                continue
            data = line.split(';')
            if len(data) < 2:
                continue
            name = data[1].strip()
            rule = data[0].strip()
            all_chanda[name] = Chanda(rule, name=name, gans=gans)
    with open(CHANDA_DATA_JSON, 'r') as r:
        names = json.load(r)
    for rule, name in names.items():
        if name not in all_chanda:
            all_chanda[name] = Chanda(rule, name=name, gans=gans)
    return sorted(all_chanda.values(), key=lambda c: c.length)


if __name__ == '__main__':
    print("String: ", CHANDA_STR)
    print("Swors: ", token_string(tokenize_line(CHANDA_STR)))
