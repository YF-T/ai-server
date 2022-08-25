import json
import os
import prepare as preprocess
def prepare(input_type, file):
    if isinstance(file, str):
        # 如果您传入的是字符串可以直接使用json.loads
        return json.loads(file)
    else:
        filepath = './input_file/' + file.filename
        file.save(filepath)
        data = None
        
        # todo
        # 如果您传入的是jpg
        # data = preprocess.readimg(input_type[0], filepath, file)
        # 如果您传入的是mp4
        # data = preprocess.readmp4(input_type[0], filepath, file)
        # 如果您传入的是txt
        # data = preprocess.readtxt(input_type, filepath, file)
        # 如果您传入的是csv
        # data = preprocess.readcsv(input_type, filepath, file)
        # 如果您传入的是zip
        # data = preprocess.readzip(input_type, filepath, file)
        
        os.remove(filepath)
        return data