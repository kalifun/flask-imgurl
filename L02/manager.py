#!/user/bin/env python

# @project : flask-imgurl
# @author : kalifun
# @file : manager.py
# @ide : PyCharm
# @time : 2019-11-15 17:00
from flask_script import Manager
from imgurl.App.initapp import CreateApp


# 创建对象
imgurl = CreateApp()
manage = Manager(app=imgurl)

if __name__ == '__main__':
    # 启动代码
    manage.run()