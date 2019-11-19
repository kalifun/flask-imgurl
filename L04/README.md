# flask-migrate数据迁移

在上一节我们已经讲过了数据库模型，在程序设计中，不断对程序更新迭代，我们加入的功能越来越多，数据模型随之修改，我们需要删除数据库重新加载，这样我们之前的数据就会丢失。根据这种场景，flask-migrate是一个不错之选，下面就来介绍它吧！

## 创建迁移仓库

```
pip install flask-migrate
```

初始化migrate

Manager.py

```
# 添加下面内容
# 要使用flask_migrate，必须绑定app和db
migrate = Migrate(imgurl,db)
# 把MigrateCommand命令添加到manager中
manage.add_command("db",MigrateCommand)
```

```bash
$ python manager.py 
usage: manager.py [-?] {db,shell,runserver} ...

positional arguments:
  {db,shell,runserver}
    db                  Perform database migrations
    shell               Runs a Python shell inside Flask application context.
    runserver           Runs the Flask development server i.e. app.run()

optional arguments:
  -?, --help            show this help message and exit

```

你可以发现manager中多了db这条命令。

```bash
$ python manager.py db init
  Creating directory /xxxx/flask-imgurl/migrations ...  done
  Creating directory /xxxx/flask-imgurl/migrations/versions ...  done
  Generating /xxxx/flask-imgurl/migrations/script.py.mako ...  done
  Generating /xxxx/flask-imgurl/migrations/env.py ...  done
  Generating /xxxx/flask-imgurl/migrations/README ...  done
  Generating /xxxx/flask-imgurl/migrations/alembic.ini ...  done
  Please edit configuration/connection/logging settings in '/xxxx/flask-imgurl/migrations/alembic.ini' before
  proceeding.

```

这时候你会发现应用程序目录多出了一个文件夹。下面是树结构。

```
migrations
├── README
├── alembic.ini
├── env.py
├── script.py.mako
└── versions
```

我们进行查看数据库，此时数据库没有发生任何变化。

## 初始化数据

我们模型已经完成，我们需要将模型初始化到数据库中。

Setting.py

```
# 初始化账号密码
    USERNAME = "admin"
    PASSWORD = "admin"
```

在model模型中添加方法，具体内容请[点击跳转](imgurl/Models/model.py)

```
    # 插入数据并提交
    def add(self):
        db.session.add(self)
        db.session.commit()
        # 输入r_name，获取相关数据
    def getid(r_name):
        return Role.query.filter_by(r_name = r_name).first()
```

Utils/database/initdb.py

```python
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
```

Manager.py

```
添加我们自定义的终端命令
manage.add_command("init",Init)
manage.add_command("drop",Drop)
```

```bash
$ python manager.py 
usage: manager.py [-?] {db,init,drop,shell,runserver} ...

positional arguments:
  {db,init,drop,shell,runserver}
    db                  Perform database migrations
    init
    drop
    shell               Runs a Python shell inside Flask application context.
    runserver           Runs the Flask development server i.e. app.run()

optional arguments:
  -?, --help            show this help message and exit

```

初始化数据库

```
python manager.py init
```

## 修改模型

Model.py

我们为了测试功能，我们只注释掉Pictures模型中的url字段。

我们先进数据库查看数据。

```
mysql> desc pictures;
+----------+--------------+------+-----+---------+----------------+
| Field    | Type         | Null | Key | Default | Extra          |
+----------+--------------+------+-----+---------+----------------+
| image_id | int(11)      | NO   | PRI | NULL    | auto_increment |
| name     | varchar(128) | YES  | UNI | NULL    |                |
| u_id     | int(11)      | YES  | MUL | NULL    |                |
| url      | varchar(64)  | YES  | UNI | NULL    |                |
| path     | varchar(64)  | YES  |     | NULL    |                |
| see      | tinyint(1)   | YES  |     | NULL    |                |
| ip       | varchar(64)  | YES  |     | NULL    |                |
| create   | datetime     | YES  |     | NULL    |                |
+----------+--------------+------+-----+---------+----------------+
```

注释行

```
# url = db.Column(db.String(64), unique=True)
```

## 创建迁移脚本

- 自动创建迁移脚本有两个函数
  - upgrade()：函数把迁移中的改动应用到数据库中。
  - downgrade()：函数则将改动删除。
- 自动创建的迁移脚本会根据模型定义和数据库当前状态的差异，生成upgrade()和downgrade()函数的内容。
- 对比不一定完全正确，有可能会遗漏一些细节，需要进行检查

```
$ python manager.py db migrate       
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected removed index 'url' on 'pictures'
INFO  [alembic.autogenerate.compare] Detected removed column 'pictures.url'
  Generating /xxxx/flask-imgurl/migrations/versions/d8099c148910_.py ...  done

```

可以看到已经检查到我们对模型进行了修改，子段位url。

## 更新数据库

```
$ python manager.py db upgrade
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> d8099c148910, empty message
```

```
mysql> desc pictures;
+----------+--------------+------+-----+---------+----------------+
| Field    | Type         | Null | Key | Default | Extra          |
+----------+--------------+------+-----+---------+----------------+
| image_id | int(11)      | NO   | PRI | NULL    | auto_increment |
| name     | varchar(128) | YES  | UNI | NULL    |                |
| u_id     | int(11)      | YES  | MUL | NULL    |                |
| path     | varchar(64)  | YES  |     | NULL    |                |
| see      | tinyint(1)   | YES  |     | NULL    |                |
| ip       | varchar(64)  | YES  |     | NULL    |                |
| create   | datetime     | YES  |     | NULL    |                |
+----------+--------------+------+-----+---------+----------------+
7 rows in set (0.00 sec)
```

你发现url数据成功删除了，我们也不需要重新初始化，这样可以确保程序快速上线。