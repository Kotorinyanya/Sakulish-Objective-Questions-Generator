"""
Relation Extraction by emnlp2017-relation-extraction
"""
import sys

sys.path.insert(0, "relation_extraction/")
from core.parser import RelParser
from core import keras_models
from core import entity_extraction
from pycorenlp import StanfordCoreNLP
import nltk
import codecs

from utils import *

from Paraphraser import Paraphraser


class NLPMainHandler:

    def __init__(self, file):
        """
        Input sentences were supposed to be a list of NLTK 'Sentence' objects
        :param file: Input file, the passage
        """
        # run Stanford CoreNLP server at localhost:9000
        # java -mx8g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer
        self.corenlp = StanfordCoreNLP('http://localhost:9000')
        self.corenlp_properties = {
            'annotators': 'tokenize, pos, ner',
            'outputFormat': 'json'
        }

        # get input sentences and the whole passage
        with codecs.open(file, 'r', encoding='utf-8') as infile:
            self.original_passage = ' '.join([line.replace('\n', '') for line in infile.readlines()])
        self.original_sentences = nltk.sent_tokenize(self.original_passage)

        # set keras model params
        keras_models.model_params['wordembeddings'] = "resources/embeddings/glove/glove.6B.50d.txt"
        self.relparser = RelParser("model_ContextWeighted", models_foldes="trainedmodels/")

        # paraphrase the passage
        self.paraphraser = Paraphraser()
        self.paraphrased_sentences = self.paraphraser.paraphrase_sentence_list(self.original_sentences)

        self.paraphrased_passage = ''

        # tag coreference by CoreNLP
        self.tagged_coreference = self.corenlp.annotate(self.original_passage, properties={
            'timeout': '60000',
            'annotators': 'coref',
            'outputFormat': 'json'
        })

        # tag input sentences by CoreNLP
        self.taggeds_sentences = []
        for sentence in self.paraphrased_sentences:
            corenlp_output = \
                self.corenlp.annotate(sentence, properties=self.corenlp_properties).get("sentences", [])[0]
            # TODO: optimazation, DO NOT require for unnecessary data.
            self.taggeds_sentences.append([(t['originalText'], t['ner'], t['pos']) for t in corenlp_output['tokens']])

        # extract entity fragments
        self.entity_fragments = []
        for tagged_plain_sentence in self.taggeds_sentences:
            self.entity_fragments.append(entity_extraction.extract_entities(tagged_plain_sentence))

        # extract edges
        self.edges = []
        for entity_fragment in self.entity_fragments:
            self.edges.append(entity_extraction.generate_edges(entity_fragment))

        # construct non_parsed_graphs for relation extraction
        self.non_parsed_graphs = []
        for tagged, edges in zip(self.taggeds_sentences, self.edges):
            self.non_parsed_graphs.append({'tokens': [t for t, _, _ in tagged],
                                           'edgeSet': edges})

        # do relation extraction
        self.parsed_graphs = []
        for non_parsed_graph in self.non_parsed_graphs:
            self.parsed_graphs.append(self.relparser.classify_graph_relations(non_parsed_graph))

        # get valid relations
        self.valid_relations = self.get_valid_relations_from_parsed_graphs(self.parsed_graphs)

        # build NER complete set
        self.NER_tags = self.build_ner_tagged_set(self.taggeds_sentences)

    def get_valid_relations_from_parsed_graphs(self, parsed_graphs):
        relations = []
        for parsed_graph in parsed_graphs:
            try:
                tokens = parsed_graph['tokens']
            except:
                continue
            edge_set = parsed_graph['edgeSet']
            for relation in edge_set:
                if relation['kbID'] != 'P0' and relation['kbID'] != 'P31' and relation['left'] != [0] and relation['right'] != [0]:
                    # P0: 'O', P31: 'instance of'
                    left, middle, right = '', '', ''
                    for token_index in relation['left']:
                        left += tokens[token_index] + ' '
                    middle = relation['lexicalInput']
                    for token_index in relation['right']:
                        right += ' ' + tokens[token_index]
                    relations.append((left, middle, right))
        return relations

    def build_ner_tagged_set(self, taggeds):
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


if __name__ == '__main__':
    # text = 'Star Wars VII is an American space opera epic film directed by  J. J. Abrams.'
    # input_sentences = sum_form_string(text)
    Re = NLPMainHandler('/Users/srt_kid/Desktop/Untitled.txt')
    relations = Re.valid_relatoins
    ner_set = Re.NER_tags
    tagged_sentences = Re.taggeds_sentences
    print()
