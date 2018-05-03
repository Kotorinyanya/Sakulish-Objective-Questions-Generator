# -*- coding: UTF-8 -*-
import http.client
import hashlib
from urllib import parse
import random
from googletrans import Translator


class Paraphraser:

    def __init__(self):
        self.baidu_appid = '20180503000153018'
        self.baidu_secretKey = 'IuYO63_t_xMc4h_qgTRZ'

        self.google_translator = Translator(service_urls=[
            'translate.google.cn'
        ])

    def paraphrase(self, input_text_list):
        encoded_list, decoded_list = [], []
        for text in input_text_list:
            encoded_list.append(self.encode(text))
        for text in encoded_list:
            decoded_list.append(self.decode(text))
        return decoded_list

    def decode(self, input_text):
        """
        Decode text by
        :param input_text:
        :return:
        """
        decoded = self.google_translator.translate(input_text, dest='en')
        return decoded.text


    def encode(self, input_text):
        """
        Encode text by Baidu Translate API.
        :param input_text:
        :return:
        """
        encoded = ''
        httpClient = None
        myurl = '/api/trans/vip/translate'
        from_lang, to_lang = 'en', 'zh'
        salt = str(random.randint(32768, 65536))
        sign = self.baidu_appid + input_text + salt + self.baidu_secretKey
        m1 = hashlib.md5()
        m1.update(sign.encode(encoding='utf-8'))
        sign = m1.hexdigest()
        myurl = myurl + '?appid=' + self.baidu_appid + '&q=' + parse.quote(
            input_text) + '&from=' + from_lang + '&to=' + to_lang + '&salt=' + salt + '&sign=' + sign

        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
            response = httpClient.getresponse()
            res = eval(response.read().decode('utf-8'))
            encoded = res['trans_result'][0]['dst']
        except Exception as e:
            print(e)
        finally:
            if httpClient:
                httpClient.close()
            return encoded


if __name__ == '__main__':
    p = Paraphraser()
    print(p.decode('谷歌比百度快。'))
    print()