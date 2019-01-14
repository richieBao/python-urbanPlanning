class Config(object):
    pass

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DATABASE = 'laeval.db'
    SQLALCHEMY_DATABASE_URI="sqlite:///{}".format(DATABASE) #SQLite对应的URI。URI是类似于URL的字符串，包含了QLAlchemy建立连接所需要的所有信息。

    DEBUG=True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

'''
SQLite数据URI为：sqlite:///database.db
MySQL数据库URI为：mysql+pymysql://user:password@ip:port/db_name
'''