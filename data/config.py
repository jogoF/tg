import os
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TG = os.environ.get("TG_TOKEN")
OWNER = os.environ.get("OWNER")
SERVER_IP = os.environ.get("SERVER_IP")
SERVER_PASS = os.environ.get("SERVER_PASS")
GPT_TOKEN = os.environ.get("GPT_TOKEN")