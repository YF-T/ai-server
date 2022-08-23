import json
import os
import prepare as default_prepare
def prepare(input_type, file):
    if isinstance(file, str):
        return json(file)
    else:
        filepath = './input_file/' + file.filename
        file.save(filepath)
        data = None
        
        # todo
        
        os.remove(filepath)
        return data