from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Chrome 브라우저 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 브라우저 창을 표시하지 않음

# ChromeDriver 경로 설정 및 브라우저 실행
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 페이지 로드
driver.get("https://www.akamai.com/ko/blog")

# 페이지 로드 후 잠시 대기 (JavaScript 로딩 대기)
import time
time.sleep(5)  # 필요에 따라 대기 시간을 조정하세요.

# 페이지 소스 가져오기
page_source = driver.page_source

# BeautifulSoup을 사용하여 HTML 파싱
soup = BeautifulSoup(page_source, 'html.parser')

# 필요한 데이터 추출 예시 (기사 제목들 추출)
articles = soup.find_all('h2', class_='article-title')
for article in articles:
    print(article.text)

# 브라우저 종료
driver.quit()
