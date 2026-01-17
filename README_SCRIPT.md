# 拼小圈文案生成脚本使用说明

## 功能说明

这个脚本使用 Cursor Cloud Agent API，根据 `Today` 文件夹中的帽子图片自动生成适合拼小圈发布的文案。

## 前置要求

1. **Python 3.6+**
2. **安装依赖**：
   ```bash
   pip install requests
   ```
3. **Cursor API Key**：需要从 Cursor 获取 API 密钥

## 配置步骤

### 1. 设置环境变量

**macOS/Linux:**
```bash
export CURSOR_API_KEY='your-api-key-here'
```

**Windows (CMD):**
```cmd
set CURSOR_API_KEY=your-api-key-here
```

**Windows (PowerShell):**
```powershell
$env:CURSOR_API_KEY='your-api-key-here'
```

### 2. 可选配置

如果需要使用 Cursor Cloud Agent 的仓库功能，可以设置：

```bash
export CURSOR_REPO_URL='https://github.com/your-org/your-repo'
```

如果需要接收 webhook 通知：

```bash
export CURSOR_WEBHOOK_URL='https://your-webhook-url.com/callback'
export CURSOR_WEBHOOK_SECRET='your-webhook-secret'
```

## 使用方法

### 基本使用

1. 确保 `Today` 文件夹中有帽子图片（支持 .jpg, .png, .jpeg, .gif, .bmp, .webp）
2. 运行脚本：
   ```bash
   python generate_copy.py
   ```

### 运行示例

```bash
$ python generate_copy.py
============================================================
拼小圈文案生成工具
============================================================

1. 读取 Today 文件夹中的图片...
找到 5 张图片：
  ✓ 主图_02.jpg
  ✓ 主图_03.jpg
  ✓ 主图_04.jpg
  ✓ 主图_05.jpg
  ✓ 主图_06.jpg

2. 启动 Cursor Agent...
正在启动 Cursor Agent...
API URL: https://api.cursor.com/v0/agents
模型: claude-4-sonnet
✓ Agent 启动成功！
  Agent ID: agent_xxxxx

✓ 任务已提交！
```

## 提示词说明

脚本使用的提示词包含以下要求：

1. 不需要包含品牌信息，只需要纯帽子相关的描述
2. 不需要包含精确数值的描述（如 UPF50+ 等）
3. 内容需要与帽子类型强相关（棒球帽、遮阳帽、雷锋帽等各有特点）
4. 生成的文案保存在 Today 文件夹内

如需修改提示词，请编辑 `generate_copy.py` 中的 `PROMPT_TEXT` 变量。

## 注意事项

1. **API 密钥安全**：请妥善保管 API 密钥，不要将密钥提交到代码仓库
2. **图片格式**：支持常见图片格式，建议使用 JPG 格式以减小文件大小
3. **Agent 执行时间**：Agent 在后台处理，可能需要一些时间完成
4. **结果获取**：
   - 如果配置了仓库 URL，Agent 会在指定分支中生成文案
   - 如果配置了 webhook，会收到任务完成通知
   - 也可以使用 Agent ID 查询任务状态

## 故障排查

### 问题：提示 "请先设置环境变量 CURSOR_API_KEY"
- **解决**：确保已正确设置环境变量，可以使用 `echo $CURSOR_API_KEY` (macOS/Linux) 或 `echo %CURSOR_API_KEY%` (Windows) 检查

### 问题：提示 "Today 文件夹不存在"
- **解决**：确保脚本在项目根目录运行，且 `Today` 文件夹存在

### 问题：提示 "没有找到可用的图片"
- **解决**：确保 `Today` 文件夹中包含支持的图片格式文件

### 问题：Agent 启动失败
- **解决**：检查 API 密钥是否正确，网络连接是否正常，以及 API 配额是否充足

## 相关文档

- [Cursor Cloud Agent API 文档](https://cursor.com/cn/docs/cloud-agent/api/endpoints)
