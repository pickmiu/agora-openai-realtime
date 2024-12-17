#!/bin/bash
# 服务器运行脚本 废弃:这个python环境太难配置了，以后还是使用docker!
python3 -m venv agora && source venv/bin/activate
pip install -r requirements.txt
python -m realtime_agent.main server