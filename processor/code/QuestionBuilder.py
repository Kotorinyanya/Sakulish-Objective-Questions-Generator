import codecs
import json
import random

import nltk
from NLPMainHandler import NLPMainHandler
from utils import sum_from_string, underline_word


class QuestionBuilder:

    def __init__(self, file=None, string=None, url='http://localhost:9000'):
        """
        Questiong builder based on NLP main handler.
        The input should be either file or string
        :param file: 
        :param string: 
        """
        # input
        if file is not None:
            self.nlp_handler = NLPMainHandler(file=file, url=url)
        elif string is not None:
            self.nlp_handler = NLPMainHandler(string=string, url=url)
        else:
            raise Exception("QuestionBuilder input required!")

        # build the complete set of NER tags
        with open('resources/ner_tags.json', 'r') as infile:
            self.NER_tags_to_append = json.load(infile)

        # build the complete set of relations
        with codecs.open('resources/properties-with-labels.txt', encoding='utf-8') as infile:
            self._property2label = {l.split("\t")[0]: l.split("\t")[1].strip() for l in infile.readlines()}
        self.relations_to_append = [relation for relation in self._property2label.values()]

        self.subjects = self.build_questions()

    def build_questions(self):
        subjects = []
        # build subject by relation
        subjects_relation = self.build_subject_from_relation(self.nlp_handler.valid_relations)

        # build subject by NER
        subjects_ner = self.build_subject_from_NER_tag_and_tagged_sentence(self.nlp_handler.NER_tags,
                                                                           self.nlp_handler.taggeds_sentences,
                                                                           self.NER_tags_to_append,
                                                                           self.nlp_handler.paraphrased_tagged_coreference[
                                                                               'corefs'])
        # build subject by TextRank
        subjects_textrank = self.build_question_by_main_idea(self.nlp_handler.paraphrased_passage)

        # build subject by Coreference
        subjects_coreference = self.build_question_by_coreference(self.nlp_handler.original_tagged_coreference,
                                                                  self.nlp_handler.original_sentences)

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

    def build_subject_from_NER_tag_and_tagged_sentence(self, NER_tags, tagged_sentences, NER_tags_to_append,
                                                       coreferences):
        subjects_complete_list = []
        # for i in range(1, 5):
        #     chosen_sentence = random.choice(tagged_sentences)
        #     tagged_sentences.remove(chosen_sentence)
        #     sentences_to_use.append(chosen_sentence)

        for current_sentence_i in range(0, tagged_sentences.__len__()):
            current_sentence = tagged_sentences[current_sentence_i]
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
                        print('The complete set of NER tags is not enough, please crawl for NER tags or you can '
                              'ignore this message.')
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
                        if cursor_tagged_word == this_tagged_word:
                            question += '_______' + ' '
                        elif cursor_tagged_word != this_tagged_word:
                            # replace 'he she this that' according to coreference
                            question_word = cursor_tagged_word
                            for id, corefs in coreferences.items():
                                done = False
                                for coref in corefs:
                                    if coref['sentNum'] == current_sentence_i + 1 and coref[
                                        'startIndex'] - 1 <= cursor <= \
                                            coref['endIndex'] - 1 and coref[
                                        'isRepresentativeMention'] == False and question_word == coref['text']:
                                        for origin in corefs:
                                            if origin['isRepresentativeMention'] == True:
                                                replacement = origin['text']
                                                question_word = replacement
                                                done = True
                                                break
                                    if done:
                                        break
                                if done:
                                    break
                            question += question_word + ' '
                        cursor += 1

                    subject = {
                        'question': question,
                        'choices': [choice_A, choice_B, choice_C, choice_D],
                        'answer': 'A'
                    }

                    subjects_complete_list.append(subject)
                    break

        return subjects_complete_list

    def build_question_by_main_idea(self, string):
        subjects_complete_list = []

        summary_sentences = sum_from_string(string)
        choices_complete_list = []
        for summary_sentence in summary_sentences:
            choices_complete_list.append(summary_sentence._text)
        question = 'What is the main idea of this passage?'
        try:
            choice_A = choices_complete_list[0]
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
        subjects, mentioned_word = [], {}
        for id, corefs in coreferences.items():
            # find the mentioned word
            for coref in corefs:
                if coref['isRepresentativeMention'] == True:
                    mentioned_word = {
                        'text': coref['text'],
                        'startIndex': coref['startIndex'],
                        'endIndex': coref['endIndex']
                    }
                    break
            # build questions if there is a word being mentioned
            if mentioned_word != {}:
                for coref in corefs:
                    if coref['isRepresentativeMention'] == True:
                        # skip mentioned words
                        continue
                    subject = self.build_single_quetion_by_coreference(coref, original_sentences,
                                                                       corefered_words_complete_list,
                                                                       mentioned_word)
                    if subject is not None:
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
            return None

        return subject


if __name__ == '__main__':
    file = 'SampleArticle.txt'
    with codecs.open(file, 'r', encoding='utf-8') as infile:
        passage = ' '.join([line for line in infile.readlines()])
    qe = QuestionBuilder(string=passage)
    subjects = qe.subjects
    with open('SampleQuestions.json', 'w') as outfile:
        json.dump(subjects, outfile, indent=4)
    print()
