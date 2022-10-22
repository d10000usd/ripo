from distutils.dir_util import copy_tree
import time
from datetime import datetime 
import ssl
from asyncio import AbstractEventLoop
from datetime import datetime, timedelta
from typing import Dict, List

def timeFormatChange(strTime): # 날짜 시간 타입변경 문자를 날자 형식으로 변경
   


    str_datetime = strTime
    format = '%Y%m%d'
    dt_datetime = datetime.strptime(str_datetime,format)
    dates = dt_datetime.strftime("%Y-%m-%d")
 
    
    return(dates)
def drange(start: str, end: str, step: int = 1) -> List[str]:
    start_date = datetime.strptime(start, "%Y%m%d")
    end_date = datetime.strptime(end, "%Y%m%d")

    iters = (end_date - start_date).days // step
    return [
        (start_date + timedelta(days=d * step)).strftime("%Y%m%d")
        for d in range(iters + 1)
    ]


start_date = ('20201110')
end_date = ('20201120')
skip_days = 1
maxpage =1
[print(f"https://entertain.naver.com/now?sid=221#sid=22f&date={timeFormatChange(date)}&page={page})")
# for category in args.category

for date in drange(start_date, end_date, skip_days)

for page in range(1, maxpage + 1)]



start_date = timeFormatChange('20201110')
print(start_date)
Y, M, D = start_date.split('-')
date = f"{Y}{M}{D}"
print(date)


