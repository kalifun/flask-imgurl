
#!/user/bin/env python

# @project : flask-imgurl
# @author : kalifun
# @file : setting.py
# @ide : PyCharm
# @time : 2019-11-15 17:02

class Setting:
    # 启动debug模式
    DEBUG = True
    # 连接数据库,mysql+pymysql(数据库类型+mysql驱动)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:kali159.@127.0.0.1:3306/imgurl'
    # SQLAlchemy将会记录所有发到标准输出(stderr)的语句
    SQLALCHEMY_ECHO = True
    # 数据库连接池的大小
    SQLALCHEMY_POOL_SIZE = 5
    # 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
    SQLALCHEMY_TRACK_MODIFICATIONS = False
