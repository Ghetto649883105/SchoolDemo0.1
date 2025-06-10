TORTOISE_ORM = {
        "connections": {
            "default": {
                "engine": "tortoise.backends.mysql",
                "credentials": {
                    "host": "127.0.0.1",  # 数据库服务器ip
                    "port": "3306",  # 数据库服务器端口
                    "user": "root",  # 数据库用户名
                    "password": "264988",  # 数据库密码
                    "database": "data_demo0.1",  # 数据库名称必须和mysql一一对应
                    "minsize": 1,
                    "maxsize": 5,
                    "charset": "utf8mb4",
                    "echo": True
                }
            }
        },
        "apps": {
            "models": {
                "models": ["models",
                           "aerich.models"],  # 中括号内第一个为模型路径
                "default_connection": "default",
            }
        },
        "use_tz": False,
        "timezone": "Asia/Shanghai"
    }
