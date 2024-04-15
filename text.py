import json
import random

import requests
import re
import os
import csv
import time
import Content_gainer
from bs4 import BeautifulSoup
from Url_manager import Url_manager_hotboard
from User_attribute_gainer import get_user_fans_stat,get_token
from get_user_agent import get_user_agent
from toutiao import TTBot
bot = TTBot()
info=bot.get_user_info("52796986240")
print(info)

