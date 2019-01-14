'''
python manage.py runserver --host 0.0.0.0 --port 9008
uswgi:
uwsgi --http :9008 --modul manange.py --virtualenv /var/www/html/laevallab/vevn
uwsgi --http 127.0.0.1:9090 --wsgi-file manange.py --virtualenv /var/www/html/laevallab/vevn

uwsgi --http :5008  --ini laeval_uwsgi.ini -d ./uwsgi.log --pidfile=uwsgi.pid

uwsgi --ini laeval_uwsgi.ini

http://robot-x.top:9008/

uwsgi --http :5008  --ini laevapkill -f -9 uwsgil_uwsgi.ini

pkill -f -9 uwsgi

[uwsgi]
http = http = 0.0.0.0:9008
chdir  = /var/www/html/laevallab
wsgi-file  = manage.py
master=true
processes = 4
vacuum=true
daemonize = logs/uwsgi.log
home= /var/www/html/laevallab/vevn

python wsgi.py runserver --host 0.0.0.0 --port 9008

[uwsgi]
socket = 127.0.0.1:5000
processes = 4
threads = 2
master = true
pythonpath = /var/www/html/laevallab/lAEVAL
module = lAEVAL
callable = app
memory-report = true


[uwsgi]
http = 0.0.0.0:9008

processes = 4
threads = 2
master = true

chdir  = /var/www/html/laevallab
wsgi-file = manage.py

callable = app
daemonize = logs/uwsgi.log

#socket = 127.0.0.1:5000
#chmod-socket = 666

home= /var/www/html/laevallab/vevn


[uwsgi]
socket = 127.0.0.1:5000
processes = 4
threads = 2
master = true
pythonpath = /var/www/html/laevallab/lAEVAL
module = lAEVAL
callable = app
memory-report = true

home= /var/www/html/laevallab/vevn
daemonize = logs/uwsgi.log
http = 0.0.0.0:9008

virtualenv= /var/www/html/laevallab/vevn



[uwsgi]
chdir=/var/www/html/laevallab
module=manage.py
home= /var/www/html/laevallab/vevn

socket=/var/www/html/laevallab/laeval.sock
chmod-socket = 666




cd /etc/nginx/conf.d
cd /var/www/html/laevallab

upstream laeval{
server unix:///var/www/html/laevallab/laeval.sock;
}
server{
    listen 8080;
    server_name robot-x.top 101.37.34.8;
    charset utf-8;
    client_max_body_size 75M;
    location /static{
        alias /var/www/html/laevallab/static;
    }
    location /{
        uwsgi_pass laeval;
        include /var/www/html/laevallab/uwsgi_params;
    }

laeval_nginxConfig.conf



'''
'''
Ubuntu Server下启动/停止/重启MySQL数据库的三种方式
2013-05-03      0 个评论      
收藏     我要投稿
Ubuntu Server下启动/停止/重启MySQL数据库的三种方式
 
系统环境：ubuntu server 12.10 x64（mysql为系统自带）
 
当我们需要修改MySQL的配置文件my.cnf（windows 下为 my.ini）来进行一些设置的时候，修改完之后我们需要重启MySQL。
 
my.cnf文件位置为：/ect/mysql/my.cnf
 
Waring：如果该文件配置错误，MySQL将无法启动。
 
下面介绍三种方式对MySQL进行启动/停止/重启操作：
 
启动mysql：
方式一：sudo /etc/init.d/mysql start 
方式二：sudo start mysql
方式三：sudo service mysql start
 
停止mysql：
方式一：sudo /etc/init.d/mysql stop 
方式二：sudo stop mysql
方式san：sudo service mysql stop
 
重启mysql：
方式一：sudo/etc/init.d/mysql restart
方式二：sudo restart mysql
方式三：sudo service mysql restart
重启MySQL：fffsdfssudo
weirubo@weirubo-VirtualBox:~$ sudo service mysql restart
重启Apache：
weirubo@weirubo-VirtualBox:~$ sudo service apache2 restart



location /static/ {
        alias  /var/www/html/laevallab/static/;
        
    }
'''