from NLPMainHandler import NLPMainHandler
from Summer import *

import random


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

        self.NER_tags_to_append = {
            'ORGANIZATION': ['Asda', 'CMA', 'Tesco', 'Walmart', 'Sainsbury', 'Lidl', 'BBC News'],
            'DATE': ['2016', 'the autumn of 2019', 'current', 'the weekend', 'currently', '1999'],
            'COUNTRY': ['UK', 'US', 'China', 'Japan'],
            'TITLE': ['chairman', 'mobile', 'chief executive', 'leader', 'business secretary', 'boss', 'general',
                      'analyst', 'director', 'retailer'],
            'PERSON': ['Vince Cable', 'Mike Cherry', 'Mike Coupe', 'Coupe', 'Argos', 'Dresser', 'Nick Bubb',
                       'Rebecca Long-Bailey', 'Steve Dresser'], 'ORDINAL': ['second and third'],
            'NUMBER': ['1', '3', '4', '2', '5', 'two', 'one'], 'PERCENT': ['10 %', '42 %', '30 %'],
            'IDEOLOGY': ['Liberal Democrat', "I don't know", "I don't know either"],
            'LOCATION': ['Chengdu', 'Tokyo', 'Beijing', 'Shanghai']
        }

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
                raise Exception('relations extracted form text is not enough!')
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
            for i in range(2, current_sentence.__len__()):
                this_NER_tag = current_sentence[i][1]
                if this_NER_tag is not 'O':
                    this_tagged_word = current_sentence[i][0]
                    m = i + 1
                    while current_sentence[m][1] is this_NER_tag:
                        this_tagged_word += ' ' + current_sentence[m][0]
                        m += 1
                    choices_complete_list = NER_tags[this_NER_tag].copy()
                    if choices_complete_list.__len__() < 4:
                        try:
                            for x in NER_tags_to_append[this_NER_tag]:
                                choices_complete_list.append(x)
                        except:
                            # TODO: extend NER_tags_to_append to avoid key error
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
                    except:
                        break
                        # raise Exception('NER tags is not enough!')
                    question = ''
                    for cursor in range(2, current_sentence.__len__()):
                        cursor_tagged_word = current_sentence[cursor][0]
                        cursor_tag = current_sentence[cursor][1]
                        next_cursor = cursor + 1
                        if next_cursor >= current_sentence.__len__():
                            continue
                        while current_sentence[next_cursor][1] is cursor_tag and cursor_tag is not 'O':
                            cursor_tagged_word += ' ' + current_sentence[next_cursor][0]
                            next_cursor += 1
                        if cursor_tagged_word is not this_tagged_word:
                            question += cursor_tagged_word + ' '
                        elif cursor_tagged_word is this_tagged_word:
                            question += '_______' + ' '

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
