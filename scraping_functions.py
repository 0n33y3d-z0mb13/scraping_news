import requests
from bs4 import BeautifulSoup
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import time
from datetime import datetime
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
urllib3.disable_warnings()

# 셀레니움 설정
chrome_options = Options() # 크롬 옵션 설정
chrome_options.add_argument("--headless")  # 브라우저 창을 띄우지 않음
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install()) 
driver = webdriver.Chrome(service=service, options=chrome_options) # 크롬 드라이버 설정

# 헤더 설정
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

def hacker_news():
    article_list = []
    try:
        # RSS 피드를 가져옴
        response = requests.get("https://feeds.feedburner.com/TheHackersNews")

        # HTTP 요청이 성공했는지 확인
        if response.status_code == 200:
            # XML 데이터 파싱
            root = ET.fromstring(response.content)
            
            for item in root.findall('.//item'):
                title = item.find('title').text
                content = item.find('description').text
                url = item.find('link').text
                date = item.find('pubDate').text

                # pubDate 문자열을 파싱하여 datetime 객체로 변환
                date_obj = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
                formatted_date = date_obj.strftime("%Y-%m-%d")

                article_dict = {
                "platform": "The Hacker News",
                "title": title,
                "date": formatted_date,
                "url": url,
                "tag": "none",
                "content": content
                }
                article_list.append(article_dict)
            print("[+] hacker news parsing done...")
            return article_list
        else:
            print(f"페이지를 가져오는데 실패했습니다. 응답 코드: ", response.status_code)
    except Exception as e:
        print(f"RSS 피드를 가져오는 동안 오류 발생: {e}")

def security_affairs():
    article_list = []

    for i in range(1, 3):  # 여러 페이지의 게시물을 가져오기 위해 반복문 사용 (1페이지부터 2페이지까지)
        try:
            response = requests.get(f"https://securityaffairs.com/?page={i}#latest_news_section", headers=headers, timeout=10)
            # 요청이 성공했는지 확인
            if response.status_code == 200:
                # HTML 파싱
                soup = BeautifulSoup(response.text, 'html.parser')
                articles = soup.findAll("div", class_="news-card mb-4 mb-lg-5")
                
                for article in articles:
                    # 게시물의 제목, url, 날짜, 태그, 내용을 가져와서 딕셔너리에 추가
                    title = article.find('h5', class_="mb-3").find('a').text

                    date_img = article.find('img', src="https://securityaffairs.com/wp-content/themes/security_affairs/images/clock-icon.svg")
                    date = date_img.parent.parent.text.strip()  #img태그의 부모의 부모 요소를 가져옴. 날짜 앞에 항상 붙는 이미지를 이용함.
                    # 날짜 변환
                    date_obj = datetime.strptime(date, "%B %d, %Y")
                    formatted_date = date_obj.strftime("%Y-%m-%d")

                    tag = article.find("span", class_="category-tag").text.strip()
                    
                    url = article.find("a")["href"].strip() #첫번째 나오는 a태그의 href 속성값을 가져옴
                    
                    content = article.find("p").text.strip()
                    
                    article_dict = {
                        "platform": "Security Affairs",
                        "title": title,
                        "date": formatted_date,
                        "url": url,
                        "tag": tag,
                        "content": content
                    }
                    article_list.append(article_dict)
                print("[+] security_affairs parsing done...")
                return article_list
            else:
                print(f"페이지를 가져오는데 실패했습니다. URL: {url}")
        except requests.RequestException as e:
            print(f"페이지 요청 중 오류 발생: {e}")

def daily_secu():
    article_list = []

    try:
        # 페이지 요청
        response = requests.get("https://www.dailysecu.com/news/articleList.html?view_type=sm", timeout=10)  # 타임아웃 설정
        
        # 요청이 성공했는지 확인
        if response.status_code == 200:
            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.findAll("div", class_="list-block")

            for article in articles:
                # 게시물의 제목, url, 날짜, 태그, 내용을 가져와서 딕셔너리에 추가
                title = article.find("div", class_="list-titles").text.strip()
                content = article.find("p", class_="list-summary").text.strip()
                tagNdate = article.find("div", class_="list-dated").text.strip()

                tag = tagNdate.split("|")[0].strip()
                date = tagNdate.split("|")[2].strip()

                date_time_obj = datetime.strptime(date, "%Y-%m-%d %H:%M")
                formatted_date = date_time_obj.strftime("%Y-%m-%d")

                url = article.find("a")["href"].strip()

                article_dict = {
                    "platform": "데일리시큐",
                    "title": title,
                    "date": formatted_date,
                    "url": url,
                    "tag": tag,
                    "content": content
                }
                article_list.append(article_dict)
            print("[+] dailysecu parsing done...")
            return article_list
        else:
            print(f"페이지를 가져오는데 실패했습니다. URL: {url}")
    except requests.RequestException as e:
        print(f"페이지 요청 중 오류 발생: {e}")

def boan_news():
    article_list = []

    try:
        response = requests.get("https://www.boannews.com/media/list.asp?mkind=1", timeout=10, verify=False)  # 타임아웃 설정

        # 요청이 성공했는지 확인
        if response.status_code == 200:
            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.findAll("div", class_="news_list")
            
            for article in articles:
                title = article.find('span', class_="news_txt").text.strip()

                url = article.find("a")["href"].strip() #첫번째 나오는 a태그의 href 속성값을 가져옴                

                content = article.find("a", class_="news_content").text.strip()

                writerNdate = article.find("span", class_="news_writer").text
                date = writerNdate.split("|")[1].strip()

                date_time_obj = datetime.strptime(date, "%Y년 %m월 %d일 %H:%M")
                date_obj = date_time_obj.date()
                formatted_date = date_obj.strftime("%Y-%m-%d")

                article_dict = {
                    "platform": "보안뉴스",
                    "title": title,
                    "date": formatted_date,
                    "url": "https://www.boannews.com" + url,
                    "content": content
                }
                article_list.append(article_dict)
            print("[+] boan news parsing done...")
            return article_list
        else:
            print(f"페이지를 가져오는데 실패했습니다. URL: {url}")
    except requests.RequestException as e:
        print(f"페이지 요청 중 오류 발생: {e}")

def ahnlab_asec():
    article_list = []

    try:
        response = requests.get("https://asec.ahnlab.com/ko/", timeout=10, verify=False)  # 타임아웃 설정

        # 요청이 성공했는지 확인
        if response.status_code == 200:
            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.findAll("article")
            
            for article in articles:
                title = article.find('h2', class_="posttitle").text.strip()

                url = article.find("a")["href"].strip() #첫번째 나오는 a태그의 href 속성값을 가져옴                

                content = article.find("p").text.strip()

                date = article.find("time").text.strip()
                date_time_obj = datetime.strptime(date, "%Y년 %m월 %d일")
                formatted_date = date_time_obj.strftime("%Y-%m-%d")

                article_dict = {
                    "platform": "안랩 ASEC",
                    "title": title,
                    "date": formatted_date,
                    "url": url,
                    "content": content
                }
                article_list.append(article_dict)
            print("[+] ahnlab asec parsing done...")
            return article_list
        else:
            print(f"페이지를 가져오는데 실패했습니다. URL: {url}")
    except requests.RequestException as e:
        print(f"페이지 요청 중 오류 발생: {e}")

def theori_blog():
    article_list = []
 
    try:
        response = requests.get("https://blog.theori.io/vulnerability-research/home", timeout=10, verify=False)  # 타임아웃 설정

        # 요청이 성공했는지 확인
        if response.status_code == 200:
            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')

            articles = soup.findAll("div", class_="col u-xs-size12of12 js-trackPostPresentation u-paddingLeft12 u-marginBottom15 u-paddingRight12 u-size6of12")
            tag = "Vulnerability Research"
            for article in articles:
                # 게시물의 제목, url, 날짜, 태그, 내용을 가져와서 딕셔너리에 추가
                title = article.find('h3').text.strip()

                # <time datetime="2021-10-07T00:00:00Z"> 이런 모양임. 
                date = article.find('time')['datetime'].strip()
                date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
                formatted_date = date_obj.strftime("%Y-%m-%d")

                url = article.find("a")["href"].strip() #첫번째 나오는 a태그의 href 속성값을 가져옴
                
                content = article.find("div", class_="u-fontSize18 u-letterSpacingTight u-lineHeightTight u-marginTop7 u-textColorNormal u-baseColor--textNormal").text.strip()
                
                article_dict = {
                    "platform": "Theori Blog",
                    "title": title,
                    "date": formatted_date,
                    "url": url,
                    "tag": tag,
                    "content": content
                }
                article_list.append(article_dict)
            print("[+] theori blog vuln parsing done...")
        else:
            print(f"[-] theori blog vuln: 페이지를 가져오는데 실패했습니다. URL: {url}")

        response = requests.get("https://blog.theori.io/web2/home", timeout=10, verify=False)  # 타임아웃 설정

        # 요청이 성공했는지 확인
        if response.status_code == 200:
            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')

            article = soup.find("div", class_="row u-marginTop30 u-marginLeftNegative12 u-marginRightNegative12")
            tag = "Web2 Security"
            
            title = article.find('h3').text.strip()

            # <time datetime="2021-10-07T00:00:00Z"> 이런 모양임. 
            date = article.find('time')['datetime'].strip()
            date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
            formatted_date = date_obj.strftime("%Y-%m-%d")

            url = article.find("a")["href"].strip() #첫번째 나오는 a태그의 href 속성값을 가져옴
            
            content = article.find("div", class_="u-fontSize18 u-letterSpacingTight u-lineHeightTight u-marginTop7 u-textColorNormal u-baseColor--textNormal").text.strip()
            
            article_dict = {
                "platform": "Theori Blog",
                "title": title,
                "date": formatted_date,
                "url": url,
                "tag": tag,
                "content": content
            }
            article_list.append(article_dict)
            print("[+] theori blog web2 parsing done...")
        else:
            print(f"[-] theori blog web2: 페이지를 가져오는데 실패했습니다. URL: {url}")

        response = requests.get("https://blog.theori.io/web3/home", timeout=10, verify=False)  # 타임아웃 설정

        # 요청이 성공했는지 확인
        if response.status_code == 200:
            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')

            article = soup.find("div", class_="row u-marginTop30 u-marginLeftNegative12 u-marginRightNegative12")
            tag = "Web3 Security"
            
            title = article.find('h3').text.strip()

            # <time datetime="2021-10-07T00:00:00Z"> 이런 모양임. 
            date = article.find('time')['datetime'].strip()
            date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
            formatted_date = date_obj.strftime("%Y-%m-%d")

            url = article.find("a")["href"].strip() #첫번째 나오는 a태그의 href 속성값을 가져옴
            
            content = article.find("div", class_="u-fontSize18 u-letterSpacingTight u-lineHeightTight u-marginTop7 u-textColorNormal u-baseColor--textNormal").text.strip()
            
            article_dict = {
                "platform": "Theori Blog",
                "title": title,
                "date": date,
                "url": formatted_date,
                "tag": tag,
                "content": content
            }
            article_list.append(article_dict)
            print("[+] theori blog web3 parsing done...")
            return article_list
        else:
            print(f"[-] theori blog web3: 페이지를 가져오는데 실패했습니다. URL: {url}")
    except requests.RequestException as e:
        print(f"페이지 요청 중 오류 발생: {e}")

def mandiant_blog():
    article_list = []

    try:
        response = requests.get("https://www.mandiant.com/resources/blog", timeout=10, verify=False)  # 타임아웃 설정

        # 요청이 성공했는지 확인
        if response.status_code == 200:
            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.findAll("a", class_="resources-card")
            
            for article in articles:
                title = article.find('h3').text.strip()

                url = article["href"].strip() #첫번째 나오는 a태그의 href 속성값을 가져옴                
                
                date = article.find("span", class_="date string body-size-m").text.strip()
                date_obj = datetime.strptime(date, "%b %d, %Y")
                formatted_date = date_obj.strftime("%Y-%m-%d")

                article_dict = {
                    "platform": "Mandiant Blog",
                    "title": title,
                    "date": formatted_date,
                    "url": url,
                }
                article_list.append(article_dict)
            print("[+] mandiant blog parsing done...")
            return article_list
        else:
            print(f"페이지를 가져오는데 실패했습니다. URL: {url}")
    except requests.RequestException as e:
        print(f"페이지 요청 중 오류 발생: {e}")

def s2w_blog():
    article_list = []
    timeout=10
    max_retries = 3
    attempts = 0

    # 타임 아웃이 빈번히 발생하므로 요청이 갈 때 까지 무한 루프를 돌림
    while attempts < max_retries:
        try:
            response = requests.get("https://s2w.medium.com/", headers=headers, timeout=timeout, verify=False)  # 타임아웃 설정

            # 요청이 성공했는지 확인
            if response.status_code == 200:
                # HTML 파싱
                soup = BeautifulSoup(response.text, 'html.parser')
                articles_div = soup.find("div", class_="l ae")

                # 기사를 불러오지 못하는 경우 재시도
                if not articles_div:
                    print("[-] s2w blog: Unable to find the article list. Retrying...")
                    attempts += 1
                    timeout += 5  # Increase timeout
                    continue

                articles = articles_div.findAll("div", class_="ab cm")
                
                for article in articles:
                    # 고정되어 있는(가장 상단에 pinned 된) 게시물인 경우 패스한다.
                    if article.find('div', class_="be b do z dn ab ld hb"):
                        continue
                    
                    title = article.find('h2').text.strip()
                    url = article.find('a', class_="af ag ah ai aj ak al am an ao ap aq ar as at")["href"].strip() 
                
                    date_div = article.find("div", class_="nh ni nj nk nl ab q")
                    if not date_div:
                        print("[-] s2w blog: Unable to find the date_div. Retrying...")
                        attempts += 1
                        timeout += 5  # Increase timeout
                        continue
                    date_spans = date_div.find_all("span")
                    date = date_spans[3].text if len(date_spans) > 2 else None
                    date_obj = datetime.strptime(date, "%b %d, %Y")
                    formatted_date = date_obj.strftime("%Y-%m-%d")

                    article_dict = {
                        "platform": "S2W Blog",
                        "title": title,
                        "date": formatted_date,
                        "url": "https://medium.com/s2wblog"+url,
                    }
                    article_list.append(article_dict)
                print("[+] s2w blog parsing done...")
                return article_list
            else:
                print(f"[-] s2w blog: Request failed. Status code: {response.status_code}, URL: {url}")
                attempts += 1
                timeout += 5  # 타임아웃 증가
        except requests.exceptions.Timeout:
            attempts += 1
            timeout += 5
            print(f"[-] s2w blog: Request timed out. Increasing timeout to {timeout} and retrying...")
        except requests.RequestException as e:
            print(f"[-] s2w blog: {e}")
            return article_list  # 심각한 오류 발생 시 함수 종료
    print("[-] s2w blog: Exceeded maximum number of retries. ")
    return article_list

def akamai_blog():
    article_list = []

    try:
        # RSS 피드를 가져옴
        response = requests.get("https://feeds.feedburner.com/akamai/blog", headers=headers, timeout=20, verify=False)

        # HTTP 요청이 성공했는지 확인
        if response.status_code == 200:
            # XML 데이터 파싱
            root = ET.fromstring(response.content)

            for item in root.findall('.//item')[:15]:
                title = item.find('title').text
                url = item.find('link').text
                content = item.find('description').text
                date = item.find('pubDate').text
                # pubDate 문자열을 파싱하여 datetime 객체로 변환
                date_obj = datetime.strptime(date[:-4], "%a, %d %b %Y %H:%M:%S")
                formatted_date = date_obj.strftime("%Y-%m-%d")

                article_dict = {
                "platform": "Akamai Blog",
                "title": title,
                "date": formatted_date,
                "url": url,
                "content": content
                }
                article_list.append(article_dict)
            print("[+] akamai blog parsing done...")
            return article_list
        else:
            print(f"페이지를 가져오는데 실패했습니다. 응답 코드: ", response.status_code)
    except Exception as e:
        print(f"RSS 피드를 가져오는 동안 오류 발생: {e}")

def cloudflare_blog():
    article_list = []

    try:
        response = requests.get("https://blog.cloudflare.com/tag/security", timeout=10, verify=False)  # 타임아웃 설정

        # 요청이 성공했는지 확인
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.findAll("article")
            articles = articles[:5] # 가져올 기사의 개수를 5개로 제한(최신글만 가져옴)

            for article in articles:
                title = article.find("h2").text.strip()

                url = article.find("a", attrs={"data-testid":"post-title"})["href"] #첫번째 나오는 a태그의 href 속성값을 가져옴                

                date = article.find("p", attrs={"data-testid":"post-date"}).text.strip()
                date_obj = datetime.strptime(date, "%m/%d/%Y")
                formatted_date = date_obj.strftime("%Y-%m-%d")

                content = article.find("p", attrs={"data-testid":"post-content"}).text.strip()

                tag = "none"
                if article.find("a", class_="dib pl2 pr2 pt1 pb1 mb2 bg-gray8 no-underline blue3 f2 mr1"):
                    tag = article.find("a", attrs={"data-testid": "post-tag"}).text.strip()

                article_dict = {
                    "platform": "Cloudflare Blog",
                    "title": title,
                    "date": formatted_date,
                    "url": "https://blog.cloudflare.com/tag/security"+url,
                    "tag": tag,
                    "content": content
                }
                article_list.append(article_dict)
            print("[+] cloudflare blog parsing done...")
            return article_list
        else:
            print(f"페이지를 가져오는데 실패했습니다. URL: {url}")
    except requests.RequestException as e:
        print(f"페이지 요청 중 오류 발생: {e}")

def sans_blog():
    article_list = []

    try:
        # 웹 페이지 열기
        driver.get("https://www.sans.org/blog/")

        # 필요한 데이터가 로드될 때까지 대기 (예: 10초 대기)
        driver.implicitly_wait(10)

        # 페이지 소스 가져오기
        html = driver.page_source


        # HTML 파싱
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.findAll("li", class_="article-listing__item")

        for article in articles:
            title = article.find('div', class_="title").text.strip()
            url = article.find("a")["href"].strip() #첫번째 나오는 a태그의 href 속성값을 가져옴                
            tag = article.find("div", class_="category").text.strip()
            date = article.find("div", class_="date with-category").text.strip()
            date_obj = datetime.strptime(date, "%b %d, %Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            content = article.find("div", class_="description whitespace-break-spaces").text.strip()

            article_dict = {
                "platform": "SANS Blog",
                "title": title,
                "date": formatted_date,
                "url": "https://www.sans.org/"+url,
                "tag": tag,
                "content": content
            }
            article_list.append(article_dict)

        print("[+] sans blog parsing done...")
        driver.quit()
        return article_list
    except requests.RequestException as e:
        print(f"페이지 요청 중 오류 발생: {e}")
