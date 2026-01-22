#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import imaplib
import email
from email.header import decode_header
import re
import os
import json
from datetime import datetime, timedelta

def extract_wechat_links(text):
    """提取微信文章链接"""
    pattern = r'https?://mp\.weixin\.qq\.com/s[^\s<>"]*'
    links = re.findall(pattern, text)
    return list(set(links))

def main():
    email_user = os.getenv('EMAIL_USER', '974351861@qq.com')
    email_pass = os.getenv('EMAIL_PASS', 'lnazxegodphwbeie')
    
    print("=" * 50)
    print("  WeChat Article Fetcher")
    print("=" * 50)
    print(f"Email: {email_user}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 连接邮箱
    print("Connecting to imap.qq.com...")
    try:
        mail = imaplib.IMAP4_SSL("imap.qq.com")
        mail.login(email_user, email_pass)
        print("[OK] Connected successfully")
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return 1
    
    # 选择收件箱
    mail.select("INBOX")
    
    # 搜索最近24小时的邮件
    since_date = (datetime.now() - timedelta(hours=24)).strftime("%d-%b-%Y")
    _, message_ids = mail.search(None, f'(SINCE {since_date})')
    
    email_ids = message_ids[0].split()
    print(f"Found {len(email_ids)} emails in last 24 hours")
    print()
    
    all_links = []
    
    # 处理每封邮件
    for email_id in email_ids[-50:]:  # 只处理最近50封
        try:
            _, msg_data = mail.fetch(email_id, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            
            # 获取主题
            subject = ""
            if msg["Subject"]:
                decoded = decode_header(msg["Subject"])[0]
                if isinstance(decoded[0], bytes):
                    subject = decoded[0].decode(decoded[1] or 'utf-8', errors='ignore')
                else:
                    subject = decoded[0]
            
            # 获取发件人
            from_addr = msg.get("From", "")
            
            # 获取邮件内容
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body += part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    elif part.get_content_type() == "text/html":
                        body += part.get_payload(decode=True).decode('utf-8', errors='ignore')
            else:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            
            # 提取微信链接
            links = extract_wechat_links(body)
            
            if links:
                print(f"[FOUND] '{subject}' - {len(links)} links")
                for link in links:
                    all_links.append({
                        'url': link,
                        'subject': subject,
                        'from': from_addr,
                        'date': msg.get("Date", ""),
                        'fetched_at': datetime.now().isoformat()
                    })
        except Exception as e:
            print(f"[ERROR] Processing email: {e}")
            continue
    
    mail.close()
    mail.logout()
    print()
    print(f"[OK] Total {len(all_links)} links found")
    
    # 保存结果
    if all_links:
        with open('articles_links.json', 'w', encoding='utf-8') as f:
            json.dump(all_links, f, ensure_ascii=False, indent=2)
        
        with open('articles_links.txt', 'w', encoding='utf-8') as f:
            for item in all_links:
                f.write(f"{item['url']}\n")
        
        print(f"[OK] Saved to articles_links.json and articles_links.txt")
    
    print()
    print("=" * 50)
    print("[OK] Task completed")
    print("=" * 50)
    return 0

if __name__ == "__main__":
    exit(main())
