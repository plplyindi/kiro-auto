# Kiro Auto - Claude Code 自动化任务调度器

使用 Claude Code CLI 每天自动执行任务的 GitHub Actions 项目。

## 功能特点

- ⏰ 每天下午 5:00（北京时间）自动运行
- 🤖 使用 Claude Code CLI 执行任务
- 🔄 失败自动重试（最多 3 次）
- 📦 任务结果自动保存
- 🔧 支持手动触发

## 快速开始

### 1. Fork 或 Clone 本仓库

```bash
git clone https://github.com/plplyindi/kiro-auto.git
cd kiro-auto
```

### 2. 配置 GitHub Secret

在仓库的 **Settings → Secrets and variables → Actions** 中添加：

**必需的 Secret：**
- **Name**: `ANTHROPIC_API_KEY`
- **Value**: 您的 Anthropic API 密钥

**获取 API Key：**
1. 访问 https://console.anthropic.com/settings/keys
2. 创建新的 API Key
3. 复制并保存到 GitHub Secrets

### 3. 自定义任务

编辑 `.kiro/specs/tasks.md` 文件来定义您的任务：

```markdown
# 我的每日任务

请帮我完成以下任务：

## 任务 1: 生成每日报告
创建一个名为 daily-report.txt 的文件，包含当前日期和时间。

## 任务 2: 系统检查
检查系统环境信息并保存到 system-info.txt。
```

### 4. 测试运行

**手动触发测试：**
1. 进入仓库的 **Actions** 标签页
2. 选择 "Claude Code 自动化任务" 工作流
3. 点击 **"Run workflow"** 按钮
4. 查看运行日志

**或使用 GitHub CLI：**
```bash
gh workflow run "Claude Code 自动化任务"
gh run watch
```

## 运行时间

- **自动运行**: 每天 17:00 (北京时间) / 09:00 (UTC)
- **手动运行**: 随时在 Actions 页面触发

## 项目结构

```
kiro-auto/
├── .github/
│   └── workflows/
│       └── kiro-automation.yml    # GitHub Actions 工作流
├── .kiro/
│   └── specs/
│       └── tasks.md               # 任务定义文件
├── .gitignore
└── README.md
```

## 任务文件格式

`.kiro/specs/tasks.md` 使用 Markdown 格式，可以包含：

- 任务描述
- 代码要求
- 文件操作指令
- 任何您想让 Claude Code 完成的任务

**示例：**
```markdown
# 每日自动化任务

请执行以下任务：

1. 创建一个 daily-log.txt 文件
2. 在文件中写入当前日期和时间
3. 添加一条消息："Claude Code 自动任务执行成功"
```

## 查看运行结果

### 方法 1：Actions 日志
1. 访问仓库的 **Actions** 标签页
2. 查看最近的运行记录
3. 点击查看详细日志

### 方法 2：下载 Artifacts
1. 进入具体的运行记录
2. 滚动到底部的 **Artifacts** 部分
3. 下载 `claude-results-X` 压缩包
4. 查看生成的文件

## 高级配置

### 修改运行时间

编辑 `.github/workflows/kiro-automation.yml` 中的 cron 表达式：

```yaml
schedule:
  - cron: '0 9 * * *'  # UTC 09:00 = 北京时间 17:00
```

**常用时间：**
- `0 9 * * *` - 每天 17:00 北京时间（09:00 UTC）
- `0 1 * * *` - 每天 09:00 北京时间（01:00 UTC）
- `0 13 * * *` - 每天 21:00 北京时间（13:00 UTC）

### 修改重试次数

在工作流文件中修改：
```yaml
env:
  MAX_RETRIES: 3        # 重试次数
  RETRY_DELAY: 10       # 重试间隔（秒）
```

## 故障排除

### ❌ 任务执行失败

**检查清单：**
1. ✅ `ANTHROPIC_API_KEY` 是否正确配置
2. ✅ API Key 是否有效（未过期）
3. ✅ `.kiro/specs/tasks.md` 文件是否存在
4. ✅ 任务描述是否清晰明确
5. ✅ 查看 Actions 日志中的详细错误

### ❌ 认证失败

```
Error: Invalid API key
```

**解决方案：**
- 重新生成 API Key
- 确认已添加到 GitHub Secrets
- 检查 Secret 名称是否为 `ANTHROPIC_API_KEY`

### ❌ 安装失败

如果 Claude Code 安装失败，检查网络连接或更新安装脚本 URL。

## 安全注意事项

- ⚠️ **永远不要**将 API Key 直接写在代码中
- ✅ 始终使用 GitHub Secrets 存储敏感信息
- ✅ 定期轮换 API Key
- ✅ 设置 API Key 的使用限额

## 成本估算

Claude Code 使用 Anthropic API，会产生费用：
- 具体费用取决于任务复杂度和 token 使用量
- 建议在 Anthropic Console 设置使用限额
- 监控 API 使用情况

## 相关链接

- [Claude Code CLI 文档](https://docs.anthropic.com/claude-code)
- [Anthropic API 控制台](https://console.anthropic.com/)
- [GitHub Actions 文档](https://docs.github.com/actions)

## 许可

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
