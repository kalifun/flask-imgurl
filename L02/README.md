# flask-script

为了让程序更加清晰，我们不能把所以代码都往一个py里面写，所以我们需要把程序架构写好，才能让自己和别人更容易看懂你的代码，而不会把自己搞迷惑。

熟悉Django的同学是否还记得Django的启动命令呢? python manager.

## 我们为什么要使用它？

**Flask-Script是一个让你的命令行支持自定义命令的工具，它为Flask程序添加一个命令行解释器。可以让我们的程序从命令行直接执行相应的程序**。

什么程序需要用到呢，跟着我一起探讨，后面你就会看到它的用处了。

## 安装

```
pip install flask-script
```

## 重构程序

```
├── imgurl
│   ├── App
│   │   ├── __init__.py
│   │   └── initapp.py		//创建程序
│   └── Config
│       ├── __init__.py
│       └── setting.py			//程序设置
├── manager.py              //管理程序
```

setting.py

```python
class Setting:
    # 启动debug模式
    DEBUG = True
```

Initapp.py

```python
from flask import  Flask
from imgurl.Config.setting import Setting

def CreateApp():
    # 创建应用
    app = Flask(__name__)
    # app.config来自于self.make_config()
    # app.config.from_object(Setting)，其实就是对默认配置的修改和添加
    app.config.from_object(Setting)
    return app
 # 下面是config默认配置
  #: Default configuration parameters.
    default_config = ImmutableDict(
        {
            "ENV": None,
            "DEBUG": None,
            "TESTING": False,
            "PROPAGATE_EXCEPTIONS": None,
            "PRESERVE_CONTEXT_ON_EXCEPTION": None,
            "SECRET_KEY": None,
            "PERMANENT_SESSION_LIFETIME": timedelta(days=31),
            "USE_X_SENDFILE": False,
            "SERVER_NAME": None,
            "APPLICATION_ROOT": "/",
            "SESSION_COOKIE_NAME": "session",
            "SESSION_COOKIE_DOMAIN": None,
            "SESSION_COOKIE_PATH": None,
            "SESSION_COOKIE_HTTPONLY": True,
            "SESSION_COOKIE_SECURE": False,
            "SESSION_COOKIE_SAMESITE": None,
            "SESSION_REFRESH_EACH_REQUEST": True,
            "MAX_CONTENT_LENGTH": None,
            "SEND_FILE_MAX_AGE_DEFAULT": timedelta(hours=12),
            "TRAP_BAD_REQUEST_ERRORS": None,
            "TRAP_HTTP_EXCEPTIONS": False,
            "EXPLAIN_TEMPLATE_LOADING": False,
            "PREFERRED_URL_SCHEME": "http",
            "JSON_AS_ASCII": True,
            "JSON_SORT_KEYS": True,
            "JSONIFY_PRETTYPRINT_REGULAR": False,
            "JSONIFY_MIMETYPE": "application/json",
            "TEMPLATES_AUTO_RELOAD": None,
            "MAX_COOKIE_SIZE": 4093,
        }
```

manager.py

```python
from flask_script import Manager
from imgurl.App.initapp import CreateApp


# 创建对象
imgurl = CreateApp()
manage = Manager(app=imgurl)

if __name__ == '__main__':
    # 启动代码
    manage.run()
```

## 启动

```bash
 $ python manager.py 
usage: manager.py [-?] {shell,runserver} ...

positional arguments:
  {shell,runserver}
    shell            Runs a Python shell inside Flask application context.
    runserver        Runs the Flask development server i.e. app.run()

optional arguments:
  -?, --help         show this help message and exit

```

```bash
$ python manager.py runserver
 * Serving Flask app "imgurl.App.initapp" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 506-704-959
```

