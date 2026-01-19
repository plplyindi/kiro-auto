# 待分析文章目录

将您需要分析的文章放在这个目录中。

## 文章格式

- 支持 Markdown (.md) 和纯文本 (.txt) 格式
- 文件命名建议：`article-001.md`, `article-002.md` 等
- 每次自动运行会分析最多 3 篇文章

## 处理流程

1. **每小时自动运行**：GitHub Actions 每小时执行一次
2. **选择文章**：自动选择前 3 篇未处理的文章
3. **AI 分析**：Claude Code 分析文章内容
4. **保存结果**：分析结果保存到 `results/` 目录
5. **归档文章**：已分析的文章移动到 `analyzed/` 目录

## 添加文章

### 方法 1：通过 Git 添加

```bash
cd ~/kiro-auto
# 复制文章到 articles 目录
cp /path/to/your/article.md articles/

# 提交并推送
git add articles/
git commit -m "Add new articles for analysis"
git push
```

### 方法 2：通过 GitHub 网页上传

1. 访问 https://github.com/plplyindi/kiro-auto/tree/main/articles
2. 点击 "Add file" → "Upload files"
3. 拖拽文章文件
4. 点击 "Commit changes"

## 查看分析结果

- 访问 https://github.com/plplyindi/kiro-auto/actions
- 下载最新的 Artifacts
- 或查看 `results/` 目录
