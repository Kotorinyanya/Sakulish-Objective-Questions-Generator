"""
This program should be both Python 2 & Python 3 compatible.
Only run.py, db.py & helper.py are included.
"""
import argparse
import uuid
from db import DB

from QuestionBuilder import QuestionBuilder
import random


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
    return parser.parse_args()


def process(text):
    """
    This function should receive a text, and generate questions from it.
    The return format should be as described in the online document.
    :param text:
    :return:
    """
    questions = list()
    q = QuestionBuilder(string=text)
    ss = q.subjects
    for s in ss:
        answer_id = int(s["answer"], 36) - int("A", 36)
        answer = s["choices"][answer_id]
        random.shuffle(s["choices"])
        questions.append({
            "stem": s["question"],
            "choices": s["choices"],
            "answer": s["choices"].index(answer)
        })
    return questions


def main():
    while True:
        # Get one task.
        task = db.get_text()
        if not task:
            continue
        try:
            result = {
                "uuid": str(uuid.uuid1()),
                "text": task["text"],
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
