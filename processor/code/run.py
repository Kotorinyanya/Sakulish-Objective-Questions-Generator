"""
This program should be both Python 2 & Python 3 compatible.
Only run.py, db.py & helper.py are included.
"""
import argparse
import uuid
from db import DB

from QuestionBuilder import QuestionBuilder
import random
import re
import html

args = None

def parse_arguments():
    """
    Parse arguments from command line and return the results.
    :return: parsed args
    """
    parser = argparse.ArgumentParser(description="SOQ Text Processor.")
    parser.add_argument("--debug", action="store_true",
                        help="Use this option to enable debug mode.")
    parser.add_argument("--host", action='store', default="redis",
                        help="Specify Redis host address.")
    parser.add_argument("--port", action='store', default=6379, type=int,
                        help="Specify Redis host port.")
    parser.add_argument("--core", action='store', default='http://core:9000', type=str,
                        help="Specify core URL.")
    return parser.parse_args()


def process(text):
    """
    This function should receive a text, and generate questions from it.
    The return format should be as described in the online document.
    :param text:
    :return:
    """
    print("Start processing...")
    questions = dict()
    print("Building questions...")
    q = QuestionBuilder(string=text, url=args.core)
    raw_list = q.subjects
    print("Formatting...")
    for t, tc in raw_list.items():
        questions[t] = list()
        for s in tc:
            if "answer" not in s:
                continue
            answer_id = int(s["answer"], 36) - int("A", 36)
            answer = s["choices"][answer_id]
            random.shuffle(s["choices"])
            stem = html.escape(s["question"])
            stem = stem.replace("_____", " ")
            stem = re.sub("__(.*)__", r"<u>\1</u>", stem)
            questions[t].append({
                "stem": stem,
                "choices": s["choices"],
                "answer": s["choices"].index(answer)
            })
    return questions


def main():
    print("Start listening...")
    while True:
        # Get one task.
        task = db.get_text()
        print("Get something...")
        if not task:
            continue
        print("Get a text, len:", len(task["text"]))
        try:
            result = {
                "uuid": str(uuid.uuid1()),
                "text": html.escape(task["text"]),
                "questions": process(task["text"]),
                "attachments": task["attachments"] if "attachments" in task else dict()
            }
        except Exception as e:
            print("An error occurred while processing the text:", e)
            continue
        else:
            db.push_result(result)


if __name__ == "__main__":
    args = parse_arguments()
    db = DB(args.host, args.port)
    main()
