#!/usr/bin/env python3
import config
import requests
import pandas
from http import HTTPStatus
import json

WEB_HOOK_URL = config.WEB_HOOK_URL
EOL_API_BASE_URL  = 'https://endoflife.date/api/'

NOTIFICATION_PRODUCTS = config.NOTIFICATION_PRODUCTS
NOTIFICATION_PRODUCTS_VERSION = config.NOTIFICATION_PRODUCTS_VERSION

def sendSlack(text):
    headers = {
        'Accept': 'application/json',
    }
    response = requests.post(WEB_HOOK_URL, headers=headers, data= json.dumps({
        'text': text
    }))
    print(response.text)

def endoflifeDate(product, version = None):
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


def jsonToMarkdownTable(data, v):
    data = json.loads(data)
    if v != None:
      df = pandas.DataFrame(data, index=[0]).rename(columns={'support':'Support', 'eol':'EOL', 'latest':'Latest', 'latestReleaseDate':'latestReleaseDate', 'releaseDate': 'releaseDate', 'lts': 'LTS'})
    else:
      df = pandas.DataFrame(data).rename(columns={'support':'Support', 'eol':'EOL', 'latest':'Latest', 'latestReleaseDate':'latestReleaseDate', 'releaseDate': 'releaseDate', 'lts': 'LTS'})
    return df.to_markdown(index=False,tablefmt='fancy_grid')

def notifyProduct():
    for product in NOTIFICATION_PRODUCTS:
      res = endoflifeDate(product)
      if res != None:
        slackText = product + '   \n'
        slackText += jsonToMarkdownTable(res, None)
        print(slackText)

def notifyProductVersion():
    for product,version in NOTIFICATION_PRODUCTS_VERSION.items():
       res = endoflifeDate(product, version)
       if res != None:
        slackText = product + '   \n'
        slackText += jsonToMarkdownTable(res, version)
        print(slackText)
#        sendSlack(slackText)

if __name__ == "__main__":
   notifyProduct()
   notifyProductVersion()