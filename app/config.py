from dotenv import load_dotenv
load_dotenv()

# 環境変数を参照
import os
WEB_HOOK_URL = os.getenv('WEB_HOOK_URL')

NOTIFICATION_PRODUCTS = []
if len(os.getenv('NOTIFICATION_PRODUCTS')) > 0:
    NOTIFICATION_PRODUCTS = os.getenv('NOTIFICATION_PRODUCTS').split()

NOTIFICATION_PRODUCTS_VERSION = {}
if len(os.getenv('NOTIFICATION_PRODUCTS_VERSION')) > 0 :
    npvstr = os.getenv('NOTIFICATION_PRODUCTS_VERSION')
    NOTIFICATION_PRODUCTS_VERSION = dict(item.split('=') for item in npvstr.split())

