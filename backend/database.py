import sqlite3
import os

database = 'information.db'

def identify(user : str, password : str):
    '''
    TODO
    身份识别函数，识别用户是否存在/用户名与密码是否匹配
     
    Parameters:
     uese - 用户名
     password - 密码
     
    Returns:
     'success' : 成功
     'user not found' : 用户不存在
     'password error' : 密码错误
     
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
        status = 'password error'
    conn.close()
    return status

def getmodel(user : str, password : str, modelname : str):
    '''
    TODO
    找到模型对应的存储地址
     
    Parameters:
     uese - 用户名
     password - 密码
     modelname - 模型名称，先假设非重复，之后再去重
     
    Returns:
     一个字符串表示模型的名称，如'test.pmml'
     
    Raises:
     本函数不应该报错
    '''
    return 'randomForest.pmml'

def savemodel(user : str, password : str, modelname : str):
    '''
    TODO
    存储模型对应的存储地址
     
    Parameters:
     uese - 用户名
     password - 密码
     modelname - 模型名称
     
    Returns:
     'success' : 成功
     'duplication' : 重名，不合法
     
    Raises:
     本函数不应该报错
    '''
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
        cur = conn.cursor()
        # 创建用户表
        cur.execute('''CREATE TABLE users 
                        (user TEXT, password TEXT, roll TEXT, 
                        modelid NUMBER, immediatetaskid NUMBER, waittaskid NUMBER);''')
        cur.executemany('INSERT INTO users VALUES (?,?,?,?,?,?)', 
                        [('tyf', '123456', 'administrator', 1, 1, 1),
                         ('crk', '123456', 'administrator', 1, 1, 1),
                         ('zyt', '123456', 'administrator', 1, 1, 1),
                         ('wzn', '123456', 'administrator', 1, 1, 1),
                         ('llz', '123456', 'administrator', 1, 1, 1),
                         ('lxt', '123456', 'administrator', 1, 1, 1)])
        # 创建模型表
        cur.execute('''CREATE TABLE models 
                        (user TEXT, modelid NUMBER, 
                        modelname TEXT, modelroute TEXT);''')
        cur.executemany('INSERT INTO models VALUES (?,?,?,?)', 
                        [('tyf', '123456', 'test', 'randomForest.pmml'),
                         ('crk', '123456', 'test', 'randomForest.pmml'),
                         ('zyt', '123456', 'test', 'randomForest.pmml'),
                         ('wzn', '123456', 'test', 'randomForest.pmml'),
                         ('llz', '123456', 'test', 'randomForest.pmml'),
                         ('lxt', '123456', 'test', 'randomForest.pmml')])
        # 创建立即任务表
        cur.execute('''CREATE TABLE immediatetasks
                        (user TEXT, id NUMBER, 
                        inputroute TEXT, outputroute TEXT);''')
        # 创建等待任务表
        cur.execute('''CREATE TABLE waittasks 
                        (user TEXT, id NUMBER, 
                        inputroute TEXT, outputroute TEXT);''')
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