#!/bin/bash
# 服务器运行脚本
python3 -m venv agora && source venv/bin/activate
pip install -r requirements.txt
python -m realtime_agent.main server