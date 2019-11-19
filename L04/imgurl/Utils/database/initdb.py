#!/user/bin/env python

# @project : flask-imgurl
# @author : kalifun
# @file : initdb.py
# @ide : PyCharm
# @time : 2019/11/19 10:51 下午

from flask_script import Command
from  imgurl.Config.setting import Setting
from imgurl.Models.model import db,User,Pictures,Role

class Init(Command):
    def run(self):
        # 将创建表和初始化字段
        db.create_all()
        role1 = Setting.ROLE1
        role2 = Setting.ROLE2
        role3 = Setting.ROLE3
        Role(r_name=role1).add()
        Role(r_name=role2).add()
        Role(r_name=role3).add()
        print("__________添加角色成功____________")
        username = Setting.USERNAME
        password = Setting.PASSWORD
        getrole = Role.getid(role1)
        roleid = getrole.r_id
        User(username=username,password=password,role_id=roleid).add()
        print("__________添加用户成功____________")
class Drop(Command):
    def run(self):
        # 清除数据库所以数据，包括表和字段
        db.drop_all()
        print("__________清除数据成功____________")