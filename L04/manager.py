#!/user/bin/env python

# @project : flask-imgurl
# @author : kalifun
# @file : manager.py
# @ide : PyCharm
# @time : 2019-11-15 17:00
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from imgurl.App.initapp import CreateApp
from imgurl.Models.model import db
from imgurl.Utils.database.initdb import Init,Drop


# 创建对象
imgurl = CreateApp()
manage = Manager(app=imgurl)
# 要使用flask_migrate，必须绑定app和db
migrate = Migrate(imgurl,db)
# 把MigrateCommand命令添加到manager中
manage.add_command("db",MigrateCommand)
manage.add_command("init",Init)
manage.add_command("drop",Drop)

if __name__ == '__main__':
    # 启动代码
    manage.run()