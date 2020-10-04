#!/bin/python

import re
import sys
from statistics import mode, StatisticsError

import app.chanda as chanda


def iscomment(line):
    if len(line.strip()) != 0 and line.strip()[0] == '#':
        return True
    return False


def extract_chanda_rule(lines):
    comments = filter(iscomment, lines)
    for comment in comments:
        line = comment[1:].strip()
        if re.match('[IS]+', line):
            return ''.join([c for c in line if c in 'IS'])
    #if not specified or find, guess the rule
    kabita_lines = filter(lambda l: not iscomment(l) and l.strip() != '',
                          lines)
    rules = map(lambda l: chanda.token_string(chanda.tokenize_line(l)),
                kabita_lines)
    try:
        rule = mode(rules)
    except StatisticsError:
        #mode couldn't be found: not error on my laptop but shows error on heroku
        rule = ''
    if len(rule) > 0:
        rule = rule[:-1] + 'S'
    return rule


def check_chanda(line, chanda_rule):
    tokens = chanda.tokenize_line(line)
    if len(tokens) > 0:
        tokens[-1] = chanda.Swor('S')
    return chanda.token_string(tokens) == chanda_rule


def render_line(line, chanda_rule):
    if line.strip() == '':
        return '', -2, 'खालि।'
    if iscomment(line):
        return f'<font color="brown">{line}</font>', -1, 'जाँच नगर्ने।'
    if check_chanda(line, chanda_rule):
        return f'<font color="green">{line}</font>', 1, 'सहि छ।'
    tokens = chanda.tokenize_line(line, word_by_word=True)
    words = chanda.extract_words(line)
    line_len = len(chanda.tokenize_line(line))
    rule_len = len(chanda_rule)
    if rule_len != line_len:
        return f'<font color="red" title="length error">{line}</font>', 0, f'यो लाईनमा {rule_len} बर्ण हुन पर्नेमा {line_len} छ।'
    count = 0
    instruction = ''
    for w, t in zip(words, tokens):
        rule_is = chanda_rule[count:count + len(t)]
        here_is = chanda.token_string(t)
        if here_is != rule_is:
            print(f"Rule Violation on word:{w}")
            line = line.replace(
                w,
                f'<font color="red" title="It should be ({rule_is}) here instead of ({here_is})">{w}</font>'
            )
            instruction += f'{w} को ठाउँमा {rule_is} हुन पर्नेमा {here_is} छ। '
            # multiple same word will break this
        count += len(t)
    return line, 0, instruction


def read_contents():
    if len(sys.argv) == 1:
        filename = input("Enter path to file for comparision: ")
    else:
        filename = sys.argv[1]

    with open(filename, 'r') as reader:
        lines = reader.readlines()
    return lines


def analysis(lines):
    chanda_rule = extract_chanda_rule(lines)
    chanda_name = chanda.get_chanda_name(chanda_rule)

    render_result = [render_line(l, chanda_rule) for l in lines]
    correct = sum((l[1] == 1 for l in render_result))
    wrong = sum((l[1] == 0 for l in render_result))
    if wrong == 0:
        err_messages = 'सबै लाईन हरु सहि छन्।'
    else:
        err_messages = '<br />'.join((f'line-{i+1}: {l[2]}'
                                  for i, l in enumerate(render_result)
                                  if l[1] == 0))
    ignored = sum((l[1] == -1 for l in render_result))

    html_lines = '<br />'.join((f'<font color="grey">{i+1}:</font>{l[0]}' for i,l in enumerate(render_result)))
    return dict(total=correct + wrong + ignored,
                correct=correct,
                wrong=wrong,
                ignored=ignored,
                chanda_name=chanda_name,
                chanda_rule=chanda_rule,
                html_lines=html_lines,
                err_messages=err_messages)


if __name__ == '__main__':
    lines = read_contents()
    with open("analysis.html", 'w') as writer:
        writer.write(analysis(lines))
