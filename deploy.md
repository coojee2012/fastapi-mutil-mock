拉去最新的代码

python3 -m venv .venv
cd .venv
source ./.venv/bin/activate
activate 
deactivate

安装依赖


sudo apt-get install libpq-dev mariadb
sudo apt-get install gcc
sudo apt-get install python3.8-dev
sudo apt install python3-wheel
sudo apt install python3.8-venv

pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r .\requirements.txt
python -m pip install PyMySQL --upgrade #如果跑不起来

初始化数据库 更新到最新版
cd backend
alembic upgrade head
cd ..
python3 init_data.py

主目录运行
nohup uvicorn --app-dir backend main:app --reload > log.txt 2>&1 &


4.nginx反代

 

nginx反代有很多文章介绍了 这里就不赘述了. 直接proxy到刚才在supervisord里面暴露的sock即可.

 

复制代码
server {
    listen 80;
    server_name wx.domain.com;

    location / {
        proxy_pass http://unix:/root/Envs/wx/gzh/wx.sock;
    }
}
复制代码
 

然后重新nginx就可以了

nginx -s reload


git reset HEAD .
git checkout .

sudo supervisorctl start guessr
sudo supervisorctl stop guessr
sudo supervisorctl restart guessr