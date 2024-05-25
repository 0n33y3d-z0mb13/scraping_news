from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from configparser import ConfigParser
import smtplib
from jinja2 import Template
from datetime import datetime
import os
from scraping_functions import hacker_news, security_affairs, daily_secu, boan_news, ahnlab_asec, theori_blog_vuln, theori_blog_web2, theori_blog_web3, mandiant_blog, s2w_blog, akamai_blog, cloudflare_blog, sans_blog

scraping_functions = [hacker_news, security_affairs, daily_secu, boan_news, ahnlab_asec, theori_blog_vuln, theori_blog_web2, theori_blog_web3, mandiant_blog, s2w_blog, akamai_blog, cloudflare_blog, sans_blog]

def send_email(html_content):
    # Get email credentials from 환경변수 
    sender_email_address = os.getenv('EMAIL_ADDRESS')
    sender_email_password = os.getenv('EMAIL_PASSWORD')

    receiver_email_address = sender_email_address

    # Create message object
    message = MIMEMultipart()
    message['From'] = sender_email_address
    message['To'] = receiver_email_address
    message['Subject'] = f"{datetime.now().strftime('%Y-%m-%d'), 'z0mb13가 알려주는 오늘의 보안 새소식'}"

    # Attach HTML content to the message
    message.attach(MIMEText(html_content, 'html'))

    # Create SMTP session
    with smtplib.SMTP('smtp.gmail.com', 587) as session:
        session.starttls()
        session.login(sender_email_address, sender_email_password)
        session.send_message(message)
        session.quit()

def generate_html(article_list):
    # Create HTML content
    previous_platform = None
    html_content = ""
    for article in article_list:
        #if article["date"] == datetime.now().strftime('%Y-%m-%d'):
        if article["date"] == "2024-05-24":
            if article["platform"] != previous_platform:
                html_content += f"<h2>{article['platform']}</h2>"
            html_content += f'<h3>{article["title"]}</h3>'
            #html_content += f'<p>Date: {article["date"]}</p>'
            if "tag" in article and article["tag"] != "none":
                html_content += f'<p>Tag: {article["tag"]}</p>'
            if "content" in article:
                html_content += f'<p>{article["content"]}</p>'
            html_content += f'<p><a href="{article["url"]}">더 보기</a></p>'
            previous_platform = article["platform"]
        else:
            pass
    return html_content

with open("result.html", "a") as f:
    f.write('<html><body>')
    html_content = ''
    for scrape_function in scraping_functions:
        article_list = scrape_function()
        
        html_content += generate_html(article_list)
        
    html_content += '</body></html>'
    f.write(html_content)
# Send email
# send_email(html_content)