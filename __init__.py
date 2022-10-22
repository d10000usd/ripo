import argparse
from os import lseek
from typing import List

import tqdm

import canrevan.parsing as parsing
import canrevan.utils as utils
from canrevan.crawling import Crawler
import time
from datetime import datetime 
DEFAULT_USER_AGENT_STRING = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/87.0.4280.66 "
    "Safari/537.36"
)
savePath = "/Users/hg/WORKSPACE/TELEGRAM/TELE/naverblog/py/뉴스.txt"
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))  




def timeFormatChange(strTime): # 날짜 시간 타입변경 문자를 날자 형식으로 변경
    str_datetime = '20210611'
    str_datetime = strTime
    format = '%Y%m%d'
    dt_datetime = datetime.strptime(str_datetime,format)
    dates = dt_datetime.strftime("%Y-%m-%d")
    return dates
def _main():
    args = _create_argument_parser().parse_args()

    # Create a crawler for collecting article urls and news contents.
    crawler = Crawler(
        concurrent_tasks=args.max_jobs,
        num_parsing_processes=args.num_cores,
        request_headers={"user-agent": args.user_agent},
        request_timeout=args.timeout,
    )

    # Collect article urls from navigation pages.
    
    
    
    ####### 1 링크 준비
    #######
    
    nav_urls = _prepare_nav_urls(args)
    if args.type==1:
        nav_urls = _prepare_nav_urls_entertain(args)
    elif args.type ==2:
        nav_urls = _prepare_nav_urls(args)
    elif args.type ==3:
        nav_urls = _prepare_nav_urls_serchkeyword(args)
    print(f"[*] navigation pages: {nav_urls[0]}")
    # print(f"[*] navigation pages: {nav_urls[1]}")
    print(f"[*] navigation pages: {len(nav_urls)}")


    ####### 2 html에서 링크만 받기
    #######
    if args.type==1:
        parse_fn_s=parsing.extract_article_urls_ent
    elif args.type ==2:
        parse_fn_s=parsing.extract_article_urls
    elif args.type ==3:
        parse_fn_s=parsing.extract_article_urls_searchkeyword
    with tqdm.tqdm(nav_urls, desc="[*] collect article urls") as tbar:
        article_urls = crawler.reduce_to_array(
            nav_urls, parse_fn=parse_fn_s, update_fn=tbar.update
        )

    # Flatten the grouped urls and remove duplicates from the array.
    article_urls = {url for urls in article_urls for url in urls}
    print(f"[*] total collected articles: {len(article_urls)}")

    # Crawl news articles from the collected article urls and save the content to the
    # output file.
    ####### 3 뉴스에서 기사내용만 뽑기
    #######
    if args.type==1:
        parse_fn_s=parsing.parse_article_content_ent
    elif args.type ==2:
        parse_fn_s=parsing.parse_article_content
    elif args.type ==3:
        parse_fn_s=parsing.parse_article_content_searchkeyword
    with tqdm.tqdm(article_urls, desc="[*] crawl news article contents") as tbar:
        total_contents = crawler.reduce_to_file(
            article_urls,
            args.output_path,
            parse_fn=parse_fn_s,
            update_fn=tbar.update,
        )

   
    prRed(f"[*] finish crawling {total_contents} news articles to [{savePath}]")
        #f"[{args.output_path}]"
        
    

def _prepare_nav_urls_origin(args: argparse.Namespace) -> List[str]:
    # https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=102#&date=%2000:00:00&page=10
    return [
        f"https://news.naver.com/main/list.nhn?mode=LSD&mid=shm"
        f"&sid1={category}&date={date}&page={page}"
        for category in args.category
        for date in utils.drange(args.start_date, args.end_date, args.skip_days)
        for page in range(1, args.max_page + 1)
    ]






def _prepare_nav_urls_entertain(args: argparse.Namespace) -> List[str]:

    std= (args.start_date)
    edd = (args.end_date)
    news_url_numbers = {}
        
    drama = [
        f"https://entertain.naver.com/now?sid=221#sid=221&date={timeFormatChange(date)}&page={page}"
        #f"https://entertain.naver.com/now?sid=221#sid=22f&date={timeFormatChange(date)}&page={page}"
        # for category in args.category
        for date in utils.drange(str(std), str(edd), args.skip_days)
        for page in range(1, args.max_page + 1)
    ]
    
    music = [
        
        f"https://entertain.naver.com/now?sid=7a5#sid=7a5&date={timeFormatChange(date)}&page={page}"
        #f"https://entertain.naver.com/now?sid=221#sid=22f&date={timeFormatChange(date)}&page={page}"
        # for category in args.category
        for date in utils.drange(str(std), str(edd), args.skip_days)
        for page in range(1, args.max_page + 1)
    ]
    
    latelyEnt = [
        f"https://entertain.naver.com/now#sid=106&date={timeFormatChange(date)}&page={page}"
        #f"https://entertain.naver.com/now?sid=221#sid=22f&date={timeFormatChange(date)}&page={page}"
        # for category in args.category
        for date in utils.drange(str(std), str(edd), args.skip_days)
        for page in range(1, args.max_page + 1)
    ]
    
    return   latelyEnt+music+drama
    


def _prepare_nav_urls_serchkeyword(args: argparse.Namespace) -> List[str]:

    std= (args.start_date)
    edd = (args.end_date)
    keywords = (args.serchkeyword)
    page = 1
    news_url_numbers = {}
        
    keywordliks = [
        f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={keywords}&start={page}&sort=1"
        #f"https://entertain.naver.com/now?sid=221#sid=22f&date={timeFormatChange(date)}&page={page}"
        # for category in args.category
        for date in utils.drange(str(std), str(edd), args.skip_days)
        for page in range(1, args.max_page + 1)
    ]
    

    
    return   keywordliks
    




def _prepare_nav_urls(args: argparse.Namespace) -> List[str]:
    # https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=229&sid1=105&date=20220624&page=3

    news_url_numbers = {}
    cat =  args.category
    sid1_100 = [264]        # 정치 - 대통령실
    sid1_101 = [258,262]   # 경제 - 증권, 글로번
    sid1_102 = [255]        # 사회 - 의료
    sid1_103 = [239, 243]   # 생활 - 자동차, 책
    sid1_104 = [232, 322]        # 세계 - 미국
    sid1_105 = [230, 229,262]   # it  - it , 게임,증권
    #sid1_105 = [221]
    for i, catVal in enumerate(cat):
        if catVal == 100: #정치
            news_url_numbers['100'] = sid1_100
        if catVal == 101: #경제
            news_url_numbers['101'] = sid1_101
        if catVal == 102: #사회
            news_url_numbers['102'] = sid1_102
        if catVal == 103: #생활
            news_url_numbers['103'] = sid1_103
        if catVal == 104: #세게
            news_url_numbers['104'] = sid1_104
        if catVal == 105: #과학
            news_url_numbers['105'] = sid1_105
        if catVal == 221: #과학
            print("wrong catVal 221 entertain")
            break
            #news_url_numbers['221'] = sid1_105
    print(news_url_numbers)
    return [
   
# https://news.naver.com/main/list.naver?mode=LS2D&sid2=101&sid1=258&mid=shm&date=20220625&page=1
# https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=258&sid1=101&date=20220624&page=4    
# https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=262&sid1=101&date=20220625&page=2  
# https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=101&sid1=262&date=20220625&page=1
# https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=262&sid1=101&date=20220625&page=2
# https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=101&sid1=262&date=20220625&page=1
            f"https://news.naver.com/main/list.naver?mode=LS2D&mid=shm"
            f"&sid2={idx}&sid1={sid1keyBotomCatecory}&date={date}&page={page}"
            
            for nunidx, (sid1keyBotomCatecory, sid2ValTopCatecory) in enumerate(news_url_numbers.items())
            for idx in sid2ValTopCatecory
            for date in utils.drange(args.start_date, args.end_date, args.skip_days)
            for page in range(1, args.max_page + 1)
    ]
def _create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="canrevan", description="crawl naver news articles"
    )

    parser.add_argument(
        #파일저장위치
        #"--output_path", default="articles.txt", help="output file path"
        "--output_path", default=f"{savePath}", help="output file path"
    )
    parser.add_argument(
        "--category",
        required=True,
        nargs="*",
        type=int,
        help="list of news article categories",
    )
    parser.add_argument(
        "--start_date", required=True, help="minimum date of news articles"
    )
    parser.add_argument(
        "--end_date", required=True, help="maximum date of news articles"
    )
    parser.add_argument(
        "--skip_days", default=1, type=int, help="number of days to skip from crawling"
    )
    parser.add_argument(
        "--max_page", default=10, type=int, help="maximum number of pages to navigate"
    )
    parser.add_argument(
        "--timeout", default=5, type=float, help="timeout for the whole request"
    )
    parser.add_argument(
        "--max_jobs",
        default=500,
        type=int,
        help="maximum number of concurrent requests",
    )
    parser.add_argument(
        "--num_cores",
        default=4,
        type=int,
        help="number of multi-processing cores for parsing",
    )
    parser.add_argument(
        "--user-agent",
        default=DEFAULT_USER_AGENT_STRING,
        help="use custom user-agent string",
    )
    parser.add_argument(
        "--type", default=1, type=int, help="news:1, ent:2"
    )
    parser.add_argument(
        "--serchkeyword", default='손흥민', help="search from naver keyword for focusing on mainword "
    )


    return parser
# canrevan --category 221  --start_date 20220625 --end_date 20220625  --max_page 1
# canrevan --category  105 --start_date 20220625 --end_date 20220625  --max_page 1 --type 1

