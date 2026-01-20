# 快速开始指南

## 3分钟配置完成

### 1. 获取QQ邮箱授权码

访问 https://mail.qq.com → 设置 → 账户 → 开启IMAP服务 → 获取授权码

### 2. 配置GitHub Secrets

仓库Settings → Secrets and variables → Actions → 添加：

```
EMAIL_USER = 你的QQ邮箱
EMAIL_PASS = QQ邮箱授权码
ANTHROPIC_API_KEY = Claude API密钥
```

### 3. 转发微信文章测试

1. 打开任意微信公众号文章
2. 复制链接：`https://mp.weixin.qq.com/s/...`
3. 发邮件到你的QQ邮箱（只包含链接即可）

### 4. 手动触发测试

GitHub仓库 → Actions → "Claude Code 技术文章分析" → Run workflow

### 5. 查看结果

等待3-5分钟，查看：
- 仓库新增的 `articles_analysis.md` 文件
- Actions运行日志
- Artifacts下载包

## 日常使用

每天只需：
1. 看到好文章，复制链接发邮件到QQ邮箱
2. 第二天早上4点自动分析
3. 到仓库查看分析报告

就这么简单！

---

详细配置请查看 [SETUP.md](./SETUP.md)
