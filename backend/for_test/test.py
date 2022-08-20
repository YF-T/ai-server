import requests
import json

files = {
    'user': (None, 'tyf'),
    'password': (None, '123456'),
    'modelname': (None, 'test2'),
    'input': (None, json.dumps({'sepal length (cm)': 1.0, 
                     'sepal width (cm)': 1.0, 
                     'petal length (cm)': 1.0, 
                     'petal width (cm)': 1.0}))
    # 'image': ('image.jpg', open('%s/resource/upload_images/image.jpg' % PATH_DIR, 'rb'), 'application/octet-stream') 参考的文件上传办法，https://www.cnblogs.com/mlllily/p/14554907.html
}
print('输入：')
print(files)
response = requests.post('http://127.0.0.1:5000/testmodel_test', files=files)
print('输出：')
print(response.content.decode('utf-8'))