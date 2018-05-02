from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


def sum_form_file(text_file, language="english", sentences_cout=100):
    parser = PlaintextParser.from_file(text_file, Tokenizer(language))
    stemmer = Stemmer(language)
    summarizer = Summarizer(stemmer)
    summarizer.stem_words = get_stop_words(language)
    sentences = summarizer(parser.document, sentences_cout)
    return sentences


def sum_form_url(url, language="english", sentences_cout=100):
    parser = HtmlParser.from_url(url, Tokenizer(language))
    stemmer = Stemmer(language)
    summarizer = Summarizer(stemmer)
    summarizer.stem_words = get_stop_words(language)
    sentences = summarizer(parser.document, sentences_cout)
    return sentences


def sum_form_string(string, language="english", sentences_cout=100):
    parser = PlaintextParser.from_string(string, Tokenizer(language))
    stemmer = Stemmer(language)
    summarizer = Summarizer(stemmer)
    summarizer.stem_words = get_stop_words(language)
    sentences = summarizer(parser.document, sentences_cout)
    return sentences


if __name__ == "__main__":
    text_file = "document.txt"
    keyphrases = sum_form_string(string='t first I was upset when they told me we were moving to some little town out in the Ozarks. I remember staring at my dinner plate while I listened to my sister throw a temper tantrum unbefitting of a 14 year old honors student. She cried, she pleaded, and then she cursed at my parents. She threw a bowl at my dad and told him it was all his fault. Mom told Whitney to calm down but she stormed off, slamming every door in the house on the way to her room.')
    print()