from NLPMainHandler import NLPMainHandler
from Summer import sum_form_url, sum_form_file, sum_form_string

import random
import codecs
import json

class QuestionBuilder:
    def __init__(self, url=None, file=None, string=None):
        # input
        if url is not None:
            self.input_sentences = sum_form_url(url)
        elif file is not None:
            self.input_sentences = sum_form_file(file)
        elif string is not None:
            self.input_sentences = sum_form_string(string)
        else:
            raise Exception("input url/file/string required!")

        # build the complete set of NER tags
        with open('resources/ner_tags.json', 'r') as infile:
            self.NER_tags_to_append = json.load(infile)

        # build the complete set of relations
        with codecs.open('resources/properties-with-labels.txt', encoding='utf-8') as infile:
            self._property2label = {l.split("\t")[0]: l.split("\t")[1].strip() for l in infile.readlines()}
        self.relations_to_append = [relation for relation in self._property2label.values()]

        # NLP
        self.nlp_handler = NLPMainHandler(self.input_sentences)

        self.subjects = []
        # build subject by method 1
        self.subjects += (self.build_subject_from_relation(self.nlp_handler.relatoins))

        # build subject by method 2
        self.subjects += (self.build_subject_from_NER_tag_and_tagged_sentence(self.nlp_handler.NER_tags,
                                                                              self.nlp_handler.taggeds_sentences,
                                                                              self.NER_tags_to_append))
        # build subject by method 3
        self.subjects += (self.build_question_by_main_idea(self.nlp_handler.plain_sentences))

    def build_subject_from_relation(self, relations):
        # build the complete set of all possible relations to choose
        subjects_complete_list = []
        choices_complete_set = set()
        for relation in relations:
            choices_complete_set.add(relation[1])
        for relation in relations:
            question = 'What is the possible relationship between {0} and {1} can you infer from the passage?'.format(
                relation[0], relation[2])

            relations_to_choose = list(choices_complete_set)
            if relations_to_choose.__len__() < 4:
                try:
                    relations_to_choose = list(set(relations_to_choose + self.relations_to_append))
                except:
                    print('relations extracted form text is not enough!')
                    continue
            choice_A = relation[1]
            relations_to_choose.remove(choice_A)
            choice_B = random.choice(relations_to_choose)
            relations_to_choose.remove(choice_B)
            choice_C = random.choice(relations_to_choose)
            relations_to_choose.remove(choice_C)
            choice_D = random.choice(relations_to_choose)
            relations_to_choose.remove(choice_D)

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
                    choices_complete_list = NER_tags[this_ner_tag].copy()
                    # TODO: This method guarantee that there's no repeated choices but reduce the number of subjects
                    # if choices_complete_list.__len__() < 4:
                    #     try:
                    #         choices_complete_list = list(set(NER_tags[this_NER_tag] + NER_tags_to_append[this_NER_tag]))
                    #     except:
                    #         # TODO: extend NER_tags_to_append by crawling passages
                    #         pass
                    # TODO: This mothod do not guarantee that there's no repeated choices
                    while choices_complete_list.__len__() < 4:
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

    def build_question_by_main_idea(self, summary_sentences):
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
        except:
            raise Exception('The passage should contain more than 4 sentences.')
        subject = {
            'question': question,
            'choices': [choice_A, choice_B, choice_C, choice_D],
            'answer': 'A'
        }
        subjects_complete_list.append(subject)
        return subjects_complete_list


if __name__ == '__main__':
    qe = QuestionBuilder(url='http://www.bbc.com/news/uk-43941624')
    subjects = qe.subjects
    print()
