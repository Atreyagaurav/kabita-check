import csv

dict_file = "./app/data/words.csv"


def wordlist(rule=None, start=None):
    with open(dict_file, 'r', newline='') as r:
        reader = csv.reader(r, quotechar='"')
        headers = next(reader)
        matches = reader
        if rule:
            matches = filter(lambda row: row[-1] == rule, matches)
        if start:
            if start[0] == '-':
                matches = filter(lambda row: row[0].endswith(start[1:]), matches)
            else:
                matches = filter(lambda row: row[0].startswith(start), matches)

        def get_dict(row):
            value = {k: v for k, v in zip(headers, row)}
            if 'meanings' in value:
                value['meanings'] = value['meanings'].split('\n')
            return value

        return [get_dict(row) for row in matches]


def just_words():
    with open(dict_file, 'r', newline='') as r:
        reader = csv.reader(r, quotechar='"')
        next(reader)
        return set(map(lambda l: l[0], reader))
