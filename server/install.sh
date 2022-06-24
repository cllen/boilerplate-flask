#! /bin/bash

# 决定使用的数据库：
# supervisor只会维护production,development两个环境。
source config.conf
export APP_CONFIG=$config_name

# 安装virtualenv、创建venv、安装requirements.txt
pip3 install virtualenv			# 安装python的虚拟环境

virtualenv -p python3 venv/ 			# 创建boilerplate-flask的python虚拟环境
source venv/bin/activate	# 为boilerplate-flask的python虚拟环境安装依赖
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
deactivate

# 安装supervisor、复制配置环境（注意配置里的文件夹路径要对的上！）
sudo apt-get install supervisor -y		# 安装supervisor
sudo cp supervisor.conf /etc/supervisor/conf.d/boilerplate-flask.conf

# 部署数据库:boilerplate-flask
source venv/bin/activate
# cd server/
export FLASK_APP=manage.py
sudo chmod 777 ./*
flask deploy
cd ../../
deactivate

sudo supervisorctl reload
