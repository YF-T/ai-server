@app.route('/upload',methods=["GET","POST"])
def upload():
    '''
    功能：接收上传的模型，验证有效性，若有效，读取模型信息并存储模型，若无效，返回错误信息

    需要前端传入的参数：
    user：str 用户名
    password：str 密码
    modeltype：str 模型类别 pmml或onnx 全大写或全小写
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
    import os
    import getInfoFromModel
    #print("in")
    file = request.files.get('file')
    if file is None:  #接受失败
        #print("err file")
        return {
            'status': False,
            'errortype':"can't get model",
            'errorinfo':'file is None'
        }
    file_name = file.filename.replace(" ", "")
    #print("获取上传文件的名称为[%s]\n" % file_name)
    #保存文件
    file_path=os.path.dirname(__file__) + '/model/' + file_name
    file.save(os.path.dirname(__file__) + '/model/' + file_name)
    # 获取前端传入信息
    user = request.form['user']
    password = request.form['password']
    modeltype = request.form['modeltype']
    time = request.form['time']
    description = request.form['description']
    #检测模型有效性
    valid,err_info=getInfoFromModel.checkmodel("user",'password',modeltype,file_name)#先验证有效性再保存，这一步目前不验证用户密码
    if valid:#模型有效
        #从模型中读取信息
        dict=getInfoFromModel.getmodelinfo(file_name)
        #print(dict)
        #储存模型
        #需要把route改成文件名 第6项 filepath改
        modelname=file_name[0:-5]+'_'+modeltype
        save_status=database.savemodel(user, password, modelname,modeltype,time,modelname,description,
                           dict['engine'],dict['algorithm'],dict['input_variate'],dict['predict_variate'])
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
