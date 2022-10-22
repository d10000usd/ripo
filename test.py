from distutils.dir_util import copy_tree
import time
from datetime import datetime 

news_url_numbers = {'101': 258, '101': 262, '105': 229, '100': 268}
category = {'101': 258, '101': 262, '101': 258, '101': 262, '101': 258, '101': 262,
            '101': 258, '101': 262, '101': 258, '101': 262, '101': 258, '101': 262, }
news_url_numbers = {}
cat = [101, 102, 103, 105]
sid1_100 = [258, 262]
sid1_101 = [258, 262]
sid1_102 = [255]
sid1_103 = [239, 243]
sid1_104 = [232]
sid1_105 = [230, 229]
for i, catVal in enumerate(cat):
    if catVal == 100:
        news_url_numbers['100'] = sid1_100
    if catVal == 101:
        news_url_numbers['101'] = sid1_101
    if catVal == 102:
        news_url_numbers['102'] = sid1_102
    if catVal == 103:
        news_url_numbers['103'] = sid1_103
    if catVal == 104:
        news_url_numbers['104'] = sid1_104
    if catVal == 105:
        news_url_numbers['105'] = sid1_105


# [print(f"&sid2={sid1keyBotomCatecory}&sid1={sid2ValTopCatecory[i]}" )for i, (sid1keyBotomCatecory, sid2ValTopCatecory) in enumerate(news_url_numbers.items())]
[print(f"&sid2={sid1keyBotomCatecory}&sid1={idx}")
for cat, (sid1keyBotomCatecory, sid2ValTopCatecory) in enumerate(news_url_numbers.items())
for idx in sid2ValTopCatecory
]

import datetime
str_datetime = '20210611'
format = '%Y%m%d'
dt_datetime = datetime.datetime.strptime(str_datetime,format)
dates = dt_datetime.strftime("%Y-%m-%d")




