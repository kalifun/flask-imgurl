#!/user/bin/env python

# @project : flask-imgurl
# @author : kalifun
# @file : initapp.py
# @ide : PyCharm
# @time : 2019-11-15 17:02

from flask import  Flask
from imgurl.Models.model import db
from imgurl.Config.setting import Setting

def CreateApp():
    # 创建应用
    app = Flask(__name__)
    # app.config来自于self.make_config()
    # app.config.from_object(Setting)，其实就是对默认配置的修改和添加
    app.config.from_object(Setting)
    db.init_app(app)
    return app