from pycorenlp import StanfordCoreNLP
from Summer import *

from itertools import chain
from collections import defaultdict

import json

corenlp = StanfordCoreNLP('http://localhost:9000')
corenlp_properties = {
    'annotators': 'ner',
    'outputFormat': 'json'
}


def build_ner_tagged_set(taggeds):
    ner_set = {}
    # create dictionary
    for tagged in taggeds:
        for single_tag in tagged:
            key = single_tag[1]
            ner_set.setdefault(key, [])

    # insert value
    prev_tag = ''
    for tagged in taggeds:
        for single_tag in tagged:
            tag = single_tag[1]
            value = single_tag[0]
            if tag == prev_tag:
                ner_set[tag].pop()
                value = prev_value + ' ' + value
            ner_set[tag].append(value)
            prev_tag, prev_value = tag, value
    for key, value in ner_set.items():
        new_value = list(set(value))
        ner_set[key] = new_value
    return ner_set


def get_ner_tags(url):
    input_sentences = sum_form_url(url)
    plain_sentences = []
    for sentence in input_sentences:
        plain_sentences.append(sentence._text.replace('\\', ''))

    taggeds_sentences = []
    for sentence in plain_sentences:
        corenlp_output = \
            corenlp.annotate(sentence, properties=corenlp_properties).get("sentences", [])[0]
        taggeds_sentences.append([(t['originalText'], t['ner']) for t in corenlp_output['tokens']])

    ner_set = build_ner_tagged_set(taggeds_sentences)
    return ner_set


ner_dict = defaultdict(list)


def delete_file_content(pfile):
    pfile.seek(0)
    pfile.truncate()

# TODO: SPEED UUUUUUP
for i in range(20000, 30000):
    url = 'http://www.gutenberg.org/files/' + str(i) + '/' + str(i) + '-h/' + str(i) + '-h.htm'
    try:
        dict = get_ner_tags(url)
    except:
        print('{0} is not available'.format(url))
        continue
    for k, v in chain(dict.items(), ner_dict.items()):
        ner_dict[k] = list(set(ner_dict[k] + v))
    with open('resources/ner_tags.json', 'w') as outfile:
        json.dump(ner_dict, outfile, indent=4)
    print('{0} is done'.format(url))

# result = {key: list(set(dict1.get(key, 0) + dict2.get(key, 0))) for key in set(dict1) | set(dict2)}
print('\n-----------------------------------------------------\n')
print('ALL DONE')
