import requests

files = {
    'user': (None, 'tyf'),
    'password': (None, '123456'),
    # 'image': ('image.jpg', open('%s/resource/upload_images/image.jpg' % PATH_DIR, 'rb'), 'application/octet-stream') 参考的文件上传办法，https://www.cnblogs.com/mlllily/p/14554907.html
}
response = requests.post('http://127.0.0.1:5000/login', files=files)
print(response.content.decode('utf-8'))