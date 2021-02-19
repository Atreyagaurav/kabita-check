import csv

dict_file = "./app/data/words.csv"


def wordlist(rule=None, start=None):
    with open(dict_file, 'r', newline='') as r:
        reader = csv.reader(r, quotechar='"')
        headers = next(reader)
        matches = reader
        if rule:
            print(f"Rule={rule}")
            if rule[0] == '-':
                def filter_fun(row): return row[-1].endswith(rule[1:])
            elif rule[-1] == '-':
                def filter_fun(row): return row[-1].startswith(rule[:-1])
            else:
                def filter_fun(row): return row[-1] == rule
            matches = filter(filter_fun, matches)

        if start:
            print(f"Start={start}")
            if start[0] == '-':
                def filter_fun(row): return row[0].endswith(start[1:])
            elif start[-1] == '-':
                def filter_fun(row): return row[0].startswith(start[:-1])
            else:
                def filter_fun(row): return row[0] == start
            matches = filter(filter_fun, matches)

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
