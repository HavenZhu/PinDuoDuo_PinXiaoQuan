#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拼小圈文案生成脚本
使用 Cursor Cloud Agent API 根据 Today 文件夹中的帽子图片自动生成文案
"""

import os
import sys
import requests
import base64
import json
from pathlib import Path

# 配置项 - 请根据实际情况修改
API_KEY = "key_ef18beee893c21bdfd156960d0f22f71bff317e5604a4a5912eca72b71906829" # 请先设置环境变量 CURSOR_API_KEY
API_BASE_URL = "https://api.cursor.com/v0/agents"

# 仓库配置（如果使用 Cursor Cloud Agent）
REPO_URL = "https://github.com/HavenZhu/PinDuoDuo_PinXiaoQuan"  # 可选：仓库地址
BASE_REF = "master"  # 基础分支
BRANCH_NAME = "feature/generate-copy"  # Agent 工作分支

# 模型配置
MODEL = "claude-4-sonnet"  # 或其他支持的模型

# 提示词
PROMPT_TEXT = """我是拼多多的商家，我想要发布拼小圈来吸引用户购买我的帽子，请根据Today文件夹中的帽子图片信息，帮我想一段适合拼小圈的文案
1. 不需要包含品牌信息，只需要纯帽子相关的描述即可
2. 不需要包含精确数值的描述，例如UPF50+等等
3. 内容需要与帽子强相关，比如棒球帽就是棒球帽的特点，遮阳帽、雷锋帽等也一样
4. 生成的文案放在Today文件夹内"""

# 项目路径
PROJECT_ROOT = Path(__file__).parent
TODAY_FOLDER = PROJECT_ROOT / "Today"
OUTPUT_FILE = TODAY_FOLDER / "拼小圈文案.txt"


def load_images_from_today():
    """
    读取 Today 文件夹中所有图片，返回 base64 编码的数据列表
    """
    images = []
    if not TODAY_FOLDER.exists():
        print(f"错误：Today 文件夹不存在 ({TODAY_FOLDER})")
        return images
    
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
    image_files = sorted([f for f in TODAY_FOLDER.iterdir() 
                         if f.suffix.lower() in image_extensions])
    
    if not image_files:
        print(f"警告：Today 文件夹中没有找到图片文件")
        return images
    
    print(f"找到 {len(image_files)} 张图片：")
    for img_file in image_files:
        try:
            with open(img_file, 'rb') as f:
                data = f.read()
            b64_data = base64.b64encode(data).decode('utf-8')
            
            # 尝试获取图片尺寸（简化处理，实际可能需要使用 PIL 等库）
            images.append({
                "data": b64_data,
                "dimension": {
                    "width": None,
                    "height": None
                }
            })
            print(f"  ✓ {img_file.name}")
        except Exception as e:
            print(f"  ✗ 读取图片失败 {img_file.name}: {e}")
    
    return images


def launch_cursor_agent(images):
    """
    调用 Cursor Cloud Agent API 启动 Agent
    """
    if not API_KEY:
        print("错误：请先设置环境变量 CURSOR_API_KEY")
        print("   macOS/Linux: export CURSOR_API_KEY='your-api-key'")
        print("   Windows: set CURSOR_API_KEY=your-api-key")
        return None
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 构建 prompt
    prompt = {
        "text": PROMPT_TEXT,
        "images": images
    }
    
    # 构建请求 payload
    payload = {
        "prompt": prompt,
        "model": MODEL,
        "target": {
            "autoCreatePr": False,
            "branchName": BRANCH_NAME
        }
    }
    
    # 如果有仓库配置，添加 source
    if REPO_URL:
        payload["source"] = {
            "repository": REPO_URL,
            "ref": BASE_REF
        }
    
    # Webhook 配置（可选）
    webhook_url = os.getenv('CURSOR_WEBHOOK_URL')
    webhook_secret = os.getenv('CURSOR_WEBHOOK_SECRET')
    if webhook_url and webhook_secret:
        payload["webhook"] = {
            "url": webhook_url,
            "secret": webhook_secret
        }
    
    print(f"\n正在启动 Cursor Agent...")
    print(f"API URL: {API_BASE_URL}")
    print(f"模型: {MODEL}")
    
    try:
        response = requests.post(API_BASE_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 201:
            data = response.json()
            agent_id = data.get("id")
            print(f"✓ Agent 启动成功！")
            print(f"  Agent ID: {agent_id}")
            return agent_id
        else:
            print(f"✗ Agent 启动失败")
            print(f"  状态码: {response.status_code}")
            print(f"  响应: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"✗ 请求失败: {e}")
        return None


def main():
    """
    主函数
    """
    print("=" * 60)
    print("拼小圈文案生成工具")
    print("=" * 60)
    
    # 读取图片
    print(f"\n1. 读取 Today 文件夹中的图片...")
    images = load_images_from_today()
    
    if not images:
        print("\n错误：没有找到可用的图片，无法生成文案")
        sys.exit(1)
    
    # 启动 Agent
    print(f"\n2. 启动 Cursor Agent...")
    agent_id = launch_cursor_agent(images)
    
    if agent_id:
        print(f"\n✓ 任务已提交！")
        print(f"\n注意：")
        print(f"  - Agent ID: {agent_id}")
        print(f"  - Agent 会在后台处理任务")
        print(f"  - 完成后，请检查仓库分支或等待 webhook 通知")
        print(f"  - 将生成的文案保存到: {OUTPUT_FILE}")
        print(f"\n如需查询 Agent 状态，可以使用 Agent ID 调用状态查询 API")
    else:
        print(f"\n✗ 任务提交失败，请检查配置后重试")
        sys.exit(1)


if __name__ == "__main__":
    main()
