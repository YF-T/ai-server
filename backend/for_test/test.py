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
curl -X POST -F file={"""sepal length (cm)""":1.0,"""sepal width (cm)""":1.0,"""petal length (cm)""":1.0,"""petal width (cm)""":1.0} -F prepare_py="import json @@def prepare(model_input_type,file):@@    print(file)@@    return json.loads(file)" http://127.0.0.1:5000/testmodel_quickresponse/qqq

curl -X POST -H '{"Content-Type":"application/x-www-form-urlencoded"}' -F 'file=10' -F 'prepare_py=20' http://127.0.0.1:5000/testmodel_quickresponse/ttt

curl -X POST -F user="tyf" -F password="123456" http://127.0.0.1:5000/login

curl -X POST -F file=@"./input.txt" -F prepare_py="import json @@def prepare(model_input_type,file):@@    string = file.read()@@    return json.loads(string)" http://127.0.0.1:5000/testmodel_quickresponse/qqq

def process_text_to_json(fileaddress: str):
    
    f = open(fileaddress)
    string = f.read()
    json_dict = json.loads(string)
    return json_dict
    
    
    
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
    
def prepare(model_input_type,file):
    return process_base64_to_csv(file, 100)
    
import zipfile@@def process_base64_to_csv(file, id: int):@@    path = \'./output/zip/\' + str(id)@@    os.mkDir(path)@@    if not file.endswith(".zip"):@@        return jsonify({\'status\': \'the file is not a zip\'})@@    # 若非zip文件则返回，原则上不 应报错@@    f = zipfile.ZipFile(file)@@    for fz in f.namelist():  # 遍历压缩包列表中的所有文件@@        # 解压缩到路径path@@        f.extract(fz, path)@@    file_list = os.listdir(path)@@    df = pd.DataFrame()@@    for txt_address in file_list:@@        temp_address = path + \'/\' + txt_address@@        # 对当前txt文件地址，调用text转json函数@@        temp_json_dict = process_text_to_json(temp_address)@@        temp_df = pd.DataFrame(temp_json_dict)@@        df = pd.concat([df, temp_df])@@    return df@@    @@def prepare(model_input_type,file):@@    return process_base64_to_csv(file, 100)@@

curl -X POST -F file=@"./input.zip" -F prepare_py="import zipfile@@import pandas as pd@@import json@@import os@@def process_text_to_json(fileaddress: str):@@    f = open(fileaddress)@@    string = f.read()@@    f.close()@@    json_dict = json.loads(string)@@    return json_dict@@def process_base64_to_csv(file, id: int):@@    path = './output/zip/' + str(id)@@    #os.makedirs(path)@@    f = zipfile.ZipFile(file)@@    for fz in f.namelist():  @@        f.extract(fz, path)@@    file_list = os.listdir(path)@@    df = pd.DataFrame()@@    for txt_address in file_list:@@        temp_address = path + '/' + txt_address@@        temp_json_dict = process_text_to_json(temp_address)@@        temp_df = pd.DataFrame(temp_json_dict, index=[0])@@        df = pd.concat([df, temp_df])@@    return df@@    @@def prepare(model_input_type,file):@@    return process_base64_to_csv(file, 100)@@" http://127.0.0.1:5000/testmodel_delayresponse/qqq

curl -X POST -F file=@"./input.zip" -F prepare_py=@"./user_prepare.py" http://127.0.0.1:5000/testmodel_delayresponse/qqq

curl -X POST http://127.0.0.1:5000/get_result_delayresponse/qqq/tyf_task_2

/get_result_delayresponse/<deployment>/<taskid>
'''