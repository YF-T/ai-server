# 前后端大作业——机器学习模型服务

## TODO List

### 前端

- 登录页面

- 主页（也可以不要，直接导航栏接功能应该也行）

- 模型管理界面

  > 列出所有部署在平台上的模型的列表

- 上传/修改模型窗口

  > 名称，简介，类型，文件传输窗口

- 模型测试页面/窗口

  > 用户输入数据，输出预测结果

- 部署模型页面/窗口（也可以融合在模型管理页面里）

  > 支持启动，暂停服务，监控模型的服务状态（如接受了多少次服务，性能如何，响应时间之类的）

- 部署模型测试界面/窗口

  > 类似模型测试界面，不同的是要加上批量化处理的内容

- 部署模型后任务id查看结果的界面

  > 这个可以用模板，最好是针对每个模型都能显示单独的一页，上面有一个列表标出所有id，不过所有模型一个也可以

- 任务管理查看界面（可选）

*备注：上述界面可以采取每个界面当作一个组件的形式，这样在切换界面时可以只切换组件，不用切换任务栏等每个界面都一样的东西。*

### 后端

#### 基本功能

- 登录并核对用户名，密码的接口（完成）
- 注册用户（完成）

##### 上传模型

- 接收并存储模型，判断模型是否有效的接口

  > 用于接收上传的模型，并存储在当前模型的列表中

- 删除模型的接口（完成）

- 修改模型信息的接口

- 查看模型信息的接口（完成）

- 查看用户的所有模型的简略信息（完成）

##### 测试模型

- 表单输入数据&json直接输入数据，返回预测结果的接口
- 文件输入返回预测结果的接口

##### 部署模型

- 部署模型服务的接口
- 启动服务的接口（完成）
- 暂停服务的接口（完成）
- 删除服务的接口
- 显示当前服务状态的接口
- 查看当前模型的所有部署的接口

##### 部署模型的restful api

- 快速返回的接口

  > 基本与测试模型相同

- 等待返回的立即返回任务id的接口

- 通过id查询状态的接口

- 通过id查询结果的接口

#### 附加功能

##### 验证模型有效性

> 后端任务
>
> 已完成
>
> 已经写在接收模型的接口当中

##### 预留CPU和内存

> 后端任务
>
> 尚未确定是否做
>
> 如要做则写在部署模型服务的接口中

##### 创建自定义脚本预处理输入

> 后端任务
>
> TODO

- 接收预处理脚本的接口

##### 扩展模型格式

> 后端任务
>
> 大概率不做

##### 监控模型服务

> 前后端任务
>
> 尚未确定是否要做

- 查看部署模型运行情况的接口

##### 任务管理查看界面

> 前端任务

- 查看已部署任务的接口

##### 模型服务的伸缩

> 后端任务
>
> 大概率不做
>
> 没有特定的接口

## 规范

### 文件结构

```
├── frontend
├── backend
│   ├── model : 存放模型的文件夹，最好有一个不会重复的命名方式命名文件
│   ├── for_test : 存放调试相关脚本的文件夹，项目完工之后删
│   │   ├── test.py : 调试接口
│   │   └── testmodel.py : 调试模型
│   ├── app.py : 接口
│   └── database.py : 数据库交互相关函数
└── README.md
```

### 接口

> 包括接口路径，传递的参数和意义，传递方法，接口作用等
>
> 注意用formdata传递参数

#### /login (post)

> 登录接口
>
> Parameters:
> uesr - 用户名
> password - 密码
>
> Returns:
> 'success' : 成功
> 'user not found' : 用户不存在
> 'invalid password' : 密码错误
>
> Raises:
>  若用户名或密码不是字符串则报错

#### /register (post)

> 注册接口
>
> Parameters:
>  uesr - 用户名
>  password - 密码
>
> Returns:
>  'success' : 成功
>  'duplication' : 用户重名
>  
>Raises:
> 若用户名或密码不是字符串则报错

#### /getmodelinfo (get)

>
> 获取用户模型信息
>
> Parameters:
>  user : str - 用户名
>  password : str - 密码
>  modelname : str - 模型名称
>
> Returns:
>  status : str - 'success' : 成功
>                 'user not found' : 用户不存在
>                 'invalid password' : 密码错误
>  **若成功才有以下属性：**
>  modelname : str - 模型名称
>  time : str - 模型创建时间
>  modeltype : str - 模型类型
>  algorithm : str - 模型算法
>  description : str - 模型描述
>  engine : str - 模型引擎
>  input : list - 输入变量，list里面的元素为一个字典，
>                 'name' : str - 变量名
>                 'type' : str - 变量类型
>                 'range' : str - 变量取值范围
>                 'dimension' : str - 变量维数
>                 'optype' : str - 持续
>  output : list - 输出变量，格式同input
>
> Raises:
>  输入变量类型错误则报错

#### /getusermodel (get)

> 获取用户模型信息
>
> Parameters:
>  user : str - 用户名
>  password : str - 密码
>
> Returns:
>  status : str - 'success' : 成功
>                 'user not found' : 用户不存在
>                 'invalid password' : 密码错误
>  若成功才有以下属性：
>  model : list - 一个包括所有该用户model的简略信息
>                 每个元素为一个字典，属性包括
>                 'modelname' : str - 模型名
>                 'modeltype' : str - 模型类型
>                 'time' : str - 模型日期
>
> Raises:
> 输入变量类型错误则报错

#### /deletemodel (delete)

> 删除模型
>
> Parameters:
>  user : str - 用户名
>  password : str - 密码
>
> Returns:
>  status : str - 'success' : 成功
>                 'user not found' : 用户不存在
>                 'invalid password' : 密码错误
>                 'model not found' : 找不到该名称模型
>
> Raises:
>  本函数不应该报错

#### /getmodeldeployment (get)

> 查看部署的服务
>
> Parameters:
>  user : str - 用户名
>  password : str - 密码
>  modelname : str - 模型名
>
> Returns:
>  status : str - 'success' : 设置成功
>                 'user not found' : 用户不存在
>                 'invalid password' : 密码错误
>                 'model not found' : 找不到该名称模型
>  若成功才有以下属性：
>  deployment : list - 一个包括所有该模型部署的简略信息
>                 每个元素为一个字典，属性包括
>                 'deployment' : str - 部署名
>                 'status' : str - 模型类型
>                 'time' : str - 创建日期
>
> Raises:
>  本函数不应该报错

#### /setdeploymentstatusrunning (post)

> 启动部署的服务
>
> Parameters:
>   user : str - 用户名
>   password : str - 密码
>   modelname : str - 模型名
> deployment : str - 部署名
> 
>  Returns:
>     status : str - 'success' : 设置成功
>                    'user not found' : 用户不存在
>                    'invalid password' : 密码错误
>                    'deployment not found' : 部署不存在
>
> Raises:
>   本函数不应该报错

#### /settaskstatuspause (post)

> 暂停部署的服务
>
> Parameters:
>   user : str - 用户名
>   password : str - 密码
>   modelname : str - 模型名
> deployment : str - 部署名
> 
>  Returns:
>     status : str - 'success' : 设置成功
>                    'user not found' : 用户不存在
>                    'invalid password' : 密码错误
>                    'deployment not found' : 部署不存在
>
> Raises:
>   本函数不应该报错

### 报错信息

> 包括错误描述，错误码，错误提示信息等，用于错误处理



## 一些其他的想法

可以做一个管理员身份的用户，可以对数据库进行删除等工作，方便管理。