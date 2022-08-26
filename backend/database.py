import sqlite3
import os

database = 'information.db'

def register(user : str, password : str):
    '''
    注册用户函数
     
    Parameters:
     uese - 用户名
     password - 密码
     
    Returns:
     'success' : 成功
     'duplication' : 用户重名
     
    Raises:
     若用户名或密码不是字符串则报错
    '''
    assert isinstance(user, str)
    assert isinstance(password, str)
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE user = ?', (user,))
    row = c.fetchone()
    if not row is None:
        status = 'duplication'
    else:
        c.execute('INSERT INTO users VALUES (?,?,?,?,?,?)', 
                        (user, password, 'user', 1, 1, 1))
        conn.commit()
        status = 'success'
    conn.close()
    return status


def identify(user : str, password : str):
    '''
    身份识别函数，识别用户是否存在/用户名与密码是否匹配
     
    Parameters:
     uese - 用户名
     password - 密码
     
    Returns:
     'success' : 成功
     'user not found' : 用户不存在
     'invalid password' : 密码错误
     
    Raises:
     若用户名或密码不是字符串则报错
    '''
    assert isinstance(user, str)
    assert isinstance(password, str)
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE user = ?', (user,))
    row = c.fetchone()
    if row is None:
        status = 'user not found'
    elif row[0] == password:
        status = 'success'
    else:
        status = 'invalid password'
    conn.close()
    return status


def getusermodel(user : str, password : str):
    '''
    返回用户的所有模型
     
    Parameters:
     uese - 用户名
     password - 密码
     
    Returns:
     多值返回
     第一个变量为一个布尔变量，False为访问失败，True为访问成功
     第二个变量：
     成功则为一个列表，这个列表包含该用户的每一个模型，每个模型的信息是一个三元组：(模型id，模型名称，类型，时间)
                                     如('test', 'pmml', '2022-08-04 19:00:00')
     失败则为一个字符串代表错误信息，'user not found' : 用户不存在
                                     'invalid password' : 密码错误
     
    Raises:
     本函数不应该报错
    '''
    if identify(user, password) != 'success':
        return False, identify(user, password)
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('SELECT modelname, modeltype, time FROM models WHERE user = ?', (user,))
    answer = c.fetchall()
    conn.close()
    return True, answer


def getmodelvariables(user : str, password : str, modelname : str):
    '''
    找到模型对应的输入变量和输出变量的信息
    Parameters:
     uese - 用户名
     password - 密码
     modelname - 模型名称，先假设非重复，之后再去重
    Returns:
     多值返回
     第一个变量为一个布尔变量，False为访问失败，True为访问成功
     若成功：
     第二个变量为一个list，里面装着所有的输入变量信息
        每个输入变量信息用一个元组(tuple)表示，元组里有四个str类型的元素，
        分别为
            字段名，
            类型，
            取值范围（若没有则为None），
            维数（没有则为None），
            测量（没有则为None）
        如('input', 'int', '0,1,2,3', '1*8', None)
        如('input', 'int', None, None, 'continuous')
     第三个变量为一个list，里面装着所有的输出变量信息，格式同input
     若失败：
     第二个变量返回报错信息，第三个变量返回None
        'model not found' : 找不到该名称模型
        'user not found' : 用户不存在
        'invalid password' : 密码错误 
    Raises:
     本函数不应该报错
    '''
    if identify(user, password) != 'success':
        return False, identify(user, password), None
    assert isinstance(modelname, str)
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('SELECT description FROM models WHERE user = ? AND modelname = ?', 
                    (user, modelname))
    if c.fetchone() is None:
        conn.close()
        return False, 'model not found', None
    c.execute('''SELECT name, type, value, dim, optype FROM variables 
                    WHERE user = ? AND modelname = ? AND inout = ?''', 
                    (user, modelname, 'input'))
    input = c.fetchall()
    c.execute('''SELECT name, type, value, dim, optype FROM variables 
                    WHERE user = ? AND modelname = ? AND inout = ?''', 
                    (user, modelname, 'output'))
    output = c.fetchall()
    conn.close()
    return True, input, output


def getmodelroute(user : str, password : str, modelname : str):
    '''
    找到模型对应的存储地址
    Parameters:
     uese - 用户名
     password - 密码
     modelname - 模型名称，先假设非重复，之后再去重
    Returns:
     多值返回
     第一个变量为一个布尔变量，False为访问失败，True为访问成功
     第二个变量为一个字符串
     成功则为路径名，一个字符串表示模型的路径，如'test.pmml'
     失败则为错误信息，'model not found' : 找不到该名称模型
                       'user not found' : 用户不存在
                       'invalid password' : 密码错误 
    Raises:
     本函数不应该报错
    '''
    if identify(user, password) != 'success':
        return False, identify(user, password)
    assert isinstance(modelname, str)
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('SELECT modelroute FROM models WHERE user = ? AND modelname = ?', 
                    (user, modelname))
    row = c.fetchone()
    if row is None:
        answer = 'model not found'
    else:
        answer = row[0]
    conn.close()
    return bool(row), answer


def getmodelinfo(user : str, password : str, modelname : str):
    '''
    找到模型对应的信息
     
    Parameters:
     uese - 用户名
     password - 密码
     modelname - 模型名称，先假设非重复，之后再去重
     
    Returns:
     多值返回
     第一个变量为一个布尔变量，False为访问失败，True为访问成功
     第二个变量为一个字符串
     成功则为模型信息，一个元组(modelname, modeltype, time, modelroute, 
                                algorithm, engine, description)
     失败则为错误信息，'model not found' : 找不到该名称模型
                       'user not found' : 用户不存在
                       'invalid password' : 密码错误 
     
    Raises:
     本函数不应该报错
    '''
    if identify(user, password) != 'success':
        return False, identify(user, password)
    assert isinstance(modelname, str)
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('''SELECT modelname, modeltype, time,  
                        algorithm, engine, description 
                        FROM models WHERE user = ? AND modelname = ?''', 
                            (user, modelname))
    row = c.fetchone()
    if row is None:
        answer = 'model not found'
    else:
        answer = row
    conn.close()
    return bool(row), answer


def savemodel(user : str, password : str, modelname : str, modeltype : str, 
                time : str, modelroute : str, description : str, 
                engine : str, algorithm : str, 
                input : list, output : list):
    '''
    存储模型信息
     
    Parameters:
     uese - 用户名
     password - 密码
     modelname - 模型名称
     modeltype - 模型类别
     time - 创建时间
     modelroute - 模型文件存储路径
     description - 模型描述
     engine - 引擎描述
     algorithm - 算法描述
     input - 输入变量信息的列表
        每个输入变量信息用一个元组(tuple)表示，元组里有四个str类型的元素，
        分别为字段名，类型，取值范围（若没有则为None），维数（没有则为None）
        如('input', 'int', '0,1,2,3', '1*8', None)
        如('input', 'int', None, None, 'continuous')
     output - 输出变量信息的列表，每个变量的信息格式同input
     
    Returns:
     'success' : 成功
     'duplication' : 重名，不合法
     'user not found' : 用户不存在
     'invalid password' : 密码错误
     
    Raises:
     参数类型错误
    '''
    # 验证用户名和密码
    if identify(user, password) != 'success':
        return identify(user, password)
    # 检验参数类型
    assert isinstance(modelname, str)
    assert isinstance(modeltype, str)
    assert isinstance(time, str)
    assert isinstance(modelroute, str)
    assert isinstance(description, str)
    assert isinstance(engine, str)
    assert isinstance(algorithm, str)
    assert isinstance(input, list)
    assert isinstance(output, list)
    for variable in input:
        assert isinstance(variable, tuple)
        for text in variable:
            assert isinstance(text, str) or text is None
    for variable in output:
        assert isinstance(variable, tuple)
        for text in variable:
            assert isinstance(text, str) or text is None
    # 链接数据库，检查是否有重名
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('SELECT description FROM models WHERE user = ? AND modelname = ?', 
                    (user, modelname))
    if not c.fetchone() is None:
        conn.close()
        return 'duplication'
    modelid = 0
    c.execute('INSERT INTO models VALUES (?,?,?,?,?,?,?,?,?)', 
                    (user, modelid, modelname, modeltype, 
                    time, modelroute, algorithm, engine, description))
    for variable in input:
        c.execute('INSERT INTO variables VALUES (?,?,?,?,?,?,?,?,?)', 
                    (user, modelid, modelname, 'input', 
                    variable[0], variable[1], variable[2], variable[3], variable[4]))
    for variable in output:
        c.execute('INSERT INTO variables VALUES (?,?,?,?,?,?,?,?,?)', 
                    (user, modelid, modelname, 'output', 
                    variable[0], variable[1], variable[2], variable[3], variable[4]))
    conn.commit()
    conn.close()
    return 'success'


def deletemodel(user : str, password : str, modelname : str):
    '''
    删除模型
     
    Parameters:
     uesr - 用户名
     password - 密码
     modelname - 模型名称
     
    Returns:
     'success' : 成功
     'user not found' : 用户不存在
     'invalid password' : 密码错误
     'model not found' : 找不到该名称模型
     
    Raises:
     参数类型错误
    '''
    # 验证用户名和密码
    if identify(user, password) != 'success':
        return identify(user, password)
    # 检验参数类型
    assert isinstance(modelname, str)
    # 检查模型是否存在
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('SELECT description FROM models WHERE user = ? AND modelname = ?', 
                    (user, modelname))
    if c.fetchone() is None:
        conn.close()
        return 'model not found'
    c.execute('DELETE FROM models WHERE user = ? AND modelname = ?', 
                    (user, modelname))
    c.execute('DELETE FROM variables WHERE user = ? AND modelname = ?', 
                    (user, modelname))
    c.execute('DELETE FROM delayresponsetasks WHERE user = ? AND modelname = ?', 
                    (user, modelname))
    c.execute('DELETE FROM deployments WHERE user = ? AND modelname = ?', 
                    (user, modelname))
    conn.commit()
    conn.close()
    return 'success'


def createtask(user : str, password : str, modelname : str, deployment : str):
    '''
    创建一个新的任务词条，返回任务id
     
    Parameters:
     uesr - 用户名
     password - 密码
     modelname - 模型名称
     
    Returns:
     多值返回
     第一个变量为一个布尔变量，False为访问失败，True为访问成功
     第二个变量为一个字符串
     成功则为模型id，例如'tyf_task_1'
     失败则为错误信息，'user not found' : 用户不存在
                       'invalid password' : 密码错误
     
    Raises:
     参数类型错误
    '''
    # 检验操作合法性
    if identify(user, password) != 'success':
        return False, identify(user, password)
    assert isinstance(modelname, str)
    # 连接数据库
    conn = sqlite3.connect(database)
    c = conn.cursor()
    # 得到数据库的
    c.execute('SELECT delayresponsetaskid FROM users WHERE user = ?', 
                    (user,))
    delayresponsetaskid = c.fetchone()[0]
    c.execute('UPDATE users SET delayresponsetaskid = ? WHERE user = ?', 
                    (delayresponsetaskid + 1, user))
    taskid = user + '_task_' + str(delayresponsetaskid)
    c.execute('INSERT INTO delayresponsetasks VALUES (?,?,?,?,?)', 
                    (user, taskid, modelname, deployment, 'None'))
    conn.commit()
    conn.close()
    return True, taskid


def deletetask(user : str, password : str, taskid : str):
    '''
    删除任务
     
    Parameters:
     uesr - 用户名
     password - 密码
     taskid - 任务id
     
    Returns:
     'success' : 设置成功
     'user not found' : 用户不存在
     'invalid password' : 密码错误
     'task not found' : 任务id不存在
     
    Raises:
     参数类型错误
    '''
    if identify(user, password) != 'success':
        return identify(user, password)
    assert isinstance(taskid, str)
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('SELECT user FROM delayresponsetasks WHERE user = ? AND id = ?', 
                    (user, taskid))
    row = c.fetchone()
    if row is None:
        answer = 'task not found'
    else:
        answer = 'success'
    c.execute('DELETE FROM delayresponsetasks WHERE user = ? AND id = ?', 
                    (user, taskid))
    conn.commit()
    conn.close()
    return answer


def gettaskfile(user: str, password: str, taskid: str):
    '''
    查看任务返回值储存路径
     
    Parameters:
     uesr - 用户名
     password - 密码
     taskid - 任务id
     
    Returns:
     多值返回
     第一个变量为一个布尔变量，False为访问失败，True为访问成功
     第二个变量为一个字符串
     成功则为路径名称
     失败则为错误信息，'user not found' : 用户不存在
                       'invalid password' : 密码错误
                       'task not found' : 任务id不存在
     
    Raises:
     参数类型错误
    '''
    if identify(user, password) != 'success':
        return False, identify(user, password)
    assert isinstance(taskid, str)
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('SELECT file FROM delayresponsetasks WHERE user = ? AND id = ?', 
                    (user, taskid))
    row = c.fetchone()
    if row is None:
        answer = 'model not found'
    else:
        answer = row[0]
    conn.close()
    return bool(row), answer


def settaskfile(user : str, password : str, taskid : str, file : str):
    '''
    设置任务存储路径
     
    Parameters:
     uesr - 用户名
     password - 密码
     taskid - 任务id
     file - 待设置的文件路径
     
    Returns:
     'success' : 设置成功
     'user not found' : 用户不存在
     'invalid password' : 密码错误
     'task not found' : 任务id不存在
     
    Raises:
     参数类型错误
    '''
    if identify(user, password) != 'success':
        return identify(user, password)
    assert isinstance(taskid, str)
    assert isinstance(file, str)
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('UPDATE delayresponsetasks SET file = ? WHERE user = ? AND id = ?', 
                    (file, user, taskid))
    c.execute('SELECT file FROM delayresponsetasks WHERE user = ? AND id = ?', 
                    (user, taskid))
    row = c.fetchone()
    if row is None:
        answer = 'task not found'
    else:
        answer = 'success'
    conn.commit()
    conn.close()
    return answer
    

def getdeployment(deployment : str):
    '''
    查询部署对应的用户名密码
     
    Parameters:
     deployment - 部署
     
    Returns:
     第一个值 - 'success' : 设置成功
                'deployment not found' : 用户不存在
     'invalid password' : 密码错误
     'task not found' : 任务id不存在
     
    Raises:
     参数类型错误
    '''
    assert isinstance(deployment, str)
    # 连接数据库
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('''SELECT user, modelname, status FROM deployments 
                    WHERE deployment = ?''' , 
                    (deployment, ))
    answer = c.fetchone()
    if not bool(answer):
        return 'deployment not found', None, None, None
    user, modelname, status = answer
    c.execute('''SELECT password FROM users
                    WHERE user = ?''' , 
                    (user, ))
    password = c.fetchone()[0]
    conn.close()
    if status == 'pause':
        return 'deployment pause', user, password, modelname
    return 'success', user, password, modelname


def createdeployment(user : str, password : str, modelname : str, 
                     deployment : str, time : str):
    '''
    创建一个新的部署
     
    Parameters:
     uesr - 用户名
     password - 密码
     modelname - 模型名称
     deployment - 部署名
     time - 创建时间
     
    Returns:
     'success' : 设置成功
     'user not found' : 用户不存在
     'invalid password' : 密码错误
     'duplication' : 部署名重复
     
    Raises:
     参数类型错误
    '''
    # 检验操作合法性
    if identify(user, password) != 'success':
        return identify(user, password)
    assert isinstance(modelname, str)
    assert isinstance(deployment, str)
    # 连接数据库
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('''SELECT time FROM deployments 
                    WHERE deployment = ?''' , 
                    (deployment, ))
    if not c.fetchone() is None:
        conn.close()
        return 'duplication'
    c.execute('INSERT INTO deployments VALUES (?,?,?,?,?,?,?,?,?,?,?)', 
                    (user, modelname, deployment, 'running', time,
                     0, 0.0, 0.0, 0.0, None, None))
    conn.commit()
    conn.close()
    return 'success'


def deletedeployment(user : str, password : str, deployment : str):
    '''
    删除部署
    Parameters:
     uesr - 用户名
     password - 密码
     deployment - 部署名
    Returns:
     'success' : 设置成功
     'user not found' : 用户不存在
     'invalid password' : 密码错误
     'deployment not found' : 任务id不存在
    Raises:
     参数类型错误
    '''
    if identify(user, password) != 'success':
        return identify(user, password)
    assert isinstance(deployment, str)
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('SELECT status FROM deployments WHERE deployment = ?', 
                    (deployment, ))
    row = c.fetchone()
    if row is None:
        answer = 'deployment not found'
    else:
        answer = 'success'
    c.execute('DELETE FROM deployments WHERE deployment = ?', 
                    (deployment, ))
    c.execute('DELETE FROM delayresponsetasks WHERE deployment = ?', 
                    (deployment, ))
    conn.commit()
    conn.close()
    return answer


def getdeploymenttask(deployment : str):
    '''
    返回部署的所有任务id
    Parameters:
     deployment - 部署名
    Returns:
     多值返回
     第一个变量为一个布尔变量，False为访问失败，True为访问成功
     第二个变量：
     成功则为一个列表，这个列表包含该用户的每一个taskid
     失败则为一个字符串代表错误信息，'deployment not found' : 部署不存在
    Raises:
     本函数不应该报错
    '''
    assert isinstance(deployment, str)
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('SELECT status FROM deployments WHERE deployment = ?', 
                    (deployment, ))
    row = c.fetchone()
    if row is None:
        conn.close()
        return False, 'deployment not found'
    c.execute('SELECT id FROM delayresponsetasks WHERE deployment = ?', (deployment,))
    answer = c.fetchall()
    answer = list(map(lambda x : x[0], answer))
    conn.close()
    return True, answer


def getdeploymentstatus(user : str, password : str, modelname : str, deployment : str):
    '''
    查看部署状态，启动/暂停
    Parameters:
     uesr - 用户名
     password - 密码
     modelname - 模型名称
     deployment - 部署名称
    Returns:
     多值返回
     第一个变量为一个布尔变量，False为访问失败，True为访问成功
     第二个变量为一个字符串
     成功则为模型状态，'running' : 正在运行
                       'pause' : 暂停
     失败则为错误信息，'user not found' : 用户不存在
                       'invalid password' : 密码错误
                       'deployment not found' : 任务id不存在
    Raises:
     参数类型错误
    '''
    if identify(user, password) != 'success':
        return False, identify(user, password)
    assert isinstance(modelname, str)
    assert isinstance(deployment, str)
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('''SELECT status FROM deployments 
                    WHERE user = ? AND modelname = ? AND deployment = ?''' , 
                    (user, modelname, deployment))
    row = c.fetchone()
    if row is None:
        answer = 'deployment not found'
    else:
        answer = row[0]
    conn.close()
    return bool(row), answer


def setdeploymentstatus(user : str, password : str, modelname : str,
                        deployment : str, status : str):
    '''
    设置部署状态为启动/暂停
    Parameters:
     uesr - 用户名
     password - 密码
     modelname - 模型名称
     deployment - 部署名称
     status - 待设置的任务状态，取值为'running', 'pause'
    Returns:
     'success' : 设置成功
     'user not found' : 用户不存在
     'invalid password' : 密码错误
     'deployment not found' : 任务id不存在
     'invalid status' : 状态不存在
    Raises:
     参数类型错误
    '''
    if identify(user, password) != 'success':
        return identify(user, password)
    assert isinstance(modelname, str)
    assert isinstance(deployment, str)
    if status not in ('running', 'pause'):
        return 'invalid status'
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('''UPDATE deployments SET status = ?
                    WHERE user = ? AND modelname = ? AND deployment = ?''' , 
                    (status, user, modelname, deployment))
    c.execute('''SELECT status FROM deployments 
                    WHERE user = ? AND modelname = ? AND deployment = ?''' , 
                    (user, modelname, deployment))
    row = c.fetchone()
    if row is None:
        answer = 'deployment not found'
    else:
        answer = 'success'
    conn.commit()
    conn.close()
    return answer


def getmodeldeployment(user : str, password : str, modelname : str):
    '''
    返回一个模型的所有部署
    Parameters:
     uesr - 用户名
     password - 密码
     modelname - 模型名称
    Returns:
     多值返回
     第一个变量为一个布尔变量，False为访问失败，True为访问成功
     若成功：
     第二个变量为一个list，里面装着所有的部署信息
        每个输入变量信息用一个元组(tuple)表示，元组里有四个str类型的元素，
        分别为
            部署名，
            部署状态（运行/暂停），
            部署时间
        如('deployment1', 'running', '2022-08-04 20:00:00')
     若失败：
     第二个变量返回报错信息
        'model not found' : 找不到该名称模型
        'user not found' : 用户不存在
        'invalid password' : 密码错误 
    Raises:
     参数类型错误
    '''
    if identify(user, password) != 'success':
        return False, identify(user, password)
    assert isinstance(modelname, str)
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('SELECT description FROM models WHERE user = ? AND modelname = ?', 
                    (user, modelname))
    if c.fetchone() is None:
        conn.close()
        return False, 'model not found'
    c.execute('''SELECT deployment, status, time FROM deployments
                    WHERE user = ? AND modelname = ?''', 
                    (user, modelname))
    deployments = c.fetchall()
    conn.close()
    return True, deployments


def setdeploymentperformance(deployment: str, times: int, averagecost: float, 
                             maxcost: float, mincost: float, 
                             firstvisit: str, lastvisit: str):
    '''
    写入部署性能     
    Parameters:
     deployment - 部署名称
     times - 执行次数
     averagecost - 平均响应时间
     maxcost - 最大响应时间
     mincost - 最小响应时间
     firstvisit - 最初访问时间点，初始值为None
     lastvisit - 最近访问时间点，初始值为None
    Returns:
     'success' : 设置成功
     'deployment not found' : 任务id不存在
    Raises:
     参数类型错误
    '''
    assert isinstance(deployment, str)
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('''UPDATE deployments SET times = ?, averagecost = ?,
                    maxcost = ?, mincost = ?, 
                    firstvisit = ?, lastvisit = ?
                    WHERE deployment = ?''' , 
                    (times, averagecost, maxcost, mincost, 
                     firstvisit, lastvisit, deployment))
    c.execute('''SELECT status FROM deployments 
                    WHERE deployment = ?''' , 
                    (deployment, ))
    row = c.fetchone()
    if row is None:
        answer = 'deployment not found'
    else:
        answer = 'success'
    conn.commit()
    conn.close()
    return answer
    

def getdeploymentperformance(deployment: str):
    '''
    查看部署性能
    Parameters:
     deployment - 部署名称
    Returns:
     多值返回
     第一个变量为一个布尔变量，False为访问失败，True为访问成功
     成功则第二个变量为一个六元组，从左往右依次是
            (执行次数，平均响应时间，最大响应时间，最小响应时间，
                首次访问时间点——初始值为None，最近一次访问时间点——初始值为None)
     失败则为错误信息，'deployment not found' : 任务id不存在
    Raises:
     参数类型错误
    '''
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('''SELECT times, averagecost, maxcost,
                    mincost, firstvisit, lastvisit FROM deployments 
                    WHERE deployment = ?''' , 
                    (deployment, ))
    row = c.fetchone()
    if row is None:
        answer = 'deployment not found'
    else:
        answer = row
    conn.close()
    return bool(row), answer


def init():
    '''
    初始化数据库
    创建六个管理员用户，并且加入默认的任务
    Parameters:
     None
    Returns:
     None
    Raises:
     本函数不应该报错
    '''
    if not os.path.exists(database):
        # 创建数据库
        conn = sqlite3.connect(database)
        c = conn.cursor()
        # 创建用户表
        c.execute('''CREATE TABLE users 
                        (user TEXT, password TEXT, roll TEXT, 
                        modelid NUMBER, delayresponsetaskid NUMBER, waittaskid NUMBER);''')
        c.executemany('INSERT INTO users VALUES (?,?,?,?,?,?)', 
                        [('tyf', '123456', 'administrator', 1, 1, 1),
                         ('crk', '123456', 'administrator', 1, 1, 1),
                         ('zyt', '123456', 'administrator', 1, 1, 1),
                         ('wzn', '123456', 'administrator', 1, 1, 1),
                         ('llz', '123456', 'administrator', 1, 1, 1),
                         ('lxt', '123456', 'administrator', 1, 1, 1)])
        # 创建模型表
        c.execute('''CREATE TABLE models 
                        (user TEXT, modelid NUMBER, 
                        modelname TEXT, modeltype TEXT, 
                        time TEXT, modelroute TEXT, 
                        algorithm TEXT, engine TEXT, 
                        description TEXT);''')
        # 创建task表
        c.execute('''CREATE TABLE delayresponsetasks
                        (user TEXT, id TEXT, 
                        modelname TEXT, deployment TEXT, file TEXT);''')
        # 创建模型变量表
        c.execute('''CREATE TABLE variables 
                        (user TEXT, id NUMBER, modelname TEXT, 
                        inout TEXT, name TEXT, 
                        type TEXT, value TEXT, dim TEXT, optype TEXT);''')
        # 创建部署任务表
        c.execute('''CREATE TABLE deployments 
                        (user TEXT, modelname TEXT, 
                        deployment TEXT, status TEXT, time TEXT, 
                        times INTEGER, averagecost REAL, 
                        maxcost REAL, mincost REAL, 
                        firstvisit TEXT, lastvisit TEXT);''')
        # 提交，关闭数据库
        conn.commit()
        conn.close()
        print('database has been created')


def restart():
    '''
    重新创建数据库
    Parameters:
     None
    Returns:
     None
    Raises:
     本函数不应该报错
    '''
    if os.path.exists(database):
        os.remove(database)
    init()