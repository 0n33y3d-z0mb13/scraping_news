from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from configparser import ConfigParser
import requests
from bs4 import BeautifulSoup
import urllib3
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
urllib3.disable_warnings()

def hacker_news():
    """
    Scrapes the Hacker News website and retrieves information about articles.

    Returns:
        list: A list of dictionaries containing information about each article.
            Each dictionary contains the following keys:
            - title: The title of the article.
            - date: The date of the article.
            - url: The URL of the article.
            - tag: The tag associated with the article.
            - content: The content of the article.
    """
    article_list = []

    try:
        # 페이지 요청
        response = requests.get("https://thehackernews.com/", headers=headers, timeout=10)  # 타임아웃 설정
        
        # 요청이 성공했는지 확인
        if response.status_code == 200:
            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.findAll("div", class_="body-post clear")

            for article in articles:
                # 게시물의 제목, url, 날짜, 태그, 내용을 가져와서 딕셔너리에 추가
                title = article.find("h2", class_="home-title").text.strip()
                date = article.find("span", class_="h-datetime").text.strip()
                url = article.find("a", class_="story-link")["href"].strip()
                content = article.find("div", class_="home-desc").text.strip()
                
                try:
                    tag = article.find("span", class_="h-tags").text
                except:
                    tag  = "none"

                article_dict = {
                    "title": title,
                    "date": date[1:],
                    "url": url,
                    "tag": tag,
                    "content": content
                }
                article_list.append(article_dict)
            return article_list
        else:
            print(f"페이지를 가져오는데 실패했습니다. URL: {url}")
    except requests.RequestException as e:
        print(f"페이지 요청 중 오류 발생: {e}")
    
def security_affairs():
    article_list = []

    for i in range(1, 3):  # 여러 페이지의 게시물을 가져오기 위해 반복문 사용 (1페이지부터 2페이지까지
        try:
            response = requests.get(f"https://securityaffairs.com/?page={i}#latest_news_section", timeout=10)  # 타임아웃 설정

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
                    
                    tag = article.find("span", class_="category-tag").text.strip()
                    
                    url = article.find("a")["href"].strip() #첫번째 나오는 a태그의 href 속성값을 가져옴
                    
                    content = article.find("p").text.strip()
                    
                    article_dict = {
                        "title": title,
                        "date": date,
                        "url": url,
                        "tag": tag,
                        "content": content
                    }
                    article_list.append(article_dict)
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
               
                url = article.find("a")["href"].strip()

                article_dict = {
                    "title": title,
                    "date": date[1:],
                    "url": url,
                    "tag": tag,
                    "content": content
                }
                article_list.append(article_dict)
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

                article_dict = {
                    "title": title,
                    "date": date,
                    "url": "https://www.boannews.com" + url,
                    "content": content
                }
                article_list.append(article_dict)
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

                article_dict = {
                    "title": title,
                    "date": date,
                    "url": url,
                    "content": content
                }
                article_list.append(article_dict)
            return article_list
        else:
            print(f"페이지를 가져오는데 실패했습니다. URL: {url}")
    except requests.RequestException as e:
        print(f"페이지 요청 중 오류 발생: {e}")

def theori_blog_vuln():
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

                date = article.find('time').text.strip()
                
                url = article.find("a")["href"].strip() #첫번째 나오는 a태그의 href 속성값을 가져옴
                
                content = article.find("div", class_="u-fontSize18 u-letterSpacingTight u-lineHeightTight u-marginTop7 u-textColorNormal u-baseColor--textNormal").text.strip()
                
                article_dict = {
                    "title": title,
                    "date": date,
                    "url": url,
                    "tag": tag,
                    "content": content
                }
                article_list.append(article_dict)
            return article_list
        else:
            print(f"페이지를 가져오는데 실패했습니다. URL: {url}")
    except requests.RequestException as e:
        print(f"페이지 요청 중 오류 발생: {e}")

def theori_blog_web2():
    article_list = []
 
    try:
        response = requests.get("https://blog.theori.io/web2/home", timeout=10, verify=False)  # 타임아웃 설정

        # 요청이 성공했는지 확인
        if response.status_code == 200:
            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')

            article = soup.find("div", class_="row u-marginTop30 u-marginLeftNegative12 u-marginRightNegative12")
            tag = "Web2 Security"
            
            title = article.find('h3').text.strip()

            date = article.find('time').text.strip()
            
            url = article.find("a")["href"].strip() #첫번째 나오는 a태그의 href 속성값을 가져옴
            
            content = article.find("div", class_="u-fontSize18 u-letterSpacingTight u-lineHeightTight u-marginTop7 u-textColorNormal u-baseColor--textNormal").text.strip()
            
            article_dict = {
                "title": title,
                "date": date,
                "url": url,
                "tag": tag,
                "content": content
            }
            article_list.append(article_dict)
            return article_list
        else:
            print(f"페이지를 가져오는데 실패했습니다. URL: {url}")
    except requests.RequestException as e:
        print(f"페이지 요청 중 오류 발생: {e}")

def theori_blog_web3():
    article_list = []
 
    try:
        response = requests.get("https://blog.theori.io/web3/home", timeout=10, verify=False)  # 타임아웃 설정

        # 요청이 성공했는지 확인
        if response.status_code == 200:
            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')

            article = soup.find("div", class_="row u-marginTop30 u-marginLeftNegative12 u-marginRightNegative12")
            tag = "Web2 Security"
            
            title = article.find('h3').text.strip()

            date = article.find('time').text.strip()
            
            url = article.find("a")["href"].strip() #첫번째 나오는 a태그의 href 속성값을 가져옴
            
            content = article.find("div", class_="u-fontSize18 u-letterSpacingTight u-lineHeightTight u-marginTop7 u-textColorNormal u-baseColor--textNormal").text.strip()
            
            article_dict = {
                "title": title,
                "date": date,
                "url": url,
                "tag": tag,
                "content": content
            }
            article_list.append(article_dict)
            return article_list
        else:
            print(f"페이지를 가져오는데 실패했습니다. URL: {url}")
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

                article_dict = {
                    "title": title,
                    "date": date,
                    "url": url,
                }
                article_list.append(article_dict)
            return article_list
        else:
            print(f"페이지를 가져오는데 실패했습니다. URL: {url}")
    except requests.RequestException as e:
        print(f"페이지 요청 중 오류 발생: {e}")

def s2w_blog():
    article_list = []

    try:
        response = requests.get("https://s2w.medium.com/", timeout=10, verify=False)  # 타임아웃 설정

        # 요청이 성공했는지 확인
        if response.status_code == 200:
            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')
            articles_div = soup.find("div", class_="l ae")
            articles = articles_div.findAll("div", class_="ab cm")
            
            for article in articles:
                # 고정되어 있는 게시물인 경우 패스한다.
                if article.find('div', class_="be b do z dn ab ld hb"):
                    continue
                
                title = article.find('h2').text.strip()

                url = article.find('a', class_="af ag ah ai aj ak al am an ao ap aq ar as at")["href"].strip() 
                
                date_div = article.find("div", class_="nh ni nj nk nl ab q")
                date_spans = date_div.find_all("span")
                date = date_spans[3].text if len(date_spans) > 2 else None

                article_dict = {
                    "title": title,
                    "date": date,
                    "url": "https://medium.com/s2wblog"+url,
                }
                article_list.append(article_dict)
            return article_list
        else:
            print(f"페이지를 가져오는데 실패했습니다. URL: {url}")
    except requests.RequestException as e:
        print(f"페이지 요청 중 오류 발생: {e}")

def akamai_blog():
    article_list = []

    try:
        # headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        # }
        # response = requests.get("https://www.akamai.com/ko/blog", headers=headers, timeout=10, verify=False)  # 타임아웃 설정
        with open('/home/zombie/2401_Dongguk/response.html', 'r') as file:
            r = file.read()

            #file.write(response.text)
        # 요청이 성공했는지 확인
        #if response.status_code == 200:
            # HTML 파싱
            #soup = BeautifulSoup(response.text, 'html.parser')
            soup = BeautifulSoup(r, 'html.parser')
            parent_div = soup.find('div', class_='filter-items__items__list')
            print(parent_div)
            articles = parent_div.find('div', recursive=False)
            
            for article in articles:
                title = article.find('h2').text.strip()

                url = article.find("a")["href"].strip() #첫번째 나오는 a태그의 href 속성값을 가져옴                

                content = article.find("p").text.strip()

                date = article.find("div", class_="Post__author").text.strip()

                article_dict = {
                    "title": title,
                    "date": date,
                    "url": "https://www.akamai.com/"+url,
                    "content": content
                }
                article_list.append(article_dict)
            return article_list
        # else:
        #     print(f"페이지를 가져오는데 실패했습니다. URL: {url}")
    except requests.RequestException as e:
        print(f"페이지 요청 중 오류 발생: {e}")

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

                content = article.find("p", attrs={"data-testid":"post-content"}).text.strip()

                tag = "none"
                if article.find("a", class_="dib pl2 pr2 pt1 pb1 mb2 bg-gray8 no-underline blue3 f2 mr1"):
                    tag = article.find("a", attrs={"data-testid": "post-tag"}).text.strip()

                article_dict = {
                    "title": title,
                    "date": date,
                    "url": "https://blog.cloudflare.com/tag/security"+url,
                    "tag": tag,
                    "content": content
                }
                article_list.append(article_dict)
            return article_list
        else:
            print(f"페이지를 가져오는데 실패했습니다. URL: {url}")
    except requests.RequestException as e:
        print(f"페이지 요청 중 오류 발생: {e}")

def sans_blog():
    article_list = []

    try:
        response = requests.get("https://www.sans.org/blog/", timeout=10, verify=False)  # 타임아웃 설정

        # 요청이 성공했는지 확인
        if response.status_code == 200:
            # HTML 파싱
            with open("./response.html", "w") as file:
                file.write(response.text)
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.findAll("li", class_="article-listing__item")
            print(articles)
            
            for article in articles:
                title = article.find('div', class_="title").text.strip()

                url = article.find("a")["href"].strip() #첫번째 나오는 a태그의 href 속성값을 가져옴                
                
                date = article.find("div", class_="date with-category").text.strip()

                content = article.find("div", class_="description whitespace-break-spaces").text.strip()
                article_dict = {
                    "title": title,
                    "date": date,
                    "url": "https://www.sans.org/"+url,
                    "tag": "none",
                    "content": content
                }
                article_list.append(article_dict)
            return article_list
        else:
            print(f"페이지를 가져오는데 실패했습니다. URL: {url}")
    except requests.RequestException as e:
        print(f"페이지 요청 중 오류 발생: {e}")

articles_list = theori_blog_vuln()

for article in articles_list:
    print(article)
    print("\n")

articles_list = theori_blog_web2()

for article in articles_list:
    print(article)
    print("\n")


articles_list = theori_blog_web3()

for article in articles_list:
    print(article)
    print("\n")