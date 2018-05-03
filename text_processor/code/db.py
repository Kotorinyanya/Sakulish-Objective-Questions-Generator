import json
import redis
from time import time


class DB(object):
    def __init__(self, host, port):
        self.db = redis.Redis(host=host, port=port)

    def get_text(self):
        """
        Try to get one text from the queue.
        Will block until there is one available.
        :return: resolved task
        """
        try:
            raw_text = self.db.blpop("soq_texts")
            text = json.loads(raw_text[1])
        except Exception as e:
            print("An error occurred while reading from text queue:", e)
            return None
        return text

    def push_result(self, result):
        """
        Try to push a result to the set.
        :param result: the generated
        :return:
        """
        try:
            new_item = json.dumps(result)
            self.db.zadd("soq_results", new_item, time())
        except Exception as e:
            print("An error occurred while saving the result:", e)

    def get_text_queue_count(self):
        """
        Return the length of text queue.
        :return: length of queue
        """
        return self.db.llen("soq_texts")

    def get_result_set_count(self):
        """
        Return the size of result set.
        :return:
        """
        return self.db.zcount("soq_results", 0, time())
