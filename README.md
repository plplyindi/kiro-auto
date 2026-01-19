# Kiro Auto - 自动化任务调度器

每天自动运行 Kiro CLI 任务的 GitHub Actions 项目。

## 功能特点

- 每天下午 5:00（北京时间）自动运行
- 支持手动触发
- 失败自动重试（最多 5 次）
- 任务结果自动保存

## 快速开始

### 1. 在 GitHub 上创建仓库

1. 访问 [GitHub](https://github.com/new)
2. 创建名为 `kiro-auto` 的新仓库
3. 选择 Public 或 Private

### 2. 配置 GitHub Secrets

在仓库的 Settings → Secrets and variables → Actions 中添加：

- `KIRO_API_KEY` - 你的 Kiro API 密钥

获取 Kiro API Key：
```bash
kiro auth login
kiro auth token
```

### 3. 推送代码

```bash
cd kiro-auto
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/plplyindi/kiro-auto.git
git push -u origin main
```

### 4. 手动测试

1. 进入仓库的 Actions 标签页
2. 选择 "Kiro 自动化任务" 工作流
3. 点击 "Run workflow" 按钮
4. 查看运行日志

## 自定义任务

编辑 `.kiro/specs/tasks.md` 文件来定义你自己的任务：

```markdown
# 我的任务

## 任务 1: 描述
执行的具体步骤...

## 任务 2: 描述
执行的具体步骤...
```

## 运行时间

- 自动运行: 每天 17:00 (北京时间) / 09:00 (UTC)
- 手动运行: 随时在 Actions 页面触发

## 目录结构

```
kiro-auto/
├── .github/
│   └── workflows/
│       └── kiro-automation.yml  # GitHub Actions 工作流
├── .kiro/
│   └── specs/
│       └── tasks.md             # 任务定义文件
└── README.md                    # 说明文档
```

## 查看运行结果

1. 访问仓库的 Actions 标签页
2. 查看最近的运行记录
3. 点击查看详细日志
4. 下载任务生成的文件（Artifacts）

## 故障排除

### 任务执行失败

1. 检查 KIRO_API_KEY 是否正确配置
2. 查看 Actions 日志中的错误信息
3. 确认任务文件格式正确

### Kiro CLI 安装失败

- 检查网络连接
- 查看 Actions 日志中的安装步骤

## 许可

MIT License
