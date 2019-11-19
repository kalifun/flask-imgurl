#!/user/bin/env python

# @project : flask-imgurl
# @author : kalifun
# @file : model.py
# @ide : PyCharm
# @time : 2019-11-15 19:00

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
    def __init__(self,username,password,role_id):
        self.username = username
        self.generate_password(password)
        self.role_id = role_id

    # 生成hash密码,用户注册后将进行hash处理再写入数据库
    def generate_password(self,password):
        self.pass_hash = generate_password_hash(password)

    # 居然密码变成了hash，那我们登录的时候不能让用户猜测自己hash密码
    def check_pass(self,password):
        # 通过用户输入的密码和数据库密码进行匹配，布尔类型
        return check_password_hash(self.pass_hash,password)

    # 插入数据并提交
    def add(self):
        db.session.add(self)
        db.session.commit()

class Role(db.Model):
    __tablename__ = 'role'
    r_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    r_name = db.Column(db.String(64),unique=True)

    def __init__(self,r_name):
        self.r_name = r_name

    # 插入数据并提交
    def add(self):
        db.session.add(self)
        db.session.commit()

    # 输入r_name，获取相关数据
    def getid(r_name):
        return Role.query.filter_by(r_name = r_name).first()

class Pictures(db.Model):
    __tablename__ = 'pictures'
    image_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    # 图片名称，图片上传成功将会修改图片名称
    name = db.Column(db.String(128), unique=True)
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 图片上传后的路径，不建议加入这个字段，因为难免会修改域名
    # url = db.Column(db.String(64), unique=True)
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

    # 插入数据并提交
    def add(self):
        db.session.add(self)
        db.session.commit()