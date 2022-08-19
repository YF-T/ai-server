from msilib.schema import File
import cv2
import base64
import numpy as np
import pandas as pd
import json
import onnx
import onnxruntime as ort



#脚本
#处理图片
#要改，可能传入jpg路径
def process_img(img_array, model_input_type):
    #处理img文件
    if img_array.shape[2] > 1:
        # print(img_array.shape[2])
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)  # 转换为单通道
    res = resize_img(img_array)
    return res

#处理图片 base64格式输入
def process_base64_to_img(base64_str: str, model_input_type):
    # 传入为RGB格式下的base64，传出为RGB格式的numpy矩阵
    byte_data = base64.b64decode(base64_str)  # 将base64转换为二进制
    encode_image = np.asarray(bytearray(byte_data), dtype="uint8")  # 二进制转换为一维数组
    img_array = cv2.imdecode(encode_image, cv2.IMREAD_COLOR)  # 用cv2解码为三通道矩阵
    if img_array.shape[2]>1:
        #print(img_array.shape[2])
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)#转换为单通道
    res=resize_img(img_array,model_input_type)
    return res

def resize_img(img,model_input_type):
    # 修改图片大小
    res = cv2.resize(img, (28, 28), interpolation=cv2.INTER_CUBIC)
    # 符合模型维数
    res = res.reshape(1, 1, 28, 28)
    return res

# 处理文本
def process_text_to_json(fileaddress: str):
    f = open(fileaddress)
    string = f.read()
    json_dict = json.loads(string)
    return json_dict
# 传入文件路径，传出转化后的dict，可以直接被模型使用


#处理视频
def process_base64_to_vedio(base64_str: str):
    pass


# 处理压缩包(转成csv)
def process_base64_to_csv(base64_str: str):
    pass


#预处理总函数
def prepare(model_input_type, file, filetype, fileaddress):
    if filetype=="jpgbase64":
        process_base64_to_img(file,model_input_type)
    elif filetype=="csv":
        return file
        # 对于csv格式，pmml和onnx都可以直接读取，本示例中不做预处理
    elif filetype=="txt":
        return process_text_to_json(fileaddress)
        # 对于txt格式文件：将文件内json形式的字符串转化为dict
    elif filetype=="mp4base64":
        pass
    elif filetype=="zip":
        pass



'''if __name__ == '__main__':

    cv2_img = cv2.imread('./t1.jpg')
    print(type(cv2_img))
    b=img_to_base64(cv2_img)
    print(b)
    i=process_base64_to_img(b)

    i = i.astype('float32')
    sess = ort.InferenceSession('./model/testonnx.onnx')  # 加载模型
    ort_inputs = {sess.get_inputs()[0].name: i}
    print(sess.get_inputs()[0])
    output = sess.run(None, ort_inputs)
    print(type(output))'''

    #e=pd.DataFrame(i)
    #i=i.reshape(4,)
    #e=pd.DataFrame(i)
    #print(e)

'''#只是测试 要删
def img_to_base64(img_array):
    # 传入图片为RGB格式numpy矩阵，传出的base64也是通过RGB的编码
    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)  # RGB2BGR，用于cv2编码
    encode_image = cv2.imencode(".jpg", img_array)[1]  # 用cv2压缩/编码，转为一维数组
    byte_data = encode_image.tobytes()  # 转换为二进制
    base64_str = base64.b64encode(byte_data).decode("ascii")  # 转换为base64
    return base64_str'''
