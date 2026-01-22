#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time

def scrape_article(url):
    """爬取微信文章内容"""
    print(f"\nFetching: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"  [ERROR] HTTP {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取标题
        title_tag = soup.find('h1', class_='rich_media_title') or soup.find('h2', class_='rich_media_title')
        title = title_tag.get_text().strip() if title_tag else "No Title"
        
        # 提取作者
        author_tag = soup.find('a', class_='rich_media_meta_link')
        author = author_tag.get_text().strip() if author_tag else "Unknown"
        
        # 提取正文
        content_tag = soup.find('div', id='js_content') or soup.find('div', class_='rich_media_content')
        if content_tag:
            # 移除script和style标签
            for tag in content_tag.find_all(['script', 'style']):
                tag.decompose()
            content = content_tag.get_text(separator='\n').strip()
        else:
            content = "Content not found"
        
        article_data = {
            'url': url,
            'title': title,
            'author': author,
            'content': content[:5000],  # 只保存前5000字符
            'scraped_at': datetime.now().isoformat()
        }
        
        print(f"  [OK] Title: {title}")
        print(f"  [OK] Author: {author}")
        print(f"  [OK] Content: {len(content)} chars")
        
        return article_data
        
    except Exception as e:
        print(f"  [ERROR] {e}")
        return None

def main():
    print("=" * 50)
    print("  WeChat Article Scraper")
    print("=" * 50)
    print()
    
    # 读取链接
    try:
        with open('test_links.txt', 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
    except:
        print("[ERROR] test_links.txt not found")
        return 1
    
    print(f"Found {len(urls)} URLs to scrape")
    
    articles = []
    for url in urls:
        article = scrape_article(url)
        if article:
            articles.append(article)
        time.sleep(2)  # 延迟2秒，避免被封
    
    print()
    print("=" * 50)
    print(f"[OK] Scraped {len(articles)}/{len(urls)} articles")
    print("=" * 50)
    
    # 保存结果
    if articles:
        output_file = f"articles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"[OK] Saved to {output_file}")
        
        # 也保存为Markdown
        md_file = output_file.replace('.json', '.md')
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("# 微信文章摘要\n\n")
            for i, article in enumerate(articles, 1):
                f.write(f"## {i}. {article['title']}\n\n")
                f.write(f"**作者**: {article['author']}\n\n")
                f.write(f"**链接**: {article['url']}\n\n")
                f.write(f"**内容**:\n\n{article['content'][:1000]}\n\n")
                f.write("---\n\n")
        print(f"[OK] Also saved as {md_file}")
    
    return 0

if __name__ == "__main__":
    exit(main())
