#!/user/bin/env python

# @project : flask-imgurl
# @author : kalifun
# @file : run.py
# @ide : PyCharm
# @time : 2019-11-15 09:41

# 引入flask
from flask import Flask

# app是Flask的实例，它接收包或者模块的名字作为参数，但一般都是传递__name__
app = Flask(__name__)

# 使用app.route装饰器会将URL和执行的视图函数的关系保存到app.url_map属性上。
@app.route("/",methods=['GET'])
def index():
    return "Hello world"

if __name__ == '__main__':
    # app.run启动服务。默认Flask只监localhost这个地址，端口为5000。
    app.run()