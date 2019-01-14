from flask_script import Manager,Server
from lAEVAL import app,db
from flask_migrate import Migrate,MigrateCommand
from models import Imageseval,imagesinfodf  #导入数据模型

from imgPred_recognizer import predConfig
from imgPred_training import ERFTrainer


manager=Manager(app) #将app传给Manager对象，初始化Flask Script。

migrate=Migrate(app,db) #通过app对象和SQLAlchemy的实例初始化Migrate对象。

manager.add_command("server",Server()) #添加执行服务器的Server命令，可以在terminal中使用python manage.py server执行。
manager.add_command('db',MigrateCommand) #添加数据库迁移命令MigrateCommand，可以在terminal中使用python manage.py db执行。

@manager.shell
def make_shell_context():
    return dict(app=app,db=db,Imagesinfo=Imagesinfo,Imageseval=Imageseval) #打开命令行时，默认的导入工作，并返回在dict中。

if __name__=="__main__":
    manager.run()

'''
A:Flask扩展库Flask Script，可以创建命令，并在Flask的应用上下文(Applilcation Context)中执行，只有这样才能够对Flask对象进行修改。Flask Script自带一些默认命令，
可以运行服务器或者开启待应用上下文的Python命令行，
例如runserver(不附加参数则运行于http://127.0.0.1:5000/，如果指定参数例如python manage.py runserver -h 127.0.0.2 -p 206，则运行于http://127.0.0.2:206/),
shell(加载Flask应用上下文的交互式环境，通过shell，可以像启动应用一样操作动态数据，往shell里面增加一些默认的变量和函数。)
***通过在terminal终端中执行python manage.py *arg运行命令行十分必要，因为一些Flask扩展只有在Flask应用对象被创建后才能被初始化。直接运行默认的python命令行可能会令扩展返回错误。 
例如在terminal中运行
$python manage.py server  #运行app开发环境服务器
$python manage.py shell #在终端中打开使用命令行,使用quit()可退出命令行

(venv) D:\MUBENAcademy\pythonSystem\pycharm\LAevaluationA>python manage.py shell
>>> app #查看app有无正确导入
<Flask 'LAevaluationA'>

'''

'''
B:数据库迁移(flask_migrate库)：pip install Flask-Migrate
1.执行python manage.py db查看db命令列表
(venv) D:\MUBENAcademy\pythonSystem\pycharm\LAevaluationA>python manage.py db
usage: Perform database migrations

Perform database migrations

positional arguments:
  {init,revision,migrate,edit,merge,upgrade,downgrade,show,history,heads,branches,current,stamp}
    init                Creates a new migration repository 
    revision            Create a new revision file.
    migrate             Alias for 'revision --autogenerate'
    edit                Edit current revision.
    merge               Merge two revisions together. Creates a new migration file
    upgrade             Upgrade to a later version
    downgrade           Revert to a previous version
    show                Show the revision denoted by the given symbol.
    history             List changeset scripts in chronological order.
    heads               Show current available heads in the script directory
    branches            Show current branch points
    current             Display the current revision for each database.
    stamp               'stamp' the revision table with the given revision;
                        don't run any migrations

optional arguments:
  -?, --help            show this help message and exit
2.python manage.py db init #执行后会在项目目录中创建一个名为migrations文件夹，所有记录文件会保存在里面。
3.python manage.py db migrate -m"initial migration" #扫描SQLAlchemy对象，找到在此之前没有被记录过的所有表和列，由于第1此提交，所有迁移记录文件较大。确保
使用-m参数保存提交信息，通过提交信息寻找所需迁移记录版本。每个迁移记录文件都保存在migrations/versions文件夹中。
4.python manage.py db upgrade #把迁移记录应用到数据库，改变数据库结构，更新数据库。
5.python manage.py db history #根据history命令找到版本号，<base> -> 4053e22a6098 (head), initial migration。
6.python manage.py db downgrade versionNum(例如4053e22a6098) #根据找到的版本号，传入downgrade，回到以前的版本。
注：如果误删除migrations文件夹，执行数据库操作有可能提示"alembic.util.exc.CommandError: Can't locate revision identified by '4053e22a6098'"，此时，可以drop掉数据库中的
alembic_version表，再执行，就正常。

ubuntu服务器运行命令：python manage.py runserver --host 0.0.0.0 --port 9008
'''