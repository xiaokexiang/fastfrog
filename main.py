import json
import os

import requests

from fastfrog import config, utils

if __name__ == '__main__':
    if os.environ.get('CORP_ID') is None \
            or os.environ.get('CORP_SECRET') is None \
            or os.environ.get('TO_USER') is None \
            or os.environ.get('AGENT_ID') is None \
            or os.environ.get('TOKEN') is None:
        print('env init error')
        exit(101)
    corp_id = os.environ.get('CORP_ID')
    corp_secret = os.environ.get('CORP_SECRET')
    to_user = os.environ.get('TO_USER')
    agent_id = os.environ.get('AGENT_ID')
    token = os.environ.get('TOKEN')
    response = requests.put(config.CHECKIN, headers={
        'AuthorizationMweb': token
    }, verify=False)
    msg = '签到失败！'
    if response.status_code == 200:
        if json.loads(response.text).get('code') == 100:
            msg = str(json.loads(response.text).get('data').get('message'))
        elif json.loads(response.text).get('code') == 10:
            msg = str(json.loads(response.text).get('message'))
    utils.push({
        "chatid": "CHATID",
        "msgtype": "news",
        "touser": to_user,
        "agentid": agent_id,
        "news": {
            "chatid": "CHATID",
            "msgtype": "textcard",
            "touser": to_user,
            "agentid": agent_id,
            "textcard": {
                "title": '速蛙云签到',
                "description": msg,
                "url": "https://faster.goodfrog1.net/",
                "btntxt": "更多"
            },
            "safe": 0
        },
        "safe": 0
    }, corp_id, corp_secret)
