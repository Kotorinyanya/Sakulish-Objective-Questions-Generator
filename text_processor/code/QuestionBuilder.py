from NLPMainHandler import NLPMainHandler
from utils import sum_form_url, sum_form_file, sum_form_string, underline_word

import nltk
import random
import codecs
import json


class QuestionBuilder:
    def __init__(self, input_file=None):
        # input
        if input_file is None:
            raise Exception("input file required!")

        self.input_file = input_file
        # build the complete set of NER tags
        with open('resources/ner_tags.json', 'r') as infile:
            self.NER_tags_to_append = json.load(infile)

        # build the complete set of relations
        with codecs.open('resources/properties-with-labels.txt', encoding='utf-8') as infile:
            self._property2label = {l.split("\t")[0]: l.split("\t")[1].strip() for l in infile.readlines()}
        self.relations_to_append = [relation for relation in self._property2label.values()]

        self.nlp_handler = NLPMainHandler(input_file)

        self.subjects = self.build_questions()

    def build_questions(self):
        subjects = []
        # build subject by relation
        subjects_relation = self.build_subject_from_relation(self.nlp_handler.valid_relations)

        # build subject by NER
        subjects_ner = self.build_subject_from_NER_tag_and_tagged_sentence(self.nlp_handler.NER_tags,
                                                                            self.nlp_handler.taggeds_sentences,
                                                                            self.NER_tags_to_append)
        # build subject by TextRank
        subjects_textrank = self.build_question_by_main_idea(self.input_file)

        # build subject by Coreference
        subjects_coreference = self.build_question_by_coreference(self.nlp_handler.tagged_coreference, self.nlp_handler.original_sentences)

        subjects = {
            'RelationQuestions': subjects_relation,
            'NerQuestions': subjects_ner,
            'TextRankQuestions': subjects_textrank,
            'CoreferenceQuestions': subjects_coreference
        }

        return subjects

    def build_subject_from_relation(self, relations):
        # build the complete set of all possible relations to choose
        subjects_complete_list = []
        choices_complete_set = set()
        for relation in relations:
            choices_complete_set.add(relation[1])
        for relation in relations:
            question = 'What is the possible relationship between {0} and {1} can you infer from the passage?'.format(
                relation[0], relation[2])

            choices_complete_list = list(choices_complete_set).copy()
            if choices_complete_list.__len__() < 4:
                choices_complete_list = list(set(choices_complete_list + self.relations_to_append))
            try:
                choice_A = relation[1]
                choices_complete_list.remove(choice_A)
                choice_B = random.choice(choices_complete_list)
                choices_complete_list.remove(choice_B)
                choice_C = random.choice(choices_complete_list)
                choices_complete_list.remove(choice_C)
                choice_D = random.choice(choices_complete_list)
                choices_complete_list.remove(choice_D)
            except Exception as e:
                raise Exception('Failed to append relations')
            subject = {
                'question': question,
                'choices': [choice_A, choice_B, choice_C, choice_D],
                'answer': 'A'
            }

            subjects_complete_list.append(subject)

        return subjects_complete_list

    def build_subject_from_NER_tag_and_tagged_sentence(self, NER_tags, tagged_sentences, NER_tags_to_append):
        subjects_complete_list = []
        sentences_to_use = tagged_sentences
        # for i in range(1, 5):
        #     chosen_sentence = random.choice(tagged_sentences)
        #     tagged_sentences.remove(chosen_sentence)
        #     sentences_to_use.append(chosen_sentence)

        for current_sentence in sentences_to_use:
            current_word_i = 0
            while current_word_i < current_sentence.__len__():
                this_ner_tag = current_sentence[current_word_i][1]
                this_tagged_word = current_sentence[current_word_i][0]
                current_word_m = current_word_i + 1
                current_word_i += 1
                if this_ner_tag != 'O':
                    if current_word_m >= current_sentence.__len__():
                        break
                    next_ner_tag = current_sentence[current_word_m][1]
                    while next_ner_tag == this_ner_tag:
                        this_tagged_word += ' ' + current_sentence[current_word_m][0]
                        current_word_m += 1
                        current_word_i += 1
                        if current_word_m >= current_sentence.__len__():
                            break
                        next_ner_tag = current_sentence[current_word_m][1]
                    choices_complete_list = list(NER_tags[this_ner_tag]).copy()
                    # TODO: This method guarantee that there's no repeated choices but reduce the number of subjects
                    # if choices_complete_list.__len__() < 4:
                    #     try:
                    #         choices_complete_list = list(set(NER_tags[this_NER_tag] + NER_tags_to_append[this_NER_tag]))
                    #     except:
                    #         # TODO: extend NER_tags_to_append by crawling passages
                    #         pass
                    # TODO: This mothod do not guarantee that there's no repeated choices
                    if choices_complete_list.__len__() < 4:
                        try:
                            choices_complete_list += NER_tags[this_ner_tag] + NER_tags_to_append[this_ner_tag]
                        except:
                            pass
                    try:
                        choice_A = this_tagged_word
                        choices_complete_list.remove(choice_A)
                        choice_B = random.choice(choices_complete_list)
                        choices_complete_list.remove(choice_B)
                        choice_C = random.choice(choices_complete_list)
                        choices_complete_list.remove(choice_C)
                        choice_D = random.choice(choices_complete_list)
                        choices_complete_list.remove(choice_D)
                    except Exception as e:
                        print(e)
                        print('the complete set of NER tags is not enough!')
                        print(NER_tags[this_ner_tag])
                        print(choices_complete_list)
                        print(choice_A)
                        break
                    question = ''
                    cursor = 0
                    while cursor < current_sentence.__len__():
                        cursor_tagged_word = current_sentence[cursor][0]
                        cursor_tag = current_sentence[cursor][1]
                        next_cursor = cursor + 1
                        if next_cursor >= current_sentence.__len__():
                            break
                        next_tag = current_sentence[next_cursor][1]
                        while next_tag == cursor_tag:
                            cursor_tagged_word += ' ' + current_sentence[next_cursor][0]
                            next_cursor += 1
                            cursor += 1
                            if next_cursor >= current_sentence.__len__():
                                break
                            next_tag = current_sentence[next_cursor][1]
                        if cursor_tagged_word != this_tagged_word:
                            question += cursor_tagged_word + ' '
                        elif cursor_tagged_word == this_tagged_word:
                            question += '_______' + ' '
                        cursor += 1

                    subject = {
                        'question': question,
                        'choices': [choice_A, choice_B, choice_C, choice_D],
                        'answer': 'A'
                    }

                    subjects_complete_list.append(subject)
                    break

        return subjects_complete_list

    def build_question_by_main_idea(self, file):
        summary_sentences = sum_form_file(file)
        subjects_complete_list = []
        question = 'What is the main idea of this passage?'
        try:
            choice_A = summary_sentences[0]
            summary_sentences.remove(choice_A)
            choice_B = random.choice(summary_sentences)
            summary_sentences.remove(choice_B)
            choice_C = random.choice(summary_sentences)
            summary_sentences.remove(choice_C)
            choice_D = random.choice(summary_sentences)
            summary_sentences.remove(choice_D)
            subject = {
                'question': question,
                'choices': [choice_A, choice_B, choice_C, choice_D],
                'answer': 'A'
            }
        except:
            print('The passage should contain more than 4 sentences.')
            return []
        subjects_complete_list.append(subject)
        return subjects_complete_list

    def build_question_by_coreference(self, corenlp_tagged_coreferences, original_sentences):
        """

        :param corenlp_tagged_coreferences: corefs tagged by CoreNLP
        :param original_sentences: sentence list without any parsing
        :return:
        """
        coreferences = corenlp_tagged_coreferences['corefs']

        # build the complete set of corefered words
        corefered_words_complete_list = []
        for id, corefs in coreferences.items():
            for coref in corefs:
                if coref['isRepresentativeMention'] == True:
                    corefered_words_complete_list.append(coref['text'])

        # build questions
        subjects = []
        for id, corefs in coreferences.items():
            for coref in corefs:
                if coref['isRepresentativeMention'] == True:
                    mentioned_word = {
                        'text': coref['text'],
                        'startIndex': coref['startIndex'],
                        'endIndex': coref['endIndex']
                    }
                    # skip words that being refered
                    continue
                subject = self.build_single_quetion_by_coreference(coref, original_sentences,
                                                                   corefered_words_complete_list,
                                                                   mentioned_word)
                subjects.append(subject)

        return subjects

    def build_single_quetion_by_coreference(self, coref, original_sentences, corefered_words_complete_list,
                                            mentioned_word):
        mention_word = {
            'text': coref['text'],
            'startIndex': coref['startIndex'],
            'endIndex': coref['endIndex']
        }
        sentence = original_sentences[coref['sentNum'] - 1]
        tokens = nltk.word_tokenize(sentence)

        underline_sentence = ''
        for index in range(0, tokens.__len__()):
            if mention_word['startIndex'] - 1 <= index <= mention_word['endIndex'] - 2:
                if index < mention_word['endIndex'] - 2:
                    underline_sentence += underline_word(tokens[index]) + '_'
                elif index == mention_word['endIndex'] - 2:
                    underline_sentence += underline_word(tokens[index]) + ' '
            else:
                underline_sentence += tokens[index] + ' '

        question = underline_sentence + '\n'
        question += 'What does the underline word "' + mention_word['text'] + '" mention in this sentence?'

        choices_complete_list = corefered_words_complete_list.copy()
        try:
            choice_A = mentioned_word['text']
            choices_complete_list.remove(choice_A)
            choice_B = random.choice(choices_complete_list)
            choices_complete_list.remove(choice_B)
            choice_C = random.choice(choices_complete_list)
            choices_complete_list.remove(choice_C)
            choice_D = random.choice(choices_complete_list)
            choices_complete_list.remove(choice_D)
            subject = {
                'question': question,
                'choices': [choice_A, choice_B, choice_C, choice_D],
                'answer': 'A'
            }
        except Exception as e:
            print('Word being mentioned by others is less than 4!')
            return {}

        return subject


if __name__ == '__main__':
    qe = QuestionBuilder('/Users/srt_kid/Desktop/Untitled.txt')
    subjects = qe.subjects
    with open('SampleQuestions.json', 'w') as outfile:
        json.dump(subjects, outfile, indent=4)
    print()
