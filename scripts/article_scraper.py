#!/usr/bin/env python3
"""
微信公众号文章内容爬取工具
从文章链接爬取标题、作者、发布时间、正文内容等
"""

import requests
import re
import json
import os
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import time

class WeChatArticleScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_article(self, url):
        """爬取单篇文章"""
        try:
            print(f"🔍 正在爬取: {url[:80]}...")
            
            response = requests.get(url, headers=self.headers, timeout=30)
            response.encoding = 'utf-8'
            html = response.text
            
            # 提取文章信息
            article = {
                "url": url,
                "scraped_at": datetime.now().isoformat()
            }
            
            # 提取标题
            title_match = re.search(r'<h1[^>]*class="rich_media_title"[^>]*>(.*?)</h1>', html, re.DOTALL)
            if title_match:
                article["title"] = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
            else:
                # 尝试从meta标签提取
                title_match = re.search(r'var msg_title = "(.*?)";', html)
                if title_match:
                    article["title"] = title_match.group(1).strip()
            
            # 提取作者
            author_match = re.search(r'<span[^>]*class="rich_media_meta rich_media_meta_text"[^>]*>(.*?)</span>', html)
            if author_match:
                article["author"] = author_match.group(1).strip()
            else:
                # 尝试从JavaScript变量提取
                author_match = re.search(r'var nickname = "(.*?)";', html)
                if author_match:
                    article["author"] = author_match.group(1).strip()
            
            # 提取发布时间
            time_match = re.search(r'var publish_time = "(\d+)"', html)
            if time_match:
                timestamp = int(time_match.group(1))
                article["publish_time"] = datetime.fromtimestamp(timestamp).isoformat()
            
            # 提取正文内容
            content_match = re.search(r'<div[^>]*class="rich_media_content[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
            if content_match:
                content_html = content_match.group(1)
                # 移除所有HTML标签，保留文本
                content_text = re.sub(r'<[^>]+>', '', content_html)
                # 清理多余空白
                content_text = re.sub(r'\s+', ' ', content_text).strip()
                article["content"] = content_text[:5000]  # 保留前5000字符
                article["content_length"] = len(content_text)
            
            # 提取摘要
            digest_match = re.search(r'var msg_desc = "(.*?)";', html)
            if digest_match:
                article["digest"] = digest_match.group(1).strip()
            
            print(f"✅ 成功爬取: {article.get('title', 'Unknown Title')}")
            return article
            
        except Exception as e:
            print(f"❌ 爬取失败: {e}")
            return {
                "url": url,
                "error": str(e),
                "scraped_at": datetime.now().isoformat()
            }
    
    def scrape_from_links_file(self, links_file="articles_links.json", output_file="articles_content.json"):
        """从链接文件批量爬取文章"""
        if not os.path.exists(links_file):
            print(f"❌ 找不到文件: {links_file}")
            return []
        
        # 读取链接
        with open(links_file, 'r', encoding='utf-8') as f:
            links_data = json.load(f)
        
        print(f"📋 找到 {len(links_data)} 个文章链接")
        
        # 读取已爬取的文章（避免重复爬取）
        existing_articles = {}
        if os.path.exists(output_file):
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    articles = json.load(f)
                    existing_articles = {a['url']: a for a in articles}
                print(f"📚 已有 {len(existing_articles)} 篇文章")
            except:
                pass
        
        # 爬取新文章
        new_count = 0
        for link_data in links_data:
            url = link_data['url']
            
            # 跳过已爬取的文章
            if url in existing_articles:
                print(f"⏭️  跳过已爬取: {existing_articles[url].get('title', url[:50])}")
                continue
            
            # 爬取文章
            article = self.scrape_article(url)
            
            # 合并邮件来源信息
            article.update({
                "source_email": {
                    "subject": link_data.get("email_subject"),
                    "from": link_data.get("email_from"),
                    "date": link_data.get("email_date")
                }
            })
            
            existing_articles[url] = article
            new_count += 1
            
            # 避免请求过快
            time.sleep(2)
        
        # 保存所有文章
        all_articles = list(existing_articles.values())
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_articles, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 爬取完成！")
        print(f"   新增: {new_count} 篇")
        print(f"   总计: {len(all_articles)} 篇")
        print(f"   保存到: {output_file}")
        
        return all_articles

def main():
    """主函数"""
    print("=" * 50)
    print("  微信公众号文章内容爬取工具")
    print("=" * 50)
    print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    scraper = WeChatArticleScraper()
    articles = scraper.scrape_from_links_file()
    
    if articles:
        # 生成简单的Markdown摘要
        summary_file = "articles_summary.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("# 微信公众号文章汇总\n\n")
            f.write(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"总计: {len(articles)} 篇文章\n\n")
            f.write("---\n\n")
            
            for i, article in enumerate(articles, 1):
                f.write(f"## {i}. {article.get('title', '无标题')}\n\n")
                f.write(f"- **作者**: {article.get('author', '未知')}\n")
                if article.get('publish_time'):
                    f.write(f"- **发布时间**: {article['publish_time']}\n")
                if article.get('digest'):
                    f.write(f"- **摘要**: {article['digest']}\n")
                f.write(f"- **链接**: [查看原文]({article['url']})\n")
                if article.get('content_length'):
                    f.write(f"- **字数**: {article['content_length']} 字\n")
                f.write("\n")
                
                if article.get('content'):
                    preview = article['content'][:200]
                    f.write(f"**内容预览**:\n\n{preview}...\n\n")
                
                f.write("---\n\n")
        
        print(f"📝 生成文章摘要: {summary_file}")
    
    print("")
    print("=" * 50)
    print(f"✅ 任务完成")
    print(f"⏰ 结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    return 0

if __name__ == "__main__":
    exit(main())
