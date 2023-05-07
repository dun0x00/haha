from flask import Flask
from bus_index import index_api
from bus_putong import putong_api
from bus_teshu import teshu_api

# 创建应用程序
app = Flask(__name__)
app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1'

app.register_blueprint(index_api)
app.register_blueprint(putong_api)
app.register_blueprint(teshu_api)

if __name__ == '__main__':
    app.run(host="127.0.0.1",port=5000) # 启动Flask项目
