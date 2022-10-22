import json
import re
from typing import List

from bs4 import BeautifulSoup, SoupStrainer

import canrevan.utils as utils
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))  


def extract_article_urls_ent(document: str) -> List[str]:
    
    
    #만이본 뉴스10 따로 뽑기
    doctemp=document
    article_urls = []
    document_ent = document[document.find('<div class="box" id="ranking_news">') :]#section_body type06_headline
    document_ent = document_ent[: document_ent.find("</ul>")]
   





    document = document[document.find('<div id="content">') :]#section_body type06_headline
    # Extract article url containers.
    document = document[: document.find('<div id="footer">') ]
    list1 = document[: document.find("</ul>")]
    list2 = document[document.find("</ul>") + 5 :]
    list2 = list2[: list2.find("</ul>")]
    document = list1 + list2
    document = document+ document_ent
    # Extract all article urls from the containers.
    # article_urls = []
    while "<li>" in document:
        document = document[document.find("<li>") :]
        container = document[: document.find("</li>")]

        if not container.strip():
            continue

        article_urls.append("https://entertain.naver.com"+re.search(r'href="(.*?)"', container).group(1))
        document = document[document.find("</li>") :]


    article_urls = list(set(article_urls)) 

    # 리스트를 딕셔너리, 딕셔너리를 리스트로
    # arr = [6, 5, 6, 4, 4, 1, 1, 2, 3, 9, 8, 7, 9, 8, 7]
    # result1 = set(arr)
    # print(f"set(arr)      : {result1}")
    # result2 = list(result1)  # list(set(arr))
    # print(f"list(set(arr) : {result2}")
    # arr = [6, 5, 6, 4, 4, 1, 1, 2, 3, 9, 8, 7, 9, 8, 7]
    # result1 = dict.fromkeys(arr) # 리스트 값들을 key 로 변경
    # print(result1)
    # result2 = list(result1) # list(dict.fromkeys(arr))
    # print(result2)


    return article_urls

    
def extract_article_urls_searchkeyword(document: str) -> List[str]:
    document = document[document.find('<ul class="list_news">') :]
    
    document = document[: document.find('<div class="banner_area">') ]
    list1 = document[: document.find("</ul>")]
    list2 = document[document.find("</ul>") + 5 :]
    list2 = list2[: list2.find("</ul>")]
        
    document = list1 + list2

    # Extract all article urls from the containers.
    article_urls = []
    while "<dt>" in document:
        document = document[document.find("<dt>") :]
        container = document[: document.find("</dt>")]

        if not container.strip():
            continue

        article_urls.append(re.search(r'<a href="(.*?)"', container).group(1))
        document = document[document.find("</dt>") :]
    article_urls = list(set(article_urls)) 
    return article_urls
def extract_article_urls(document: str) -> List[str]:
    document = document[document.find('<ul class="type06_headline">') :]

    # Extract article url containers.
    list1 = document[: document.find("</ul>")]
    list2 = document[document.find("</ul>") + 5 :]
    list2 = list2[: list2.find("</ul>")]

    document = list1 + list2

    # Extract all article urls from the containers.
    article_urls = []
    while "<dt>" in document:
        document = document[document.find("<dt>") :]
        container = document[: document.find("</dt>")]

        if not container.strip():
            continue

        article_urls.append(re.search(r'<a href="(.*?)"', container).group(1))
        document = document[document.find("</dt>") :]
    article_urls = list(set(article_urls)) 
    return article_urls


def parse_article_Title_content(document: str) -> str:
    strainer = SoupStrainer("h2", attrs={"class": "media_end_head_headline"})
    document = BeautifulSoup(document, "lxml", parse_only=strainer)
    content = document.find("h2")
    #print(content)
    content = content.get_text(separator="\n").strip()
    content = "\n".join([line.strip() for line in content.splitlines() if line.strip()])

    pattern = '\[[^)]*\]'
    x = '이건 [괄호 안의 불필요한 정보를]삭제하는 코드다.'
    x = content
    headLineTit = re.sub(pattern=pattern, repl='', string= x) 
    

    headLineTit = re.sub('[-=+/:^.@*\"※~ㆍ!』‘|\(\)\[\]`\\n`\'…》\”\“\’·,]', ' ', headLineTit)
    headLineTit = ' '.join(headLineTit.split()) #문자열 타입     #text = (text.split()) #배열타입
    return headLineTit+". &&& . "


def parse_article_content(document: str) -> str:
    headLineTit = parse_article_Title_content(document)
    
    
    strainer = SoupStrainer("div", attrs={"id": "dic_area"})
    document = BeautifulSoup(document, "lxml", parse_only=strainer)
    content = document.find("div")

    # Skip invalid articles which do not contain news contents.
    if content is None:
        raise ValueError("there is no any news article content.")

    # Remove unnecessary tags except `<br>` elements for preserving line-break
    # characters.
    for child in content.find_all():
        if child.name != "br":
            child.clear()
            
            

        
    content = content.get_text(separator="\n").strip()
    content = "\n".join([line.strip() for line in content.splitlines() if line.strip()])
    
    # Skip the contents which contain too many non-Korean characters.
    
    skipList = ["날씨","공감언론","속보","기자 입니다","MBN","KBS"]
    for idx, val in enumerate(skipList):
        if val in str(content):
            raise ValueError("Article have a skip word in the content.")
    


    # Normalize the contents by removing abnormal sentences.
    content = "\n".join(
        [
            line
            for line in content.splitlines()
            if utils.is_normal_character(line[0]) and line[-1] == "."
        ]
    )

    content=headLineTit+content
    if len(str(content)) <350:
        raise ValueError("there are too few Article in the content.")
    
    return json.encoder.encode_basestring(content)





def parse_article_content_ent(document: str) -> str:
    

    #headLineTit = parse_article_Title_content(document)
    
    #뉴스
    #strainer = SoupStrainer("div", attrs={"id": "dic_area"})
    
    #연예
    strainer = SoupStrainer("div", attrs={"id": "articeBody"})
    document = BeautifulSoup(document, "lxml", parse_only=strainer)
    content = document.find("div")
    

        

    # Skip invalid articles which do not contain news contents.
    if content is None:
        raise ValueError("there is no any news article content.")

    # Remove unnecessary tags except `<br>` elements for preserving line-break
    # characters.
    for child in content.find_all():
        if child.name != "br":
            child.clear()


    content = content.get_text(separator="\n").strip()
    content = "\n".join([line.strip() for line in content.splitlines() if line.strip()])
    # print("11111111111")
    # print()
    # print()
    # print() 
    # print()
    # print(content)
    # print("11111111111")      

    # Skip the contents which contain too many non-Korean characters.
    
    skipList = ["날씨","공감언론","속보","기자 입니다","MBN","KBS"]
    for idx, val in enumerate(skipList):
        if val in str(content):
            raise ValueError("Article have a skip word in the content.")
    


    # Normalize the contents by removing abnormal sentences.
    content = "\n".join(
        [
            line
            for line in content.splitlines()
            if utils.is_normal_character(line[0]) and line[-1] == "."
        ]
    )

    content=content
    
        

    if len(str(content)) <260:
        raise ValueError("there are too few Article in the content.")
    
    return json.encoder.encode_basestring(content)\

def parse_article_content_searchkeyword(document: str) -> str:
    headLineTit = parse_article_Title_content(document)
    
    
    strainer = SoupStrainer("div", attrs={"id": "article-body"})
    document = BeautifulSoup(document, "lxml", parse_only=strainer)
    content = document.find("div")

    # Skip invalid articles which do not contain news contents.
    if content is None:
        raise ValueError("there is no any news article content.")

    # Remove unnecessary tags except `<br>` elements for preserving line-break
    # characters.
    for child in content.find_all():
        if child.name != "br":
            child.clear()
            
            

        
    content = content.get_text(separator="\n").strip()
    content = "\n".join([line.strip() for line in content.splitlines() if line.strip()])
    
    # Skip the contents which contain too many non-Korean characters.
    
    skipList = ["날씨","공감언론","속보","기자 입니다","MBN","KBS"]
    for idx, val in enumerate(skipList):
        if val in str(content):
            raise ValueError("Article have a skip word in the content.")
    


    # Normalize the contents by removing abnormal sentences.
    content = "\n".join(
        [
            line
            for line in content.splitlines()
            if utils.is_normal_character(line[0]) and line[-1] == "."
        ]
    )

    content=headLineTit+content
    if len(str(content)) <350:
        raise ValueError("there are too few Article in the content.")
    
    return json.encoder.encode_basestring(content)




#canrevan --category 101  --start_date 20220523 --end_date 20220625  --max_page 2