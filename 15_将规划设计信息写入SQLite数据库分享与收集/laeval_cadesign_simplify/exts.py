#将SQLAlchemy()实例化单独放置于一个.py文件中，避免在主文件LAevaluationA.py和数据模型models.py文件中互相调用，产生错误
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()