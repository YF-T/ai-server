import database

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/register", methods=['POST'])
def register():
    '''
    注册接口

    Parameters:
     user : str - 用户名
     password : str - 密码

    Returns:
     status : str - 'success' : 成功
                    'duplication' : 用户重名

    Raises:
     本函数不应该报错
    '''
    user = request.form['user']
    password = request.form['password']

    status = database.register(user, password)

    return jsonify({'status':status})

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

@app.route('/getmodelinfo',methods=["GET"])
def getmodelinfo():
    '''
    获取用户模型信息

    Parameters:
     user : str - 用户名
     password : str - 密码
     modelname : str - 模型名称

    Returns:
     status : str - 'success' : 成功
                    'user not found' : 用户不存在
                    'invalid password' : 密码错误
     若成功才有以下属性：
     modelname : str - 模型名称
     time : str - 模型创建时间
     modeltype : str - 模型类型
     algorithm : str - 模型算法
     description : str - 模型描述
     engine : str - 模型引擎
     input : list - 输入变量，list里面的元素为一个字典，
                    'name' : str - 变量名
                    'type' : str - 变量类型
                    'range' : str - 变量取值范围
                    'dimension' : str - 变量维数
     output : list - 输出变量，格式同上

    Raises:
     本函数不应该报错
    '''
    # 解析数据包
    user = request.form['user']
    password = request.form['password']
    modelname = request.form['modelname']
    # 调用数据库访问函数获取信息
    status1, input, output = database.getmodelvariables(user, password, modelname)
    status2, info = database.getmodelinfo(user, password, modelname)
    # 若报错则返回错误信息
    if not status1 or not status2:
        return jsonify({'status' : info if not status2 else input})
    # 转换input,output变量的存储格式
    variabletitle = ['name', 'type', 'range', 'dimension']
    input = list(map(lambda x : dict(zip(variabletitle, x)), input))
    output = list(map(lambda x : dict(zip(variabletitle, x)), output))
    # 返回值
    infotitle = ['modelname', 'modeltype', 'time', 'algorithm', 'engine', 'description']
    answer = dict(zip(infotitle, info))
    answer['status'] = 'success'
    answer['input'] = input
    answer['output'] = output
    return jsonify(answer)

@app.route('/testmodel',methods=["GET"])
def testmodel():
    '''
    Parameters:
     user : str - 用户名
     password : str - 密码
     modelname : str - 模型名称
     input : dict - 输入变量
                    {'input1' : '1', 'input2' : '100.5'}

    Returns:
     status : str - 'success' : 成功
                    'user not found' : 用户不存在
                    'invalid password' : 密码错误
     若成功才有以下属性：
     output : dict - 输出变量，格式同上
     '''
    pass

if __name__ == '__main__':
    database.init()
    app.run(debug=True)