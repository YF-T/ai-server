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
                    'invalid password' : 密码错误
     
    Raises:
     本函数不应该报错
    '''
    user = request.form['user']
    password = request.form['password']
    
    status = database.identify(user, password)
        
    return jsonify({'status':status})

@app.route('/upload',methods=["POST"])
def upload():
    import os
    #待debug。。route也未和前端统一
    file = request.files.get('file')
    if file is None:  #接受失败
        return {
            'message': "文件上传失败"
        }
    file_name = file.filename.replace(" ", "")
    #print("获取上传文件的名称为[%s]\n" % file_name)
    #保存文件
    file.save(os.path.dirname(__file__) + '/model/' + file_name)
    #记录模型对应用户
    user = request.form['user']
    password = request.form['password']

    database.savemodel(user, password, file_name)

    return 'success'

@app.route('/fake_getmodelinfo',methods=["GET"])
def fake_getmodelinfo():
    user = request.form['user']
    password = request.form['password']
    modelname = request.form['modelname']
    return jsonify({'status' : 'success', 
                    'modelname' : 'test', 
                    'time' : '2022-08-10 16:00:00', 
                    'modeltype' : 'pmml', 
                    'algorithm' : 'randomforest', 
                    'description' : '测试用模型', 
                    'engine' : 'pypmml', 
                    'input' : [{'name' : 'input1', 
                                'type' : 'int', 
                                'range' : '0,1,2,3',
                                'dimension' : '5*5'},
                               {'name' : 'input2', 
                                'type' : 'int', 
                                'range' : None,
                                'dimension' : None},],
                    'output' : [{'name' : 'output1', 
                                 'type' : 'int', 
                                 'range' : None,
                                 'dimension' : None},],})

if __name__ == '__main__':
    database.init()
    app.run(debug=True)