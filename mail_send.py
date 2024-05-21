import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
from datetime import datetime

# 수집된 기사 예시 (원래는 위의 스크래핑 함수에서 가져옵니다)
hacker_news = [
    {"title": "Example Title 1", "url": "https://example.com/article1", "date": "2024-05-16", "tag": "Security", "content": "Example content 1..."},
    {"title": "Example Title 2", "url": "https://example.com/article2", "date": "2024-05-16", "tag": "Vulnerability", "content": "Example content 2..."}
]
security_affairs = [
    {"title": "Example Title 3", "url": "https://example.com/article3", "date": "2024-05-16", "tag": "Malware", "content": "Example content 3..."},
    {"title": "Example Title 4", "url": "https://example.com/article4", "date": "2024-05-16", "tag": "Incident", "content": "Example content 4..."}
]
boan_news = [
    {"title": "Example Title 5", "url": "https://example.com/article5", "date": "2024-05-16", "content": "Example content 5..."},
    {"title": "Example Title 6", "url": "https://example.com/article6", "date": "2024-05-16", "content": "Example content 6..."}
]
daily_secu = [
    {"title": "Example Title 7", "url": "https://example.com/article7", "date": "2024-05-16", "tag": "Phishing", "content": "Example content 7..."},
    {"title": "Example Title 8", "url": "https://example.com/article8", "date": "2024-05-16", "tag": "APT", "content": "Example content 8..."}
]

# HTML 템플릿
html_template = '''
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 20px;
        }
        .container {
            width: 100%;
            max-width: 600px;
            margin: auto;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .section-title {
            font-size: 20px;
            font-weight: bold;
            margin-top: 20px;
            border-bottom: 2px solid #ccc;
            padding-bottom: 5px;
        }
        .article {
            border-bottom: 1px solid #ccc;
            padding-bottom: 10px;
            margin-bottom: 10px;
        }
        .title {
            font-size: 18px;
            font-weight: bold;
        }
        .url {
            color: #1a0dab;
        }
        .content {
            margin-top: 5px;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 12px;
            color: #888;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>오늘의 뉴스 요약</h2>
            <p>{{ date }}</p>
        </div>

        <div class="section-title">1. The Hacker News</div>
        {% for article in hacker_news %}
        <div class="article">
            <div class="title">{{ article.title }}</div>
            <div class="url"><a href="{{ article.url }}" target="_blank">{{ article.url }}</a></div>
            <div class="date">{{ article.date }}</div>
            <div class="tag">{{ article.tag }}</div>
            <div class="content">{{ article.content }}</div>
        </div>
        {% endfor %}

        <div class="section-title">2. Security Affairs</div>
        {% for article in security_affairs %}
        <div class="article">
            <div class="title">{{ article.title }}</div>
            <div class="url"><a href="{{ article.url }}" target="_blank">{{ article.url }}</a></div>
            <div class="date">{{ article.date }}</div>
            <div class="tag">{{ article.tag }}</div>
            <div class="content">{{ article.content }}</div>
        </div>
        {% endfor %}

        <div class="section-title">3. 보안뉴스</div>
        {% for article in boan_news %}
        <div class="article">
            <div class="title">{{ article.title }}</div>
            <div class="url"><a href="{{ article.url }}" target="_blank">{{ article.url }}</a></div>
            <div class="date">{{ article.date }}</div>
            <div class="content">{{ article.content }}</div>
        </div>
        {% endfor %}

        <div class="section-title">4. 데일리시큐</div>
        {% for article in daily_secu %}
        <div class="article">
            <div class="title">{{ article.title }}</div>
            <div class="url"><a href="{{ article.url }}" target="_blank">{{ article.url }}</a></div
'''