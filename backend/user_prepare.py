import zipfile
import pandas as pd
import json
import os

def process_text_to_json(fileaddress: str):
    f = open(fileaddress)
    string = f.read()
    f.close()
    json_dict = json.loads(string)
    return json_dict
def process_base64_to_csv(file, id: int):
    path = './output/zip/' + str(id)
    #os.makedirs(path)
    f = zipfile.ZipFile(file)
    for fz in f.namelist():  
        f.extract(fz, path)
    file_list = os.listdir(path)
    df = pd.DataFrame()
    for txt_address in file_list:
        temp_address = path + '/' + txt_address
        temp_json_dict = process_text_to_json(temp_address)
        temp_df = pd.DataFrame(temp_json_dict, index=[0])
        df = pd.concat([df, temp_df])
    return df
    
def prepare(model_input_type,file):
    return process_base64_to_csv(file, 100)
