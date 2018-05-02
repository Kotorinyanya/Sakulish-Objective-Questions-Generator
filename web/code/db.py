import json
import redis
import uuid
from time import time


class DB(object):
    def __init__(self, host, port):
        self.db = redis.Redis(host=host, port=port)

    def feed_text(self, text, uid=None):
        """
        Feed a text into to-do queue manually.
        :param text: text to process
        :param uid: UUID of text
        :return: length of queue
        """
        new_item = dict()
        # If UUID not specified, generate one.
        if not uid:
            uid = uuid.uuid1()
        new_item["uuid"] = str(uid)
        new_item["text"] = text
        length = self.db.lpush("soq_texts", json.dumps(new_item))
        return length

    def get_results(self, rank, count=1):
        """
        Fetch [count] results starting from [rank].
        :param rank: start rank
        :param count: items count
        :return: results
        """
        raw_results = self.db.zrange("soq_results", rank, rank + count - 1, withscores=True)
        try:
            results = [{"timestamp": x[1], "result": json.loads(x[0].decode().replace("\n", "\\n").replace("\r", "\\r"))} for x in raw_results]
        except Exception as e:
            print("An error occurred while fetching results {} ~ {}".format(rank, rank + count), e)
            return list()
        return results

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
