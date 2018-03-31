# -*-coding:utf-8 -*-

import requests
import json


class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        params = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【北华1408】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code),
        }

        response = requests.post(self.single_send_url, data=params)
        re_dict = json.loads(response.text)

        return re_dict


if __name__ == "__main__":
    yun_pian = YunPian('b138e4bca3779dc9a2ceb208b8e4614c')
    yun_pian.send_sms("2018", "13244205282")