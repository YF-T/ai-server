import sys
import onnx
import onnxruntime
import re
from xml.etree import ElementTree as ET

import check_pmml_xsd.pmml_441
import check_pmml_xsd.pmml_44
import check_pmml_xsd.pmml_43
import check_pmml_xsd.pmml_42
import check_pmml_xsd.pmml_41
import check_pmml_xsd.pmml_40
import check_pmml_xsd.pmml_32


def getmodelinfo(modelpath : str):
    '''
    功能：从输入的pmml和onnx文件中读取模型信息，如输入输出变量
    输入的模型名称为已经储存在/backend/model里的文件，需要带.pmml或.onnx后缀
    Returns:
            model_type:string PMML或ONNX  模型
            algorithm:string  算法 pmml有，onnx不要求，为空字符串
            engine:string  pmml文件为pypmml，onnx文件为onnx Runtime
            input_variate：list 输入变量 为一列表，list中每一元素为一元组，每一元组表示一变量，结构为
                （name:string 变量名称
                data_type:string 变量类型
                value:str 如‘1，2，3’没有为None
                shape:str onnx有，pmml没有，None
                optype:string pmml有，onnx没有，为None
                ）
            predict_variate:list 预测变量 结构同输入变量
    '''
    #返回数据
    model_type=''
    algorithm=''
    engine=''
    input_variate_list=[]
    predict_variate_list=[]
    #判断是哪个模型
    model=re.search(r'....$',modelpath)
    file_path = "./model/" + modelpath
    #对pmml
    if model.group()=="pmml":
        model_type="PMML"
        engine="PyPMML"
        # modelname 需要带.pmml或.onnx后缀
        with open(file_path, encoding='utf-8') as file_obj:
            contents = file_obj.read()
        #匹配使用的模型算法
        model_contents = re.search(r'<.*?modelName.*?>', contents)
        try:
            model_contents = model_contents.group()
            model_type_contents = re.search(r'<(.*?) ', model_contents)
            model_type_contents = model_type_contents.group(1)
            model_function = re.search(r'functionName="(.*?)"', model_contents)
            if model_function != None:
                model_function = model_function.group(1)
                algorithm = model_type_contents + "(" + model_function + ")"
            else:
                model_function = ""
                algorithm = model_type_contents
        except:
            algorithm = ""
        # 匹配输入和预测变量
        input_variate_name = set()
        predict_variate_name = set()
        name_contents = re.search(r'<MiningSchema>[\s\S]*?</MiningSchema>', contents)  # 仅第一组不包括中间变量
        name_contents = name_contents.group()
        pattern = re.compile(r"<MiningField\b.*>")
        name_info_list = pattern.findall(name_contents)
        for name_info in name_info_list:
            usage = re.search(r'\busageType="(.*?)"', name_info)
            if usage!=None:
                usage = usage.group(1)
            else:#缺省，默认输入变量
                usage=''
            name = re.search(r'\bname="(.*?)"', name_info)
            if name!=None:
                name = name.group(1)
            else:
                name=''
            if usage == "predicted" or usage == "target":  # 看pmml版本，4.3以上是target，之前是predicted
                predict_variate_name.add(name)
            else:
                input_variate_name.add(name)
        # 匹配输入变量和预测变量的具体信息
        input_variate_list = []
        predict_variate_list = []
        dict = re.search(r'<DataDictionary[\s\S]*?</DataDictionary>', contents)  # 仅第一组不包括中间变量
        dict = dict.group()
        pattern = re.compile(r"<DataField.*?/>|<DataField[\s\S]*?</DataField>")
        name_info_list = pattern.findall(dict)

        for name_info in name_info_list:
            name = re.search(r'\bname="(.*?)"', name_info)
            if name!=None:
                name=name.group(1)
            else:
                continue
            tmp = {"name": name}
            # 类型
            dataType = re.search(r'\bdataType="(.*?)"', name_info)
            if dataType != None:
                dataType = dataType.group(1)
            else:
                dataType = None
            tmp["data_type"] = dataType
            # 测量
            optype = re.search(r'\boptype="(.*?)"', name_info)
            if optype != None:
                optype = optype.group(1)
            else:
                optype = None
            tmp["optype"] = optype
            # 取值
            value = re.findall(r'\bvalue="(.*?)"', name_info)
            if value!=[]:
                value1=list(map(lambda x: str(x), value))
                value=','.join(value1)
                tmp["value"] = value
            else:
                tmp["value"] = None
            tmp["shape"]=None
            #和savemodel对接
            tmp_tup=(tmp['name'],tmp['data_type'],tmp['value'],tmp['shape'],tmp['optype'])
            #print(tmp_tup)
            if name in input_variate_name:
                input_variate_list.append(tmp_tup)
            if name in predict_variate_name:
                predict_variate_list.append(tmp_tup)

    if model.group() == "onnx":
        model_type = "ONNX"
        engine = "ONNX Runtime"
        onnx_session = onnxruntime.InferenceSession(file_path)
        input_variate_list=[]
        predict_variate_list=[]
        for node in onnx_session.get_inputs():
            tmp={}
            tmp["name"]=node.name
            tmp["data_type"]=node.type
            nshape = node.shape
            nshape=list(map(lambda x: str(x), nshape))
            nshape = ','.join(nshape)
            nshape=nshape.replace(',', '*')
            tmp['shape']=nshape
            tmp["optype"]=None
            tmp["value"]=None
            # 和savemodel对接
            tmp_tup = (tmp['name'], tmp['data_type'], tmp['value'], tmp['shape'], tmp['optype'])
            input_variate_list.append(tmp_tup)
        for node in onnx_session.get_outputs():
            tmp={}
            tmp["name"]=node.name
            tmp["data_type"]=node.type
            nshape = node.shape
            nshape = list(map(lambda x: str(x), nshape))
            nshape = ','.join(nshape)
            nshape = nshape.replace(',', '*')
            tmp["shape"]=nshape
            tmp["optype"] = None
            tmp["value"] = None
            # 和savemodel对接
            tmp_tup = (tmp['name'], tmp['data_type'], tmp['value'], tmp['shape'], tmp['optype'])
            predict_variate_list.append(tmp_tup)
    '''print(model_type)
    print(algorithm)
    print(engine)
    print(input_variate_list)
    print(predict_variate_list)'''
    return {"model_type":model_type,
            "algorithm":algorithm,
            "engine":engine,
            "input_variate":input_variate_list,
            "predict_variate":predict_variate_list}


def checkmodel(user: str, password: str, modeltype: str, modelname: str):
    '''
    Args:
        user: 用户名
        password: 密码
        modeltype: 用户通过表单选择， pmml或onnx
        modelname: 输入的模型名称,模型为已经储存在/backend/model里的文件，需要带.pmml或.onnx后缀

    Returns:
        legal:bool值，True表示模型合法，False表示模型不合法。若模型不合法，getmodelinfo函数返回值可能为空
        error_info:str 在不合法时返回报错，合法时为空字符串
    '''

    valid = False
    error_info = 'model is invalid'
    model = re.search(r'....$', modelname)
    file_path = "./model/" + modelname
    if (modeltype == "pmml") or (modeltype == "PMML"):
        # 验证是否为pmml模型
        if model.group() != "pmml":
            valid = False
            error_info = "model is invalid: not a pmml model"
            return valid, error_info
        #检验是否是合格的xml
        try:
            ET.parse(file_path)
        except Exception as e:
            error_info =e
            valid=False
            return valid,error_info
        #是否符合对应版本的xsd
        #读取版本
        try:
            with open(file_path, encoding='utf-8') as file_obj:
                contents = file_obj.read()
            version = re.search(r'<PMML.*?version="(.*?)"', contents)
            version=version.group(1)
        except Exception:
            error_info = "model is invalid:can't get version"
            valid = False
            return valid, error_info
        #验证对应版本
        if version=="4.4.1":
            try:
                model = check_pmml_xsd.pmml_441.parse(file_path, silence=True)
            except Exception as e:
                error_info = "cannot pass pmml4-4-1.xsd validation"
                valid = False
            else:
                error_info = ""
                valid = True
        elif version=="4.4":
            try:
                model = check_pmml_xsd.pmml_44.parse(file_path, silence=True)
            except Exception as e:
                error_info = "cannot pass pmml4-4.xsd validation"
                valid = False
            else:
                error_info = ""
                valid = True
        elif version=="4.3":
            try:
                model = check_pmml_xsd.pmml_43.parse(file_path, silence=True)
            except Exception as e:
                error_info = "cannot pass pmml4-3.xsd validation"
                valid = False
            else:
                error_info = ""
                valid = True
        elif version=="4.2":
            try:
                model = check_pmml_xsd.pmml_42.parse(file_path, silence=True)
            except Exception as e:
                error_info = "cannot pass pmml4-2.xsd validation"
                valid = False
            else:
                error_info = ""
                valid = True
        elif version=="4.1":
            try:
                model = check_pmml_xsd.pmml_41.parse(file_path, silence=True)
            except Exception as e:
                error_info = "cannot pass pmml4-1.xsd validation"
                valid = False
            else:
                error_info = ""
                valid = True
        elif version=="4.0":
            try:
                model = check_pmml_xsd.pmml_40.parse(file_path, silence=True)
            except Exception as e:
                error_info = "cannot pass pmml4-0.xsd validation"
                valid = False
            else:
                error_info = ""
                valid = True
                #print("haha")
        elif version=="3.2":
            try:
                model = check_pmml_xsd.pmml_32.parse(file_path, silence=True)
            except Exception as e:
                error_info = "cannot pass pmml3-2.xsd validation"
                valid = False
            else:
                error_info = ""
                valid = True
        else:
            # 若version为4.2.1之类无法转成float的且不在枚举范围内的，4.4可验证4.1-4.4，3.2可验证3.0-3.2
            version=version[0]
            if version=='4':
                try:
                    model = check_pmml_xsd.pmml_44.parse(file_path, silence=True)
                except Exception as e:
                    error_info = "cannot pass pmml4-4.xsd validation"
                    valid = False
                else:
                    error_info = ""
                    valid = True
            elif version=='3':
                try:
                    model = check_pmml_xsd.pmml_32.parse(file_path, silence=True)
                except Exception as e:
                    error_info = "cannot pass pmml3-2.xsd validation"
                    valid = False
                else:
                    error_info = ""
                    valid = True
            else:
                #在2.1以前的版本
                error_info = ""
                valid = True
    elif (modeltype=="onnx") or (modeltype=="ONNX"):
        #是否为onnx
        if model.group() !="onnx":
            valid=False
            error_info="model is invalid: not an onnx model"
            return valid,error_info
        #加载
        try:
            model = onnx.load(file_path)
        except:
            error_info=sys.exc_info()
            valid=False
        else:
            #检验有效性
            try:
                onnx.checker.check_model(model)
            except onnx.checker.ValidationError as e:
                error_info = error_info+e
                valid=False
            else:
                valid = True
                error_info=''
    else:#传入的modeltype有问题 仅能接受pmml、onnx和PMML ONNX 查看拼写是否正确
        valid=False
        error_info="model type error(only support pmml or onnx)"

    return valid,error_info

if __name__ == '__main__':
    a,b=checkmodel('haha','haha','pmml',"xgb-iris.pmml")
    print(a)
    print(b)

