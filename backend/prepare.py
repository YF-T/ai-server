import cv2
import base64
import numpy as np
import pandas as pd
import json
import os
from flask import jsonify
import zipfile



'''
处理jpg能调用的函数：
    process_img_path(path, input_type)#path为jpg的存储地址，input_type为单个输入变量信息，为tuple 五元组，如('Input3', 'tensor(float)', None, '1*1*28*28', None)
    process_base64_to_img(base64_str, input_type)#base64_str为jpg的base64编码，input_type为单个输入变量信息，为tuple 五元组
处理MP4能调用的函数：
    process_mp4(path, input_type)#path为mp4的存储地址，input_type为单个输入变量信息，为tuple 五元组
处理txt能调用的函数：
    process_text_to_json(fileaddress: str)#fileaddress为txt的存储地址
处理zip能调用的函数：
def process_base64_to_csv(file, id: int)# 处理压缩包(假设压缩包内均为.txt文档，且文档内为json指令格式，最终转成csv)
                                        #为了创建文件夹方便，希望最好能传入当前任务的id
'''

#传入jpg路径
def process_img_path(path, input_type):
    # 传入为RGB格式下的base64，传出为RGB格式的numpy矩阵
    img_array =cv2.imread(path)
    if img_array.shape[2]>1:
        #print(img_array.shape[2])
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)#转换为单通道
    res=resize_img(img_array,input_type)
    #根据模型需要的输入调节
    res = res.astype('float32')
    res = {input_type[0]: res}
    return res


#处理图片 base64格式输入
def process_base64_to_img(base64_str: str, input_type):
    # 传入为RGB格式下的base64，传出为RGB格式的numpy矩阵
    byte_data = base64.b64decode(base64_str)  # 将base64转换为二进制
    encode_image = np.asarray(bytearray(byte_data), dtype="uint8")  # 二进制转换为一维数组
    img_array = cv2.imdecode(encode_image, cv2.IMREAD_COLOR)  # 用cv2解码为三通道矩阵
    if img_array.shape[2] > 1:
        #print(img_array.shape[2])
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)#转换为单通道
    res=resize_img(img_array,input_type)
    #根据模型需要的输入调节
    res = res.astype('float32')
    res = {input_type[0]: res}
    return res

def resize_img(img, model_input):
    # 修改图片大小
    #读取所需维数及其元组个数
    shape=model_input[3]
    type=model_input[2]
    #print(shape)
    #print(type(shape))
    if shape ==None:
        img=img.ravel()
        return img[0]
    else:
        #读取总维数
        shape_list=shape.split("*")
        shape_list = np.array(shape_list).astype(dtype=int).tolist()
        #print(type(shape_list))
        n=1
        for i in shape_list:
            n=n*int(i)
        img=img.ravel()
        img=img[0:n]
        img=img.reshape(shape_list)
        return img

# 处理文本
def process_text_to_json(fileaddress: str):
    f = open(fileaddress)
    string = f.read()
    f.close()
    json_dict = json.loads(string)
    return json_dict
# 传入文件路径，传出转化后的dict，可以直接被模型使用


#处理视频
def process_mp4(path, input_type):
    videoCapture = cv2.VideoCapture(path)
    rval = videoCapture.isOpened()
    res={"input":None}
    while rval:  # 循环读取视频帧
        rval, frame = videoCapture.read()
        if rval:
            #用户自定义处理
            res = process_img(frame, input_type)
    return res

    #传入编码好的jpg
def process_img(img_array, model_input_type):
    #处理img文件
    if img_array.shape[2] > 1:
        # print(img_array.shape[2])
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)  # 转换为单通道
    res = resize_img(img_array,model_input_type)
    res = res.astype('float32')
    res={model_input_type[0]:res}
    return res

def process_base64_mp4(file, model_input_type):
    #base64转码
    mp4_data = base64.b64decode(file)
    mp4_data = np.asarray(bytearray(mp4_data), dtype="uint8")
    #之后操作 用户自定义
    return mp4_data


# 处理压缩包(假设压缩包内均为.txt文档，且文档内为json指令格式，最终转成csv)
# 为了创建文件夹方便，希望最好能传入当前任务的id
def process_base64_to_csv(file, id: int):
    path = './output/zip/' + str(id)
    os.mkDir(path)
    if not file.endswith(".zip"):
        return jsonify({'status': 'the file is not a zip'})
    # 若非zip文件则返回，原则上不应报错
    f = zipfile.ZipFile(file)
    for fz in f.namelist():  # 遍历压缩包列表中的所有文件
        # 解压缩到路径path
        f.extract(fz, path)
    file_list = os.listdir(path)
    df = pd.DataFrame()
    for txt_address in file_list:
        temp_address = path + '/' + txt_address
        # 对当前txt文件地址，调用text转json函数
        temp_json_dict = process_text_to_json(temp_address)
        temp_df = pd.DataFrame(temp_json_dict)
        df = pd.concat([df, temp_df])
    return df


# 预处理总函数
def prepare(model_input_type, file, filetype, fileaddress: str, id: 0):
    if filetype=="jpgbase64":
        #base64格式的jpg文件
        return process_base64_to_img(file,model_input_type)

    elif filetype=="jpg":
        return process_img_path(fileaddress, model_input_type)
        # 传入jpg的地址

    elif filetype=="csv":
        return file
        # 对于csv格式，pmml和onnx都可以直接读取，本示例中不做预处理

    elif filetype=="txt":
        return process_text_to_json(fileaddress)
        # 对于txt格式文件：将文件内json形式的字符串转化为dict

    elif filetype=="mp4base64":
        return process_base64_mp4(file, model_input_type)

    elif filetype=="mp4":
        return process_mp4(fileaddress, model_input_type)
        #传入mp4的地址

    elif filetype=="zip":
        return process_base64_to_csv(file, id)

    else:
        return jsonify({'invalid type'})


'''def img_to_base64(img_array):
    # 传入图片为RGB格式numpy矩阵，传出的base64也是通过RGB的编码
    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)  # RGB2BGR，用于cv2编码
    encode_image = cv2.imencode(".jpg", img_array)[1]  # 用cv2压缩/编码，转为一维数组
    byte_data = encode_image.tobytes()  # 转换为二进制
    base64_str = base64.b64encode(byte_data).decode("ascii")  # 转换为base64
    return base64_str'''

'''def reshape_onnx_test(img, model_input):
    res = cv2.resize(img, (28, 28), interpolation=cv2.INTER_CUBIC)
    # 符合模型维数
    res = res.reshape(1, 1, 28, 28)
    return res'''


