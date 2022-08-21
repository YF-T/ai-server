import requests
import json

files = {
    'user': (None, 'tyf'),
    'password': (None, '123456'),
    'modelname': (None, 'test2'),
    'file' : (None, '''{"sepal length (cm)":1.0,"sepal width (cm)":1.0,"petal length (cm)":1.0,"petal width (cm)":1.0}'''), 
    'prepare_py' : (None, '''import json \ndef prepare(model_input_type, file):\n    return json.loads(file)'''),
    'filetype' : (None, 'none')
    # 'image': ('image.jpg', open('%s/resource/upload_images/image.jpg' % PATH_DIR, 'rb'), 'application/octet-stream') 参考的文件上传办法，https://www.cnblogs.com/mlllily/p/14554907.html
}
print('输入：')
print(files)
response = requests.post('http://127.0.0.1:5000/testmodel_quickresponse/ttt', files=files)
print('输出：')
print(response.content.decode('utf-8'))
'''
curl -X POST -F file='{"sepal length (cm)":1.0,"sepal width (cm)":1.0,"petal length (cm)":1.0,"petal width (cm)":1.0}' -F prepare_py="import json ^ndef  prepare(model_input_type,file):^n    return json.loads(file)" http://127.0.0.1:5000/testmodel_quickresponse/ttt

curl -X POST -H '{"Content-Type":"application/x-www-form-urlencoded"}' -F 'file=10' -F 'prepare_py=20' http://127.0.0.1:5000/testmodel_quickresponse/ttt

curl -X POST -F user="tyf" -F password="123456" http://127.0.0.1:5000/login
'''