from dotenv import load_dotenv
load_dotenv()

# 環境変数を参照
import os
WEB_HOOK_URL = os.getenv('WEB_HOOK_URL')