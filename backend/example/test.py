import cv2
import base64
import numpy as np
import pandas as pd
import onnx
import onnxruntime as ort

#只是测试
def img_to_base64(img_array):
    # 传入图片为RGB格式numpy矩阵，传出的base64也是通过RGB的编码
    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)  # RGB2BGR，用于cv2编码
    encode_image = cv2.imencode(".jpg", img_array)[1]  # 用cv2压缩/编码，转为一维数组
    byte_data = encode_image.tobytes()  # 转换为二进制
    base64_str = base64.b64encode(byte_data).decode("ascii")  # 转换为base64
    return base64_str


def base64_to_img(base64_str):
    # 传入为RGB格式下的base64，传出为RGB格式的numpy矩阵
    byte_data = base64.b64decode(base64_str)  # 将base64转换为二进制
    encode_image = np.asarray(bytearray(byte_data), dtype="uint8")  # 二进制转换为一维数组
    img_array = cv2.imdecode(encode_image, cv2.IMREAD_COLOR)  # 用cv2解码为三通道矩阵
    if img_array.shape[2]>1:
        #print(img_array.shape[2])
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)#转换为单通道
    #修改图片大小
    res = cv2.resize(img_array, (28,28), interpolation=cv2.INTER_CUBIC)
    #符合模型维数
    res=res.reshape(1,1,28,28)
    return res


def base64_to_video(base64_str):
    pass

def prepare():
    pass


from importlib import reload
def find():
    reload(haha)
    c = haha.admin()
    print(c)


if __name__ == '__main__':
    f2=open("haha.py", 'w', encoding='UTF-8')
    str="def admin():\n    return 7+2"
    f2.write(str)
    f2.close()
    #判断haha.py是否有语法错误
    try:
        import haha
        print('a')
    except:
        print('false')
        pass
    else:
        c=haha.admin()
        print(c)





    '''a = [1, 2, 3]
    b = [4, 5, 6]
    c = [7, 8, 9]
    w2 = np.array([[a, b, c], [a, b, c]])'''

    #e=pd.DataFrame(i)
    #i=i.reshape(4,)
    #e=pd.DataFrame(i)
    #print(e)