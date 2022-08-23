import json
import os
import prepare as default_prepare
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
        # data = default_prepare.readimg(input_type[0], filepath, file)
        # 如果您传入的是mp4
        #data = default_prepare.readmp4(input_type[0], filepath, file)
        # 如果您传入的是txt
        # data = default_prepare.readtxt(input_type, filepath, file)
        # 如果您传入的是csv
        # data = default_prepare.readcsv(input_type, filepath, file)
        # 如果您传入的是zip
        # data = default_prepare.readzip(input_type, filepath, file)
        
        os.remove(filepath)
        return data