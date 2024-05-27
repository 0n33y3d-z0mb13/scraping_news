from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from datetime import datetime
import os
from scraping_functions import hacker_news, security_affairs, daily_secu, boan_news, ahnlab_asec, theori_blog, mandiant_blog, s2w_blog, akamai_blog, cloudflare_blog, sans_blog

scraping_functions = [hacker_news, security_affairs, daily_secu, boan_news, ahnlab_asec, theori_blog, mandiant_blog, s2w_blog, akamai_blog, cloudflare_blog, sans_blog]

scraping_functions_names = {
    hacker_news: "The Hacker News",
    security_affairs: "Security Affairs",
    daily_secu: "데일리시큐",
    boan_news: "보안뉴스",
    ahnlab_asec: "안랩 ASEC Blog",
    theori_blog: "Theori Blog",
    mandiant_blog: "Mandiant Blog",
    s2w_blog: "S2W Blog",
    akamai_blog: "Akamai Blog",
    cloudflare_blog: "Cloudflare Blog",
    sans_blog: "SANS Blog"
}

html_content = '''
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                padding: 0;
                background-color: #f4f4f4;
                color: #333;
            }
            h1 {
                text-align: center;
                color: #222;
                background-color: #e2e2e2;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            h2 {
                border-bottom: 2px solid #ddd;
                padding-bottom: 10px;
                color: #444;
                background-color: #eee;
                padding: 10px;
                border-radius: 5px;
            }
            .article {
                margin-bottom: 20px;
                padding: 15px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #fff;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .article h3 {
                color: #0066cc;
            }
            .tag {
                color: #777;
                font-size: 0.9em;
                margin-top: 5px;
            }
            .more {
                text-align: right;
                margin-top: 10px;
            }
            .more a {
                color: #0066cc;
                text-decoration: none;
                font-weight: bold;
            }
            .more a:hover {
                text-decoration: underline;
            }
            .no-articles {
                color: #555;
                font-style: italic;
            }
            footer {
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                text-align: center;
                color: #666;
            }
            footer p {
                margin: 5px 0;
            }
            footer a {
                color: #0066cc;
                text-decoration: none;
            }
            footer a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
    '''

html_footer = '''
    <footer>
        <p>이 페이지는 자동으로 생성되었습니다.</p>
        <p>개발자: 0n33y3d-z0mb13</p>
        <p>문의: <a href="mailto:z0b13@example.com">kminji4466@gmail.com</a></p>
        <p><a href="https://github.com/0n33y3d-z0mb13/scraping_news" target="_blank">GitHub 프로젝트 링크</a></p>
        <p>&copy; 2024 0n33y3d-z0mb13. All rights reserved.</p>
    </footer>
    '''

def send_email(html_content):
    # Get email credentials from 환경변수 
    sender_email_address = os.getenv('EMAIL_ADDRESS')
    sender_email_password = os.getenv('EMAIL_PASSWORD')

    receiver_email_address = sender_email_address

    # Create message object
    message = MIMEMultipart()
    message['From'] = sender_email_address
    message['To'] = receiver_email_address
    message['Subject'] = f"[보안 뉴스 레터] {datetime.now().strftime('%Y-%m-%d')}"

    # Attach HTML content to the message
    message.attach(MIMEText(html_content, 'html'))

    # Create SMTP session
    with smtplib.SMTP('smtp.gmail.com', 587) as session:
        session.starttls()
        session.login(sender_email_address, sender_email_password)
        session.send_message(message)
        session.quit()

def generate_html(article_list):
    # HTML 안에 채워질 기사들을 불러온다.
    html_content = ""
    for article in article_list:
        if article["date"] == datetime.now().strftime('%Y-%m-%d'):
            html_content += f'<div class="article">'
            html_content += f'<a href="{article["url"]}"><h3>{article["title"]}</h3></a>'
            if "tag" in article and article["tag"] != "none":
                html_content += f'<p class="tag">Tag: {article["tag"]}</p>'
            if "content" in article:
                html_content += f'<p>{article["content"]}</p>'
            html_content += f'</div>'        
        else:
            pass
    return html_content

if __name__ == "__main__":
    # html 내용 전체를 저장하는 html_content
    html_content += f'<h1>컴퓨터쟁이가 알려주는 오늘의 새 보안 소식<br>({datetime.now().strftime("%Y-%m-%d")})</h1>'
    html_content += '<p>※ 제목을 누르면 기사로 이동합니다.</p>'
    empty_article = False
    empty_article_platform_list = []

    print("[*] Start scraping news...")
    for scrap_function in scraping_functions:
        function_name = scraping_functions_names.get(scrap_function)
        article_list = scrap_function()

        # 오늘 날짜의 article이 있는지 확인하기 위해 html_article을 따로 둠
        html_article = generate_html(article_list)

        # 기사가 없다면
        if not html_article.strip():
            empty_article = True
            empty_article_platform_list.append(function_name)
        else:
            html_content += f'<h2>{function_name}</h2>'
            empty_article = False
            #html_article += "<hr>"
        html_content += html_article

    # 글을 마무리 하며 새로운 기사가 없는 플랫폼 출력
    if empty_article_platform_list:
        html_content += "<p><b>아래 뉴스(블로그)에는 새로운 기사가 없습니다.</b></p>"
        html_content += ', '.join(empty_article_platform_list)

    html_content += html_footer
    html_content += '</body></html>'

    with open("test.html", "w") as file:
        file.write(html_content)

    # 기사가 없을 경우 메일을 보내지 않는다.
    if not empty_article:
        send_email(html_content)
        print("[+] Email sent successfully!")
