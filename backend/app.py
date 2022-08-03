import database

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})


@app.route("/login", methods=['POST'])
def login():
    '''
    登录接口
    TODO：之后可能会加一些用户权限系统
     
    Parameters:
     user : str - 用户名
     password : str - 密码
     
    Returns:
     status : str - 'success' : 成功
                    'user not found' : 用户不存在
                    'password error' : 密码错误
     
    Raises:
     本函数不应该报错
    '''
    user = request.form['user']
    password = request.form['password']
    
    status = database.identify(user, password)
        
    return jsonify({'status':status})

if __name__ == '__main__':
    database.init()
    app.run(debug=True)