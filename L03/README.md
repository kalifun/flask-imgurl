# Flask之数据库

我们在在里先不使用Jinja2模板，我们先用前后端分离的思想，我们把后台应用写好，在去考虑前端的事情。

在很多引用中，我们都无法避开使用数据库，但是想到那复杂的SQL语句就头皮发麻。我一直支持一句话“不会偷懒的程序员不是一个合格的程序员”。所以我是不愿意每次对数据库操作的时候还要写一堆SQL语句的，为了解决这个懊恼的问题，出现一个概念ORM。

## 什么是ORM？

即Object-Relationl Mapping，它的作用是在关系型数据库和对象之间作一个映射，这样，我们在具体的操作数据库的时候，就不需要再去和复杂的SQL语句打交道，只要像平时操作对象一样操作它就可以了 。

数据库操作问题是解决了，那我们数据库设计缺陷，需要重构数据库怎么办？数据需要迁移？这些问题都可能遇到，毕竟没有完美的程序。针对这个问题，Migrate将给我们带来更大的便利。

所以在接下来的程序中我们将引入`flask-SQLAlchemy`，`flask-migrate`

[Flask-migrate基本使用方法](https://www.cnblogs.com/sablier/p/11084080.html)

[SQLAlchemy技术手册](https://www.cnblogs.com/sablier/p/11829623.html)

请看对这两个概念进行了解后在进行下面操作。

## 数据库设计

![](images/1.png)

数据库设计的很简单，我们只需要三张表就可以了。后期为了实现Migrate功能，我将会重新构造数据库。所以前期我们先按照这个数据库来设计。

一对一(用户和角色)，一对多(用户和图片)

## 数据库模型

```
pip install flask-SQLAlchemy,pymysql
```

### SQLAlchemy配置

Setting.py

```python
class Setting:
    # 启动debug模式
    DEBUG = True
    # 连接数据库,mysql+pymysql(数据库类型+mysql驱动)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://account:passwd@127.0.0.1:3306/database'
    # SQLAlchemy将会记录所有发到标准输出(stderr)的语句
    SQLALCHEMY_ECHO = True
    # 数据库连接池的大小
    SQLALCHEMY_POOL_SIZE = 5
    # 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

Model.py

```python
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from imgurl.Utils.avatar.initavatar import get_pic
from werkzeug.security import generate_password_hash,check_password_hash

db = SQLAlchemy()

class User(db.Model):
    # 数据库中表的名称。这是SQLAlchemy所必需的；但是，如果模型定义了主键，则Flask - SQLAlchemy将自动设置它。如果显式设置了__table__或__tablename__，则将使用它。
    __tablename__ = "user"
    # 设置字段为id，类型为int类型，自动递增，并设置为主键
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    # 设置username字段，类型为string，并是唯一的。
    username = db.Column(db.String(64), unique=True)
    # 设置密码字段，类型为string
    pass_hash = db.Column(db.String(128))
    # 设置锁，当用户被锁时无法登录，类型为布尔类型，默认为false
    lock = db.Column(db.Boolean, default=False)
    # 设置当前用户的头像，我们这里写了一个自动生产头像的代码
    avatar = db.Column(db.String(128), default=get_pic())
    # 设置创建用户的时间，程序会根据用户创建时间填入
    crate = db.Column(db.DateTime, default=datetime.now)
    # 角色id，我们这里的角色是唯一，关联着role表的id，ForeignKey(外键)
    role_id = db.Column(db.Integer, db.ForeignKey('role.r_id'))

    # 可以理解表初始化必须要的字段
    def __init__(self,username,password):
        self.username = username
        self.generate_password(password)

    # 生成hash密码,用户注册后将进行hash处理再写入数据库
    def generate_password(self,password):
        self.pass_hash = generate_password_hash(password)

    # 居然密码变成了hash，那我们登录的时候不能让用户猜测自己hash密码
    def check_pass(self,password):
        # 通过用户输入的密码和数据库密码进行匹配，布尔类型
        return check_password_hash(self.pass_hash,password)

class Role(db.Model):
    __tablename__ = 'role'
    r_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    r_name = db.Column(db.String(64),unique=True)

    def __init__(self,r_name):
        self.r_name = r_name

class Pictures(db.Model):
    __tablename__ = 'pictures'
    image_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    # 图片名称，图片上传成功将会修改图片名称
    name = db.Column(db.String(128), unique=True)
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 图片上传后的路径，不建议加入这个字段，因为难免会修改域名
    url = db.Column(db.String(64), unique=True)
    # 图片路径，因为图片我们将会存储在本地
    path = db.Column(db.String(64))
    # 设置管理是否可见
    see = db.Column(db.Boolean, default=True)
    # 上传时的ip
    ip = db.Column(db.String(64))
    create = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, name, u_id, url, path):
        self.name = name
        self.u_id = u_id
        self.url = url
        self.path = path
```

Initavatar.py

```python
import random
import hashlib


def get_pic(size=256):
    styles = ['mm','identicon', 'monsterid', 'wavatar','retro']
    random_str = ''.join([chr(random.randint(0x0000, 0x9fbf)) for i in range(random.randint(1, 25))])

    m1 = hashlib.md5("{}".format(random_str).encode("utf-8")).hexdigest()
    url = 'http://www.gravatar.com/avatar/{}?s={}&d={}'.format(m1, size, random.choice(styles))
    return url
```

## 总结

我们需要将模型设置好，到后期我们需要对数据库操作就变得便利了。