import requests


files = {
    'user': (None, 'tyf'),
    'password': (None, '123456'),
    'modelname': (None, 'test6')
    # 'image': ('image.jpg', open('%s/resource/upload_images/image.jpg' % PATH_DIR, 'rb'), 'application/octet-stream') 参考的文件上传办法，https://www.cnblogs.com/mlllily/p/14554907.html
}
response = requests.get('http://127.0.0.1:5000/getusermodel', files=files)
print(response.content.decode('utf-8'))
response = requests.delete('http://127.0.0.1:5000/deletemodel', files=files)
print(response.content.decode('utf-8'))