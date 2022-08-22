import threading

import database

from flask import Flask, jsonify, request
from flask_cors import CORS

from myThread import MyThread
from threading import Thread
# 以上两行是否并不使用？能否删除？
import pickle

from pypmml import Model
import onnxruntime as ort

import json
import os

import prepare

import getInfoFromModel

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

@app.route('/upload',methods=["GET","POST"])
def upload():
    '''
    功能：接收上传的模型，验证有效性，若有效，读取模型信息并存储模型，若无效，返回错误信息

    需要前端传入的参数：
    user：str 用户名
    password：str 密码
    modeltype：str 模型类别 pmml或onnx 全大写或全小写
    modelname:str 用户输入的模型名称
    file：模型文件 pmml或onnx
    time：str 创建时间
    description： str 模型描述

    Returns:
        'status':bool 表示从接收模型，验证有效性，读取信息到将其存在数据库中整个过程是否成功，成功为True，否则为False

        'errortype':str 表示出错的步骤 若status为True为空字符串
                    ’can't get model‘接收不到模型，file为None
                    ’model is invalid‘ 模型无效
                    ’can't save model‘ 将模型存入数据库过程出错，具体错误见errinfo

        'errorinfo':str 若status为False，返回错误具体的错误信息，若status为True为空字符串
                    例如：若模型无效，返回具体无效原因，如："model is invalid:can't get version"
                        若将模型存入数据库过程出错，返回具体出错原因，如:'user not found' : 用户不存在
                                                                'invalid password' : 密码错误
                                                                'duplication' : 部署名重复
    '''
    #print("in")
    print(type(request.files.get('file')))
    file = request.files.get('file')
    if file is None:  #接受失败
        #print("err file")
        return {
            'status': False,
            'errortype':"can't get model",
            'errorinfo':'file is None'
        }
    # 获取前端传入信息
    user = request.form['user']
    password = request.form['password']
    modelname = request.form['modelname']
    modeltype = request.form['modeltype']
    time = request.form['time']
    description = request.form['description']
    #print("获取上传文件的名称为[%s]\n" % file_name)
    #保存文件
    file_name = user + '_' + modelname + '_' + file.filename.replace(" ", "")
    file_path=os.path.dirname(__file__) + '/model/' + file_name
    file.save(os.path.dirname(__file__) + '/model/' + file_name)
    #检测模型有效性
    valid,err_info=getInfoFromModel.checkmodel("user",'password',modeltype,file_name)#先验证有效性再保存，这一步目前不验证用户密码
    if valid:#模型有效
        #从模型中读取信息
        dict=getInfoFromModel.getmodelinfo(file_name)
        #print(dict)
        #储存模型
        #需要把route改成文件名 第6项 filepath改
        '''print('user',user)
        print('password',password)
        print('modelname',modelname)
        print('modeltype',modeltype)
        print('time',time)
        print('file_path',file_path)
        print('description',description)
        print('dict',dict)'''
        save_status=database.savemodel(user, password, modelname,modeltype,time,file_name,description,
                           dict['engine'],dict['algorithm'],dict['input_variate'],dict['predict_variate'])
        #print('save_status',save_status)
        if save_status !='success':
            jsonify({'status': False,
                     'errortype': "can't save model",
                     'errorinfo': save_status})
    else:
        #模型不合法
        return jsonify({'status': False,
                        'errortype':'model is invalid',
                        'errorinfo': err_info})

    return jsonify({'status': True,
                    'errortype':'',
                    'errorinfo':''})


@app.route('/getusermodel',methods=["POST", "GET"])
def getusermodel():
    '''
    获取用户模型信息

    Parameters:
     user : str - 用户名
     password : str - 密码

    Returns:
     status : str - 'success' : 成功
                    'user not found' : 用户不存在
                    'invalid password' : 密码错误
     若成功才有以下属性：
     model : list - 一个包括所有该用户model的简略信息
                    每个元素为一个字典，属性包括
                    'modelname' : str - 模型名
                    'modeltype' : str - 模型类型
                    'time' : str - 模型日期

    Raises:
     本函数不应该报错
    '''
    # 解析数据包
    user = request.form['user']
    password = request.form['password']
    # 调用数据库访问函数获取信息
    status, answer = database.getusermodel(user, password)
    # 若报错则返回错误信息
    if not status:
        return jsonify({'status' : answer})
    # 转换answer变量的存储格式
    modeltitle = ['modelname', 'modeltype', 'time']
    answer = list(map(lambda x : dict(zip(modeltitle, x)), answer))
    # 返回值
    return jsonify({'status': 'success',
                    'model': answer})

@app.route('/deletemodel',methods=["DELETE", "POST"])
def deletemodel():
    '''
    删除模型

    Parameters:
     user : str - 用户名
     password : str - 密码
     modelname : str - 模型名

    Returns:
     status : str - 'success' : 成功
                    'user not found' : 用户不存在
                    'invalid password' : 密码错误
                    'model not found' : 找不到该名称模型

    Raises:
     本函数不应该报错
    '''
    # 解析数据包
    user = request.form['user']
    password = request.form['password']
    modelname = request.form['modelname']
    # 执行删除
    status = database.deletemodel(user, password, modelname)
    # 返回状态
    return jsonify({'status': status})

@app.route('/getmodeldeployment',methods=["GET", "POST"])
def getmodeldeployment():
    '''
    查看部署的服务

    Parameters:
     user : str - 用户名
     password : str - 密码
     modelname : str - 模型名

    Returns:
     status : str - 'success' : 设置成功
                    'user not found' : 用户不存在
                    'invalid password' : 密码错误
                    'model not found' : 找不到该名称模型
     若成功才有以下属性：
     deployment : list - 一个包括所有该模型部署的简略信息
                    每个元素为一个字典，属性包括
                    'deployment' : str - 部署名
                    'status' : str - 模型类型
                    'time' : str - 创建日期

    Raises:
     本函数不应该报错
    '''
    # 解析数据包
    user = request.form['user']
    password = request.form['password']
    modelname = request.form['modelname']
    # 调用数据库访问函数获取部署信息
    status, answer = database.getmodeldeployment(user, password, modelname)
    # 若报错则返回错误信息
    if not status:
        return jsonify({'status' : answer})
    # 转换answer变量的存储格式
    deploymenttitle = ['deployment', 'status', 'time']
    answer = list(map(lambda x : dict(zip(deploymenttitle, x)), answer))
    # 返回值
    return jsonify({'status' : 'success',
                    'deployment' : answer})

@app.route('/createdeployment',methods=["POST","GET"])
def createdeployment():
    '''
    启动部署的服务

    Parameters:
     user : str - 用户名
     password : str - 密码
     modelname : str - 模型名
     deployment : str - 部署名
     time : str - 部署时间

    Returns:
     status : str - 'success' : 设置成功
                    'user not found' : 用户不存在
                    'invalid password' : 密码错误
                    'duplication' : 部署名重复

    Raises:
     本函数不应该报错
    '''
    # 解析数据包
    user = request.form['user']
    password = request.form['password']
    modelname = request.form['modelname']
    deployment = request.form['deployment']
    time = request.form['time']
    # 创建部署
    status = database.createdeployment(user, password, modelname, deployment, time)
    # 返回成功/报错
    return jsonify({'status' : status})

@app.route('/setdeploymentstatusrunning',methods=["POST"])
def setdeploymentstatusrunning():
    '''
    启动部署的服务

    Parameters:
     user : str - 用户名
     password : str - 密码
     modelname : str - 模型名
     deployment : str - 部署名

    Returns:
     status : str - 'success' : 设置成功
                    'user not found' : 用户不存在
                    'invalid password' : 密码错误
                    'deployment not found' : 部署不存在

    Raises:
     本函数不应该报错
    '''
    # 解析数据包
    user = request.form['user']
    password = request.form['password']
    modelname = request.form['modelname']
    deployment = request.form['deployment']
    # 设置为暂停
    status = database.setdeploymentstatus(user, password, modelname, deployment, 'running')
    # 返回成功/报错
    return jsonify({'status' : status})

@app.route('/setdeploymentstatuspause',methods=["POST"])
def setdeploymentstatuspause():
    '''
    暂停部署的服务

    Parameters:
     user : str - 用户名
     password : str - 密码
     modelname : str - 模型名
     deployment : str - 部署名

    Returns:
     status : str - 'success' : 设置成功
                    'user not found' : 用户不存在
                    'invalid password' : 密码错误
                    'deployment not found' : 部署不存在

    Raises:
     本函数不应该报错
    '''
    # 解析数据包
    user = request.form['user']
    password = request.form['password']
    modelname = request.form['modelname']
    deployment = request.form['deployment']
    # 设置为暂停
    status = database.setdeploymentstatus(user, password, modelname, deployment, 'pause')
    # 返回成功/报错
    return jsonify({'status' : status})

@app.route('/fake_getmodelinfo',methods=['POST',"GET"])
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
                                'dimension' : '5*5', 
                                'optype' : None},
                               {'name' : 'input2',
                                'type' : 'int',
                                'range' : None,
                                'dimension' : None, 
                                'optype' : 'don\'t know'},],
                    'output' : [{'name' : 'output1',
                                 'type' : 'int',
                                 'range' : None,
                                 'dimension' : None, 
                                 'optype' : None},],})

@app.route('/getmodelinfo',methods=["POST","GET"])
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
                    'optype' : str - 测量
     output : list - 输出变量，格式同input

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
    variabletitle = ['name', 'type', 'range', 'dimension', 'optype']
    input = list(map(lambda x : dict(zip(variabletitle, x)), input))
    output = list(map(lambda x : dict(zip(variabletitle, x)), output))
    # 返回值
    infotitle = ['modelname', 'modeltype', 'time', 'algorithm', 'engine', 'description']
    answer = dict(zip(infotitle, info))
    answer['status'] = 'success'
    answer['input'] = input
    answer['output'] = output
    return jsonify(answer)

@app.route('/testmodel_test',methods=["POST"])
def testmodel_test():
    '''
    名称：测试模型
    功能：对应lxt说的模型测试
    Parameters:
     user : str - 用户名
     password : str - 密码
     modelname : str - 模型名称
     input : dict - 模型需要的变量
             或 str - 传输jpg的base64编码
             或 file - txt的文件
     filetype : str - 'none' : 正常输入
                      'jpgbase64' : 图片
                      'csv' : csv
                      'txt' : txt
                      'mp4base64'
                      'mp4'
                      'zip'
                或
                dict - 一个表示input的元素是否危文件的字典
                例如
                {'input1' : 'none', 'input2' : 'jpgbase64'}
                这时则可以从inputfile_input2中读取文件

    Returns:
     status : str - 'success' : 成功
                    'user not found' : 用户不存在
                    'invalid password' : 密码错误
                    'invalid input' : 输入不合法
                    'model not found' : 未找到模型
                    'runtime error' : 模型运行出错
                    
     若成功，返回：
     output : dict - 输出结果，格式服从前端要求
     '''
    
    user = request.form['user']
    password = request.form['password']
    modelname = request.form['modelname']
    if request.form['filetype'] in ('none', 'jpgbase64', 'csv', 'txt',
                                    'mp4base64', 'mp4', 'zip'):
        if request.form['filetype'] == 'none':
            input = json.loads(request.form['input'])
            print(input,request.form["input"])
        elif request.form['filetype'] == 'jpgbase64':
            input = prepare.prepare(None, request.form['input'], 'jpgbase64', None)
        else:
            print(type(request.files.get('input')))
            file = request.files.get('input')
            filepath = ('./inputfile/' + user + '_' + modelname 
                        + '_'file.filename.replace(" ", ""))
            file.save(filepath)
            input = prepare.prepare(None, file, request.form['filetype'], filepath, None)
    else:
        filetype = json.loads(request.form['filetype'])
        input = json.loads(request.form['input'])
        for variable in filetype:
            if filetype[variable] in ('jpgbase64', 'mp4base64'):
                input[variable] = prepare.prepare(None, input[variable],
                                                   filetype[variable], None, None)
    # 参考getmodelinfo函数，首先判断用户输入参数是否符合标准，不符合则返回报错
    # 获取用户输入变量的信息
    status, inputvariables, outputvariables = database.getmodelvariables(user, password, modelname)
    if not status:
        return jsonify({'status': inputvariables})
    # 检查input是否符合输入变量的要求
    for variable in inputvariables:
        # 若input中没有需要的变量
        if variable[0] not in input:
            return jsonify({'status': 'invalid input'})

    # 提取待测试模型地址，若地址不存在，则报错"model not found"；存储在str类型变量address中
    address = find_model(user, password, modelname)
    print(address)
    if address == 'model not found':
        return jsonify({'status': address})

    # 用传入参数训练模型，注意：pmml和onnx格式的训练代码不同，如果添加新格式需要再做处理
    # 本模块（快速返回）暂时不使用多线程
    output = naive_test_model(address, input)
    print(output)
    print(dict(output))
    if output is None:
        return jsonify({'status': 'runtime error'})
    return jsonify({'status': 'success', 
                    'output': output})

@app.route('/testmodel_quickresponse/<deployment>',methods=["POST", "GET"])
def testmodel_quickresponse(deployment: str):
    '''
    名称：快速返回预测结果
    功能：接受传入的模型设定参数，使用模型进行测试，并返回测试结果（不使用多线程）
    Parameters:
     file : dict - 模型需要的变量
             或 str - 传输jpg的base64编码
             或 file - txt的文件
     prepare_py : str - 用户函数

    Returns:
     status : str - 'success' : 成功
                    'prepare invalid' :用户自定义预处理
                    'user not found' : 用户不存在
                    'invalid password' : 密码错误
                    'model not found' : 找不到模型

     若成功，返回：
     output : dict - 输出结果，格式服从前端要求
     '''
    user, password, modelname = database.getdeployment(deployment)
    #从前端接收文件 具体代码需要修改
    file = request.form['file']
    #预处理，用户自定义，任务2测试模型不需要
    #从前端接收用户的python代码
    prepare_py = request.form['prepare_py'].replace('@@', '\n')
    f1 = open("user_prepare.py", 'w', encoding='UTF-8')
    f1.write(prepare_py)
    f1.close()
    # 参考getmodelinfo函数，首先判断用户输入参数是否符合标准，不符合则返回报错
    status1, input, output = database.getmodelvariables(user, password, modelname)
    status2, info = database.getmodelinfo(user, password, modelname)
    if not status1 or not status2:
        return jsonify({'status': info if not status2 else input})

    import user_prepare
    data = user_prepare.prepare(input,file)
    # 检验用户的模型 语法是否有问题 获得输入 data
    try:
        print('success1')
        import user_prepare
        print('success2')
        data = user_prepare.prepare(input,file)#待更新，目前input是模型的input标准，file是从前端读取的input数据
    except:
        return jsonify({'status': 'preprocess failed'})

    # 提取待测试模型地址，若地址不存在，则报错"model not found"；存储在str类型变量address中
    address = find_model(user, password, modelname)
    if address == 'model not found':
        return jsonify({'status': address})

    # 用传入参数训练模型，注意：pmml和onnx格式的训练代码不同，如果添加新格式需要再做处理
    output = naive_test_model(address, data)
    if output is None:
        return jsonify({'status': 'runtime error'})
    return jsonify({'status': 'success', 
                    'output': output})

@app.route('/testmodel_delayresponse/<deployment>',methods=["GET","POST"])
def testmodel_delayresponse(deployment: str):
    '''
    名称：等待返回预测结果
    功能、说明基本同testmodel_quickresponse，使用多线程
    '''
    user, password, modelname = database.getdeployment(deployment)
    # 从前端接收文件 具体代码需要修改
    file = request.files.get('file')
    if file is None:
        file = request.form['file']
    # 从前端接收用户的python代码 #伪
    prepare_py = request.form['prepare_py']
    f1 = open("user_prepare.py", 'w', encoding='UTF-8')
    f1.write(prepare_py)
    f1.close()
    # 判断输入参数是否合法，此处的input不等于待使用的input
    status1, input, output = database.getmodelvariables(user, password, modelname)
    status2, info = database.getmodelinfo(user, password, modelname)
    if not status1 or not status2:
        return jsonify({'status': info if not status2 else input})

    # 检验用户的模型 语法是否有问题 获得输入 data
    try:
        import user_prepare
        data = user_prepare.prepare(input, file)  # 待更新，目前input是模型的input标准，file是从前端读取的input数据
    except:
        return jsonify({'status': 'preprocess failed'})

    # 提取待测试模型地址
    address = find_model(user, password, modelname)
    if address == 'model not found':
        return jsonify({'status': address})

    # 多线程
    #创建id
    state, id = database.createtask()
    if state == False:
        return jsonify({'status': id})
    task=threading.Thread(target=multithread_delayresponse,args=(address, input, user, password, id, data))
    task.start()
    #成功建立新线程
    return jsonify({'status': 'success'})

@app.route('/get_result_delayresponse/<deployment>/<taskid>',methods=["GET", "POST"])
def get_result(deployment: str, taskid:str):
    '''
    功能：查询等待返回的结果
    Args:
        user: 用户名
        password: 密码
        taskid: 任务id

    Returns:
        status：str 成功为success，失败为错误信息
        output： 成功为返回结果，失败为None
        file: 成功为pkl文件，失败为None
    '''
    user, password, modelname = database.getdeployment(deployment)
    #调用database查询任务id对应的文件
    #path具体是啥。。（应该是taskfile的存储路径，可以直接使用）
    state, path = database.gettaskfile(user, password, taskid)
    #目前用一个list储存所有的output
    if state == False:
        return jsonify({'status': path,
                        'output': None,
                        'file': None})
    else:
        f_read = open(path, 'rb')
        output=[]
        while True:
            try:
                res = pickle.load(f_read)
                output.append(res)
            except:
                break
        f_read.close()
        return jsonify({'status':"success",
                        'output':output,
                        'file':None})

def multithread_delayresponse(address: str, input: dict, user: str, password: str, id: str,data):
    '''
    功能：多线程执行等待返回 将返回的结果的文件路径和对应id储存在database
    Args:
        address:
        input: 输入格式应统一为dataframe（需要pandas）
        user: 用户
        password: 密码
        id: 任务id

    Returns:
    '''
    suffix = address[-4:]
    file_path='./output/'+id+'.pkl'
    if suffix == 'pmml':  # 模型为pmml格式
        model = Model.fromFile(address)
        output = model.predict(input)
        # pmml模型下dataframe的输出结果仍为dataframe
        # 储存output为文件 先用pickle，不行再改
        f_save = open(file_path, 'ab')
        pickle.dump(output, f_save)
        f_save.close()
        # 将id和对应文件储存到数据库
        database.settaskfile(user,password,id,file_path)
        #return output
    elif suffix == 'onnx':  # 模型为onnx格式
        sess = ort.InferenceSession(address)  # 加载模型
        for input in data:
            output = sess.run(None, input)
            # 储存output为文件 先用pickle，不行再改
            f_save = open(file_path, 'ab')
            pickle.dump(output, f_save)
            f_save.close()
        # 将id和对应文件储存到数据库
        database.settaskfile(user, password, id, file_path)
        #return output
    else:
        pass


# 以下函数只适用于测试界面
def find_model(user: str, password: str, modelname: str):
    # 提取待测试模型地址，若地址不存在，则报错"model not found"；存储在str类型变量address中
    status3, address = database.getmodelroute(user, password, modelname)
    if not status3:
        return address
    address = './model/' + address
    return address

def naive_test_model(address: str, input: dict):  # 最基础形式，只适用于测试界面快速返回
    suffix = address[-4:]
    # 模型为pmml
    if suffix == 'pmml':
        model = Model.fromFile(address)
        output = model.predict(input)
        if not output is None:
            output = dict(output)
        return output
    # 模型为onnx
    elif suffix == 'onnx':
        sess = ort.InferenceSession(address)  # 加载模型
        output = sess.run(None, input)
        # 注意：run函数的第二个参数必须为dict或者list
        return output
    else:
        pass


if __name__ == '__main__':
    database.restart()
    app.run(debug = True)