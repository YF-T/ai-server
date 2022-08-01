
def identify(user : str, password : str):
    '''
    TODO
    身份识别函数，识别用户是否存在/用户名与密码是否匹配
     
    Parameters:
     uese - 用户名
     password - 密码
     
    Returns:
     一个布尔值表示用户名是否匹配
     TODO：之后可能会增加一些用户的权限系统用于区分管理员和普通用户
     
    Raises:
     本函数不应该报错
    '''
    return True

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