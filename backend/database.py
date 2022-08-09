import sqlite3
import os

database = 'information.db'

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
     成功则为一个列表，这个列表包含该用户的每一个模型，每个模型的信息是一个四元组：(模型id，模型名称，类型，时间)
                                     如(1, 'test', 'pmml', '2022-08-04 19:00:00')
     失败则为一个字符串代表错误信息，'user not found' : 用户不存在
                                     'invalid password' : 密码错误 
     
    Raises:
     本函数不应该报错
    '''
    if identify(user, password) != 'success':
        return False, identify(user, password)
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('SELECT modelid, modelname, modeltype, time FROM models WHERE user = ?', (user,))
    answer = c.fetchall()
    conn.close()
    return True, answer

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
    找到模型对应的描述信息
     
    Parameters:
     uese - 用户名
     password - 密码
     modelname - 模型名称，先假设非重复，之后再去重
     
    Returns:
     多值返回
     第一个变量为一个布尔变量，False为访问失败，True为访问成功
     第二个变量为一个字符串
     成功则为模型描述，一个字符串表示模型的描述，如'测试模型'
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
    c.execute('SELECT description FROM models WHERE user = ? AND modelname = ?', 
                    (user, modelname))
    row = c.fetchone()
    if row is None:
        answer = 'model not found'
    else:
        answer = row[0]
    conn.close()
    return bool(row), answer

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
        分别为字段名，类型，取值范围（若没有则为None），维数（没有则为None）
        如('input', 'int', '0,1,2,3', '1*8')
        如('input', 'int', None, None)
     第三个变量为一个list，里面装着所有的输出变量信息，格式同上
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
    c.execute('''SELECT name, type, value, dim FROM variables 
                    WHERE user = ? AND modelname = ? AND inout = ?''', 
                    (user, modelname, 'input'))
    input = c.fetchall()
    c.execute('''SELECT name, type, value, dim FROM variables 
                    WHERE user = ? AND modelname = ? AND inout = ?''', 
                    (user, modelname, 'output'))
    output = c.fetchall()
    conn.close()
    return True, input, output

def savemodel(user : str, password : str, modelname : str, modeltype : str, 
                time : str, modelroute : str, description : str, 
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
     input - 输入变量信息的列表
        每个输入变量信息用一个元组(tuple)表示，元组里有四个str类型的元素，
        分别为字段名，类型，取值范围（若没有则为None），维数（没有则为None）
        如('input', 'int', '0,1,2,3', '1*8')
        如('input', 'int', None, None)
     output - 输出变量信息的列表，每个变量的信息格式如上
     
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
    c.execute('INSERT INTO models VALUES (?,?,?,?,?,?,?)', 
                    (user, modelid, modelname, modeltype, 
                    time, modelroute, description))
    for variable in input:
        c.execute('INSERT INTO variables VALUES (?,?,?,?,?,?,?,?)', 
                    (user, modelid, modelname, 'input', 
                    variable[0], variable[1], variable[2], variable[3]))
    for variable in output:
        c.execute('INSERT INTO variables VALUES (?,?,?,?,?,?,?,?)', 
                    (user, modelid, modelname, 'output', 
                    variable[0], variable[1], variable[2], variable[3]))
    conn.commit()
    conn.close()
    return 'success'

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
                        modelid NUMBER, immediatetaskid NUMBER, waittaskid NUMBER);''')
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
                        description TEXT);''')
        c.executemany('INSERT INTO models VALUES (?,?,?,?,?,?,?)', 
                        [('tyf', -1, 'test', 'pmml', 
                         '2020-08-03 16:00:00', 'randomForest.pmml', '测试模型'),
                         ('crk', -1, 'test', 'pmml', 
                         '2020-08-03 16:00:00', 'randomForest.pmml', '测试模型'),
                         ('zyt', -1, 'test', 'pmml', 
                         '2020-08-03 16:00:00', 'randomForest.pmml', '测试模型'),
                         ('wzn', -1, 'test', 'pmml', 
                         '2020-08-03 16:00:00', 'randomForest.pmml', '测试模型'),
                         ('llz', -1, 'test', 'pmml', 
                         '2020-08-03 16:00:00', 'randomForest.pmml', '测试模型'),
                         ('lxt', -1, 'test', 'pmml', 
                         '2020-08-03 16:00:00', 'randomForest.pmml', '测试模型')])
        # 创建立即任务表
        c.execute('''CREATE TABLE immediatetasks
                        (user TEXT, id NUMBER, 
                        inputroute TEXT, outputroute TEXT);''')
        # 创建等待任务表
        c.execute('''CREATE TABLE waittasks 
                        (user TEXT, id NUMBER, 
                        inputroute TEXT, outputroute TEXT);''')
        # 创建模型变量表
        c.execute('''CREATE TABLE variables 
                        (user TEXT, id NUMBER, modelname TEXT, 
                        inout TEXT, name TEXT, 
                        type TEXT, value TEXT, dim TEXT);''')
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