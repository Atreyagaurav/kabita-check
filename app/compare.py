#!/bin/python

import re
import sys
from statistics import mode, StatisticsError

import app.chanda as chanda
# import app.dictionary as dictionary


def extract_chanda_rule(lines):
    comments = filter(lambda l: l.iscomment() and l.length > 0, lines)
    for comment in comments:
        line = comment.value[1:].strip()
        if re.match('[ISO]+', line):
            return ''.join([c for c in line if c in 'IS'])
    # if not specified or find, guess the rule
    kabita_lines = filter(lambda l: not l.iscomment() and l.si != '',
                          lines)
    rules = map(lambda l: l.si, kabita_lines)
    try:
        rule = mode(rules)
    except StatisticsError:
        # mode couldn't be found: not error on my laptop but shows
        # error on heroku
        rule = ''
    return rule


def read_contents():
    if len(sys.argv) == 1:
        filename = input("Enter path to file for comparision: ")
    else:
        filename = sys.argv[1]

    with open(filename, 'r') as reader:
        lines = reader.readlines()
    return lines


def analysis(text, rule='auto-detect'):
    lines = list(map(chanda.Line, text.split('\n')))
    if rule == 'auto-detect' or not rule:
        rule = extract_chanda_rule(lines)
    chanda_obj = chanda.Chanda(rule)
    # all_words = dictionary.just_words()

    for line in lines:
        line.match(chanda_obj)
        # Check spelling not applied as it can't check combined words
        # like eko eka eki ones. 
        # if line.check == chanda.LineType.UNCHECKED:
        #     continue
        # line.check_spelling(all_words)
    correct = sum(map(lambda l: l.check == chanda.LineType.CORRECT, lines))
    wrong = sum(map(lambda l: l.check == chanda.LineType.WRONG, lines))
    ignored = sum(map(lambda l: l.check == chanda.LineType.UNCHECKED, lines))
    if wrong == 0:
        err_messages = 'सबै लाईन हरु सहि छन्।'
    else:
        err_messages = '<br />'.join((f'line-{i+1}: {";".join(l.comments)}'
                                      for i, l in enumerate(lines)
                                      if l.check == chanda.LineType.WRONG))

    html_lines = '<br />'.join((f'<font color="grey">{i+1}:</font>{l.html}'
                                for i, l in enumerate(lines)))
    return dict(total=correct + wrong + ignored,
                correct=correct,
                wrong=wrong,
                ignored=ignored,
                chanda_name=chanda_obj.name,
                chanda_rule=rule,
                html_lines=html_lines,
                err_messages=err_messages)


if __name__ == '__main__':
    lines = read_contents()
    with open("analysis.html", 'w') as writer:
        writer.write(analysis(lines))
