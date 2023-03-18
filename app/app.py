#!/usr/bin/env python3
import config
import requests
import pandas
from http import HTTPStatus
import json
import sys
from datetime import datetime, timedelta

WEB_HOOK_URL = config.WEB_HOOK_URL
EOL_API_BASE_URL  = 'https://endoflife.date/api/'

NOTIFICATION_PRODUCTS = config.NOTIFICATION_PRODUCTS
NOTIFICATION_PRODUCTS_VERSION = config.NOTIFICATION_PRODUCTS_VERSION
NOTIFICATION_BEFORE_DEADLINE_DAYS = config.NOTIFICATION_BEFORE_DEADLINE_DAYS

def send_slack(text):
    headers = {
        'Accept': 'application/json',
    }
    response = requests.post(WEB_HOOK_URL, headers=headers, data= json.dumps({
        'text': text
    }))
    print(response.text)

def fetch_end_of_life_date(product, version = None):
    url = EOL_API_BASE_URL + product
    if version != None :
        url = url + '/' + version + '.json'
    else:
        url = url + '.json'
    response = requests.get(url)
    if response.status_code == HTTPStatus.OK:
        return response.text
    else:
        return None

def json_to_markdown_table(data, v):
    data = json.loads(data)
    if v != None:
      df = pandas.DataFrame(data, index=[0]).rename(columns={'support':'Support', 'eol':'EOL', 'latest':'Latest', 'latestReleaseDate':'latestReleaseDate', 'releaseDate': 'releaseDate', 'lts': 'LTS'})
    else:
      df = pandas.DataFrame(data).rename(columns={'support':'Support', 'eol':'EOL', 'latest':'Latest', 'latestReleaseDate':'latestReleaseDate', 'releaseDate': 'releaseDate', 'lts': 'LTS'})
    return df.to_markdown(index=False,tablefmt='fancy_grid')

def notify_product():
    for product in NOTIFICATION_PRODUCTS:
      res = fetch_end_of_life_date(product)
      if res != None:
        slack_text = product + '   \n'
        slack_text += json_to_markdown_table(res, None)
        print(slack_text)

def notify_product_version():
    for product,version in NOTIFICATION_PRODUCTS_VERSION.items():
      res = fetch_end_of_life_date(product, version)
      if res != None:
        slack_text = product + '   \n'
        slack_text += json_to_markdown_table(res, version)
        print(slack_text)

def notify_product_version_deadline_for_slack():
   for product,version in NOTIFICATION_PRODUCTS_VERSION.items():
       res = fetch_end_of_life_date(product, version)
       if res != None:
         product_json = json.loads(res)

         slack_notify = None
         eol = product_json["eol"]
         try:
           deadline_date = datetime.strptime(eol, '%Y-%m-%d')
         except:
            continue
         today = datetime.now()
         for day in NOTIFICATION_BEFORE_DEADLINE_DAYS:
            notify_date = deadline_date - timedelta(days=day)
            print('notify_date', notify_date)
            if today >= notify_date:
               slack_notify = {
                  'product': product,
                  'day': day,
                  'support_term': (deadline_date - datetime.now()).days
                }
               break
         if slack_notify != None and deadline_date >= today:
           slack_text = create_notify_message(product_json, slack_notify)
           send_slack(slack_text)

def create_notify_message(product_json, slack_notify):
    slack_text = '*****' + slack_notify["product"] +  '*****\n'
    slack_text += '【期限切れ】 ' + str(slack_notify["day"]) + ' 日前の通知です。\n'
    slack_text += '残りサポート期間:' + str(slack_notify["support_term"])  + '日です。\n'
    slack_text += slack_notify["product"] + 'は EOLが' + product_json["eol"] + 'です。\n'
    return slack_text

if __name__ == "__main__":
    if len(sys.argv) < 2:
      print("Error: argument is required.")
      sys.exit(1)
    exec_action = sys.argv[1]
    if exec_action == 'notify_version':
       notify_product_version_deadline_for_slack()
       notify_product_version()
    elif exec_action == 'notify_all':
       notify_product()