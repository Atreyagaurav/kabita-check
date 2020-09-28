#!/bin/python

import re
import sys
from statistics import mode

from jinja2 import Template

import chanda


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
    return mode(rules)


def check_chanda(line, chanda_rule):
    tokens = chanda.tokenize_line(line)
    return chanda.token_string(tokens) == chanda_rule


def render_line(line, chanda_rule):
    if check_chanda(line, chanda_rule):
        return f'<font color="green">{line}</font>'
    tokens = chanda.tokenize_line(line, word_by_word=True)
    words = chanda.extract_words(line)
    count = 0
    for w, t in zip(words, tokens):
        if chanda.token_string(t) != chanda_rule[count:count + len(t)]:
            print(f"Rule Violation on word:{w}")
            line = line.replace(
                w,
                f'<font color="red" title="It should be ({chanda_rule[count:count+len(t)]}) here instead of ({chanda.token_string(t)})">{w}</font>',
                1)
            # multiple same word will break this
        count += len(t)
    return line


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

    html_lines = map(lambda l: render_line(l, chanda_rule), lines)

    with open("templates/comparision.html", 'r') as reader:
        template = Template(reader.read())

    html = template.render(title="", chanda_rule=chanda_rule, lines=html_lines)
    return html


if __name__ == '__main__':
    lines = read_contents()
    with open("analysis.html", 'w') as writer:
        writer.write(analysis(lines))
