#!/usr/bin/env python3
"""
微信公众号文章邮箱监听和提取工具
支持从QQ邮箱读取微信文章链接并保存
"""

import imaplib
import email
from email.header import decode_header
import re
import os
import json
from datetime import datetime, timedelta
import time

class WeChatArticleFetcher:
    def __init__(self, email_user, email_pass, imap_server="imap.qq.com"):
        self.email_user = email_user
        self.email_pass = email_pass
        self.imap_server = imap_server
        self.mail = None
        
    def connect(self):
        """连接到邮箱"""
        print(f"正在连接到 {self.imap_server}...")
        self.mail = imaplib.IMAP4_SSL(self.imap_server)
        self.mail.login(self.email_user, self.email_pass)
        print("✅ 邮箱连接成功")
        
    def disconnect(self):
        """断开邮箱连接"""
        if self.mail:
            self.mail.close()
            self.mail.logout()
            print("✅ 邮箱连接已关闭")
    
    def decode_str(self, s):
        """解码邮件头"""
        if s is None:
            return ""
        value, charset = decode_header(s)[0]
        if charset:
            try:
                value = value.decode(charset)
            except:
                value = value.decode('utf-8', errors='ignore')
        elif isinstance(value, bytes):
            value = value.decode('utf-8', errors='ignore')
        return str(value)
    
    def extract_wechat_links(self, text):
        """提取微信文章链接"""
        # 匹配微信公众号文章链接
        pattern = r'https?://mp\.weixin\.qq\.com/s[^\s<>"\']*'
        links = re.findall(pattern, text)
        # 去重
        return list(set(links))
    
    def get_email_body(self, msg):
        """获取邮件正文"""
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain" or content_type == "text/html":
                    try:
                        payload = part.get_payload(decode=True)
                        charset = part.get_content_charset() or 'utf-8'
                        body += payload.decode(charset, errors='ignore')
                    except:
                        pass
        else:
            try:
                payload = msg.get_payload(decode=True)
                charset = msg.get_content_charset() or 'utf-8'
                body = payload.decode(charset, errors='ignore')
            except:
                pass
        return body
    
    def fetch_articles_from_last_24h(self):
        """获取最近24小时的邮件中的微信文章链接"""
        try:
            self.connect()
            
            # 选择收件箱
            self.mail.select("INBOX")
            
            # 搜索最近24小时的邮件
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
            status, messages = self.mail.search(None, f'(SINCE {yesterday})')
            
            if status != "OK":
                print("❌ 无法搜索邮件")
                return []
            
            email_ids = messages[0].split()
            print(f"📧 找到 {len(email_ids)} 封最近24小时的邮件")
            
            all_articles = []
            
            for email_id in email_ids:
                status, msg_data = self.mail.fetch(email_id, "(RFC822)")
                
                if status != "OK":
                    continue
                
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        # 获取邮件信息
                        subject = self.decode_str(msg["Subject"])
                        from_ = self.decode_str(msg.get("From"))
                        date = msg.get("Date")
                        
                        # 获取邮件正文
                        body = self.get_email_body(msg)
                        
                        # 提取微信链接
                        links = self.extract_wechat_links(body)
                        
                        if links:
                            print(f"📎 在邮件 '{subject}' 中找到 {len(links)} 个微信文章链接")
                            
                            for link in links:
                                article = {
                                    "url": link,
                                    "email_subject": subject,
                                    "email_from": from_,
                                    "email_date": date,
                                    "fetched_at": datetime.now().isoformat()
                                }
                                all_articles.append(article)
            
            self.disconnect()
            return all_articles
            
        except Exception as e:
            print(f"❌ 获取邮件时出错: {e}")
            if self.mail:
                self.disconnect()
            return []
    
    def save_articles(self, articles, output_file="articles_links.json"):
        """保存文章链接到文件"""
        if not articles:
            print("ℹ️  没有找到新的文章链接")
            return
        
        # 读取已有的文章链接（如果存在）
        existing_articles = []
        if os.path.exists(output_file):
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    existing_articles = json.load(f)
            except:
                existing_articles = []
        
        # 合并并去重（基于URL）
        existing_urls = {a['url'] for a in existing_articles}
        new_articles = [a for a in articles if a['url'] not in existing_urls]
        
        if new_articles:
            all_articles = existing_articles + new_articles
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_articles, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 保存了 {len(new_articles)} 个新文章链接到 {output_file}")
            print(f"📊 总共 {len(all_articles)} 个文章链接")
            
            # 也保存一个简单的链接列表
            links_file = "articles_links.txt"
            with open(links_file, 'w', encoding='utf-8') as f:
                for article in all_articles:
                    f.write(f"{article['url']}\n")
            print(f"✅ 同时保存链接列表到 {links_file}")
        else:
            print("ℹ️  没有新的文章链接（全部已存在）")

def main():
    """主函数"""
    # 从环境变量读取配置
    email_user = os.environ.get("EMAIL_USER")
    email_pass = os.environ.get("EMAIL_PASS")
    
    if not email_user or not email_pass:
        print("❌ 错误: 请设置环境变量 EMAIL_USER 和 EMAIL_PASS")
        print("   EMAIL_USER: 你的QQ邮箱地址")
        print("   EMAIL_PASS: QQ邮箱授权码（不是密码）")
        return 1
    
    print("=" * 50)
    print("  微信公众号文章链接提取工具")
    print("=" * 50)
    print(f"📧 邮箱: {email_user}")
    print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    fetcher = WeChatArticleFetcher(email_user, email_pass)
    
    # 获取文章链接
    articles = fetcher.fetch_articles_from_last_24h()
    
    # 保存文章链接
    fetcher.save_articles(articles)
    
    print("")
    print("=" * 50)
    print(f"✅ 任务完成")
    print(f"⏰ 结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    return 0

if __name__ == "__main__":
    exit(main())
