# 微信公众号文章自动分析系统 - 配置指南

## 系统架构

```
微信文章 → 转发到QQ邮箱 → GitHub Actions自动爬取 → Claude分析 → 结果保存到仓库
```

## 功能说明

1. **邮箱监听** - 每天早上4点（北京时间）自动检查QQ邮箱
2. **链接提取** - 从邮件中提取微信公众号文章链接
3. **内容爬取** - 自动爬取文章标题、作者、正文等
4. **智能分析** - 使用Claude分析文章内容，生成报告
5. **自动保存** - 将分析结果提交到GitHub仓库

## 配置步骤

### 第一步：获取QQ邮箱授权码

1. 登录QQ邮箱网页版 (https://mail.qq.com)
2. 点击【设置】→【账户】
3. 找到【POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务】
4. 开启【IMAP/SMTP服务】
5. 按照提示发送短信，获得**授权码**（16位字符）
6. **保存好这个授权码**，后面需要用到

### 第二步：配置GitHub Secrets

在GitHub仓库页面：

1. 进入 **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**，添加以下secrets：

#### 必需的Secrets：

| Secret名称 | 说明 | 示例 |
|-----------|------|------|
| `EMAIL_USER` | QQ邮箱地址 | `your_email@qq.com` |
| `EMAIL_PASS` | QQ邮箱授权码（不是密码！） | `abcdefghijklmnop` |
| `ANTHROPIC_API_KEY` | Claude API密钥 | `sk-ant-...` |

#### 可选的Secrets：

| Secret名称 | 说明 | 默认值 |
|-----------|------|--------|
| `ANTHROPIC_BASE_URL` | Claude API地址（国内中转可用） | `https://api.anthropic.com` |

### 第三步：如何转发微信文章到邮箱

#### 方法1：使用"文件传输助手"（推荐）

1. 在微信中打开公众号文章
2. 点击右上角 **...** 菜单
3. 选择【复制链接】
4. 将链接发送到【文件传输助手】
5. 在电脑微信打开，复制链接
6. 发送邮件到你的QQ邮箱（可以只发链接，不需要写主题）

#### 方法2：使用微信"收藏"功能

1. 在微信中打开公众号文章
2. 点击右上角 **...** → 选择【收藏】
3. 在【我】→【收藏】中找到该文章
4. 点击右上角 **...** → 选择【分享到邮箱】
5. 输入你的QQ邮箱地址并发送

#### 方法3：直接在电脑浏览器操作

1. 在电脑微信或浏览器中打开文章
2. 复制文章链接（格式：`https://mp.weixin.qq.com/s/...`）
3. 发送邮件到你的QQ邮箱

> **重要提示**：只要邮件中包含微信文章链接，系统就能自动识别和爬取！

### 第四步：测试运行

配置完成后，可以立即测试：

1. 转发1-2篇微信文章到你的QQ邮箱
2. 在GitHub仓库页面：**Actions** → 选择 **Claude Code 技术文章分析**
3. 点击 **Run workflow** → 选择 **main** 分支 → 点击 **Run workflow**
4. 等待几分钟，查看运行结果

### 第五步：查看分析结果

运行成功后，可以在以下位置查看结果：

1. **仓库文件** - 自动提交的分析报告：
   - `articles_analysis.md` - Claude生成的详细分析报告
   - `articles_summary.md` - 文章摘要汇总
   - `articles_content.json` - 爬取的原始文章数据
   - `articles_links.json` - 文章链接记录

2. **Actions Artifacts** - 可下载的完整结果包：
   - 进入 Actions 运行详情页
   - 在页面底部找到 **Artifacts**
   - 下载 `claude-results-xxx` 压缩包

## 定时任务说明

系统已配置为：
- **执行时间**：每天早上4点（北京时间）
- **cron表达式**：`0 20 * * *`（UTC 20:00）
- **自动运行**：无需手动触发

如需修改时间，编辑 `.github/workflows/kiro-automation.yml` 中的cron表达式。

## 常见问题

### Q1: 为什么邮箱连接失败？
- 确认已开启QQ邮箱的IMAP服务
- 检查 `EMAIL_PASS` 使用的是**授权码**，不是QQ密码
- 授权码中不要有空格

### Q2: 文章爬取失败怎么办？
- 微信可能会限制爬虫访问，这是正常现象
- 建议每次转发2-5篇文章，避免过于频繁
- 如果某篇文章爬取失败，系统会跳过继续处理其他文章

### Q3: 如何查看历史分析记录？
- 所有分析结果都会提交到仓库，可以查看提交历史
- 在 Actions 页面可以看到每次运行的详细日志
- Artifacts 保留30天，可以下载查看

### Q4: 可以分析多久之前的文章？
- 默认检查最近24小时内收到的邮件
- 如需修改，编辑 `scripts/email_fetcher.py` 中的 `timedelta(days=1)`

### Q5: Claude分析失败怎么办？
- 检查 `ANTHROPIC_API_KEY` 是否正确
- 确认API额度是否充足
- 查看Actions日志中的具体错误信息

## 文件说明

```
kiro-auto/
├── .github/workflows/
│   └── kiro-automation.yml      # GitHub Actions工作流配置
├── scripts/
│   ├── email_fetcher.py         # 邮箱监听和链接提取
│   └── article_scraper.py       # 文章内容爬取
├── articles_links.json          # 文章链接记录（自动生成）
├── articles_content.json        # 文章内容数据（自动生成）
├── articles_summary.md          # 文章摘要（自动生成）
└── articles_analysis.md         # Claude分析报告（自动生成）
```

## 进阶使用

### 自定义分析提示词

编辑 `.github/workflows/kiro-automation.yml` 中的 `analysis_prompt.txt` 部分，可以自定义Claude的分析方向。

### 添加其他邮箱支持

修改 `scripts/email_fetcher.py` 中的 `imap_server` 参数：
- Gmail: `imap.gmail.com`
- 网易邮箱: `imap.163.com`
- 新浪邮箱: `imap.sina.com`

### 扩展文章来源

可以修改 `extract_wechat_links` 函数的正则表达式，支持其他平台的文章链接。

## 支持与反馈

如有问题或建议，请在GitHub Issues中提出。

---

**享受自动化的文章分析吧！** 🚀
