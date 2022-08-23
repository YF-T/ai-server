<template>
    <div class="context">
        <div class="datatran">
          <div class="inputtest">
            <div class="infoline">
              <label>输入</label>
              <button class='inputtype' @click="input(2)"><span>文件输入</span></button>
              <button class='inputtype' @click="input(1)"><span>表单输入</span></button>
              <button class='inputtype' @click="input(0)"><span>JSON输入</span></button>
            </div>
            <span style="white-space:pre"></span><span class="line"></span>
            <div v-show="inputtypeindex===2">
              <div class="content">
                <div class="drag-area" @dragover="fileDragover" @drop="fileDrop">
                  <div v-if="fileName" class="file-name">{{ fileName }}</div>
                  <div v-else class="uploader-tips">
                    <span class="upfile">将文件拖拽至此，或</span>
                    <label class="upfile" for="fileInput" style="color: #11A8FF; cursor: pointer">点此上传</label>
                  </div>
                </div>
              </div>
          
              <div class="footer">
                <input type="file" id="fileInput" @change="chooseUploadFile" style="display: none;">
                <label class="jsonsubmit" for="fileInput" v-if="fileName" style="font-size:20px;width:200px;cursor: pointer"><span>重新选择文件</span></label>
                <button class='jsonsubmit' @click="uploadOk"><span>提交</span></button>
              </div>
            </div>
            <form name="argsform" v-show="inputtypeindex===1" onsubmit="return false">
              <!-- 需要知道变量名和变量类型，变量数量-->
              <!-- {% for %} -->
              <div v-for="(inputone,i) in inputlist" :key="inputone">
                <label class="argsname">{{inputnamelist[i]}}:</label>
                <label class="radiolabel">输入方式选择：</label>
                  <label class="radiolabel"><input v-model=nofileshow[i] type="radio" :name=inputone.name value='1' />文本框输入</label>
                  <label class="radiolabel"><input v-model=nofileshow[i] type="radio" :name=inputone.name value='0' />文件输入</label><br/>
                <input type="file" v-if="nofileshow[i]==='0'" value="" accept="image/png, image/jpeg, image/gif, image/jpg" @change="uploadImg($event,i)"/>
                <div class="parent" v-else>
                  <div class="dummy" name='point'></div>
                  <textarea class="textarea" v-on:input="test(i)" v-model="valuelist[i]"></textarea>
                </div>
              </div>
              <!-- {% endfor %} -->
              <!-- <input type="button" value="清空" onclick="argsform.reset()"/> -->
              <div class="trashbutton" @click="deletedata">
                <button type="reset" class="button" onclick="argsform.reset()" >
                  <div class="trash">
                      <div class="top">
                          <div class="paper"></div>
                      </div>
                      <div class="box"></div>
                      <div class="check">
                          <svg viewBox="0 0 8 6">
                              <polyline points="1 3.4 2.71428571 5 7 1"></polyline>
                          </svg>
                      </div>
                  </div>
                  <span>Delete Item</span>
                </button>
              </div>
              <!-- <input type="reset" value="清空"/> -->
              <!-- <input type="submit" @click="pagechange(2)"/> -->
              <div class="truckbuttonflex" @click="worduploaddata()">
                <button type="submit" class="truck-button">
                    <span class="default">Complete Order</span>
                    <span class="success">
                        Order Placed
                        <svg viewbox="0 0 12 10">
                            <polyline points="1.5 6 4.5 9 10.5 1"></polyline>
                        </svg>
                    </span>
                    <div class="truck">
                        <div class="wheel"></div>
                        <div class="back"></div>
                        <div class="front"></div>
                        <div class="box"></div>
                    </div>
                </button>
              </div>
            </form>
            <form v-show="inputtypeindex===0" onsubmit="return false">
              <div id="parent">
                <div id="dummy"></div>
                <textarea id="textarea" oninput="document.getElementById('dummy').textContent = this.value" v-model="jsoninput"></textarea>
              </div>
              <button type="submit" class='jsonsubmit' @click="jsonuploaddata()"><span>提交</span></button>
            </form>
          </div>
          <div class="outputtest">
            <label>输出</label>
            <span style="white-space:pre"></span><span class="line"></span>
            <!-- {% for %} -->
            <div class="codeline" v-show="outputshowindex===0">
              <span style="font-size:3em">暂无结果显示</span>
            </div>

            <div class="codeline" v-show="outputshowindex===1">
              <span class="codeshow"> {</span>
              <span class="codeshow" v-for="(value,key) in output" :key="key"> " {{key}} " : {{value}} , </span>
              <span class="codeshow"> }</span>
            </div>

            <div class="codeline" v-show="outputshowindex===2">
              <span class="codeshow"> {</span>
              <span class="codeshow">{{output}}</span>
              <span class="codeshow"> }</span>
            </div>
            <!-- {% endfor %} -->
          </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { gsap } from "gsap";
import { useStore } from 'vuex';
import axios from 'axios';


export default defineComponent({
  name: 'model_info_test',
  props: {
    msg: String,
  },
  created:function(){
    this.overviewshow();
  },
  mounted(){
    this.truckanimationadd();
    this.trashanimationadd();
  },
  data(){
    return {
      inputlist:[],
      output:'',
      store: useStore(),
      valuelist:[],
      filebaselist:new Array(),
      nofileshow:[],
      inputtypeindex:1,
      fileName: '',
      batchFile: '',
      jsoninput:'',
      inputnamelist:new Array(),
      outputshowindex: 0,
    }
  },
  methods:{
    deletedata(){
      this.filebaselist = new Array();
    },
    uploadImg:function(e:any,index:number){
        var file = e.target.files[0]
        if (!/\.(jpg|JPG)$/.test(e.target.value)) {
            alert('目前只支持jpg文件');
            return false;
        }
        var reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onload = (e) => {
            if(e.target){
              this.filebaselist[index] = e.target.result;
            }
        }
    },
    MapTOJson(m:any){
       var str = '{\n';
      var i = 1;
      m.forEach(function (item:any, key:string, mapObj:any) {
        if(mapObj.size == i){
          str += '"'+ key+'":"'+ item +'"\n';
        }else{
          str += '"'+ key+'":"'+ item + '",\n';
        }
        i++;
      });
      str +='}';
      return str;
    },
    worduploaddata(){
      let param=new FormData();
      param.append('user',this.store.state.username);
      param.append('password',this.store.state.password);
      param.append('modelname',this.store.state.modelname);
      
      let filetypecontent = new Map();
      let inputcontent = new Map();
      for (let index = 0; index < this.inputlist.length; index++){
        if(this.nofileshow[index]==0){
          if(this.filebaselist[index]=='') return;
          inputcontent.set(this.inputnamelist[index],this.filebaselist[index]);
          filetypecontent.set(this.inputnamelist[index],"jpgbase64");
        }
        else{
          if(this.valuelist[index]=='') return;
          inputcontent.set(this.inputnamelist[index],this.valuelist[index]);
          filetypecontent.set(this.inputnamelist[index],"none");
        }
      }
      var content = this.MapTOJson(inputcontent);
      var filetype = this.MapTOJson(filetypecontent);
      console.log(content);
      console.log(filetype);
      param.append("input",content);
      param.append("filetype",filetype);
      console.log("wai")
      var path = 'http://127.0.0.1:5000/testmodel_test';
      axios
        .post(path,param,{headers:{"Content-Type":"application/x-www-form-urlencoded"}})
        .then(res=> {
          if(res.data.status=='success'){
            this.output=res.data.output;
            if(res.data.return_type=='dict')
              this.outputshowindex = 1;
            else if(res.data.return_type == 'str')
              this.outputshowindex = 2;
            console.log(res.data.output);
          }
          else{
            this.outputshowindex = 0;
            if(res.data.status== 'user not found' )
              alert("用户不存在");
            else if(res.data.status=='invalid password' )
              alert("密码错误");
            else if(res.data.status=='invalid input')
              alert("输入不合法");
            else if(res.data.status== 'model not found' )
              alert("未找到模型");
            else if(res.data.status=='runtime error')
              alert("模型运行出错")
          }
        }
        );
      
    },
    chooseUploadFile (e:any) {
      const file = e.target.files.item(0)
      if (!file) return
      this.batchFile = file
      this.fileName = file.name
      // 清空，防止上传后再上传没有反应
      e.target.value = ''
    },
    // 拖拽上传
    fileDragover (e:any) {
      e.preventDefault()
    },
    fileDrop (e:any) {
      e.preventDefault()
      const file = e.dataTransfer.files[0] // 获取到第一个上传的文件对象
      if (!file) return
      this.batchFile = file
      this.fileName = file.name
    },
    // 提交
    uploadOk () {
      if (this.batchFile === '') {
        return alert('请选择要上传的文件')
      }
      let index = this.fileName.lastIndexOf('.');
      let fileType = this.fileName.substring(index+1, this.fileName.length); //index是点的位置。点的位置加1再到结尾
      if (fileType!='txt'&&fileType!="csv"&&fileType!="jpg"){
        return alert("不支持当前文件类型")
      }
      let param=new FormData();
      param.append('user',this.store.state.username);
      param.append('password',this.store.state.password);
      param.append('modelname',this.store.state.modelname);
      param.append("filetype",fileType);
      param.append('input', this.batchFile);
      console.log("22222222222222")
      var path = 'http://127.0.0.1:5000/testmodel_test';
      axios
        .post(path,param,{headers:{"Content-Type":"application/x-www-form-urlencoded"}})
        .then(res=> {
          console.log("333333333333333")
          if(res.data.status=='success'){
            this.output=res.data.output;
            if(res.data.return_type=='dict')
              this.outputshowindex = 1;
            else if(res.data.return_type == 'str')
              this.outputshowindex = 2;
          }
          else{
            this.outputshowindex = 0;
            if(res.data.status== 'user not found' )
              alert("用户不存在");
            else if(res.data.status=='invalid password' )
              alert("密码错误");
            else if(res.data.status=='invalid input')
              alert("输入不合法");
            else if(res.data.status== 'model not found' )
              alert("未找到模型");
            else if(res.data.status=='runtime error')
              alert("模型运行出错")
          }
        });
      //todo
      // ajax
    },
    input(index:number){
      this.inputtypeindex = index;
    },
    test(i:number){
      let s1=document.getElementsByName("point")[i];
      s1.textContent = this.valuelist[i];
    },
    jsonuploaddata(){
      let param=new FormData();
      param.append('user',this.store.state.username);
      param.append('password',this.store.state.password);
      param.append('modelname',this.store.state.modelname);
      param.append("filetype",'none');
      param.append("input",this.jsoninput);
      var path = 'http://127.0.0.1:5000/testmodel_test';
      axios
        .post(path,param,{headers:{"Content-Type":"application/x-www-form-urlencoded"}})
        .then(res=> {
          if(res.data.status=='success'){
            this.output=res.data.output;
            if(res.data.return_type=='dict')
              this.outputshowindex = 1;
            else if(res.data.return_type == 'str')
              this.outputshowindex = 2;
          }
          else{
            this.outputshowindex = 0;
            if(res.data.status== 'user not found' )
              alert("用户不存在");
            else if(res.data.status=='invalid password' )
              alert("密码错误");
            else if(res.data.status=='invalid input')
              alert("输入不合法");
            else if(res.data.status== 'model not found' )
              alert("未找到模型");
          }
        });
    },
    overviewshow(){
      let param=new FormData();
      param.append('user',this.store.state.username);
      param.append('password',this.store.state.password);
      param.append('modelname',this.store.state.modelname);
      var path = 'http://127.0.0.1:5000/getmodelinfo';
      axios
        .post(path,param,{headers:{"Content-Type":"application/x-www-form-urlencoded"}})
        .then(res=> {
          console.log("参数名称");
          if(res.data.status==='success'){
            console.log("test");
            for (let index = 0; index < res.data.input.length; index++){
              this.inputnamelist[index] = res.data.input[index].name;
              console.log(this.inputnamelist[index]);
            }
            this.inputlist = res.data.input;
          }
        });
    },
    truckanimationadd(){
          document.querySelectorAll('.truck-button').forEach(button => {
            button.addEventListener('click', e => {

                e.preventDefault();

                let box = button.querySelector('.box'),
                    truck = button.querySelector('.truck');
                
                if (!button.classList.contains('done')) {

                    if (!button.classList.contains('animation')) {

                        button.classList.add('animation');

                        gsap.to(button, {
                            '--box-s': 1,
                            '--box-o': 1,
                            duration: .3,
                            delay: .5
                        });

                        gsap.to(box, {
                            x: 0,
                            duration: .4,
                            delay: .7
                        });

                        gsap.to(button, {
                            '--hx': -5,
                            '--bx': 50,
                            duration: .18,
                            delay: .92
                        });

                        gsap.to(box, {
                            y: 0,
                            duration: .1,
                            delay: 1.15
                        });

                        gsap.set(button, {
                            '--truck-y': 0,
                            '--truck-y-n': -26
                        });

                        gsap.to(button, {
                            '--truck-y': 1,
                            '--truck-y-n': -25,
                            duration: .2,
                            delay: 1.25,
                            onComplete() {
                                gsap.timeline({
                                    onComplete() {
                                        button.classList.add('done');
                                        setTimeout(function() {
                                          button.classList.remove('animation', 'done');
                                          gsap.set(truck, {
                                              x: 4
                                          });
                                          gsap.set(button, {
                                              '--progress': 0,
                                              '--hx': 0,
                                              '--bx': 0,
                                              '--box-s': .5,
                                              '--box-o': 0,
                                              '--truck-y': 0,
                                              '--truck-y-n': -26
                                          });
                                          gsap.set(box, {
                                              x: -24,
                                              y: -6
                                          });
                                        }, 2000)
                                    }
                                }).to(truck, {
                                    x: 0,
                                    duration: .4
                                }).to(truck, {
                                    x: 40,
                                    duration: 1
                                }).to(truck, {
                                    x: 20,
                                    duration: .6
                                }).to(truck, {
                                    x: 96,
                                    duration: .4
                                });
                                gsap.to(button, {
                                    '--progress': 1,
                                    duration: 2.4,
                                    ease: "power2.in"
                                });
                            }
                        });

                    }

                }
            });
        });
    },
    trashanimationadd(){
      document.querySelectorAll('.button').forEach(button => button.addEventListener('click', e => {
            if (!button.classList.contains('delete')) {
                button.classList.add('delete');
                setTimeout(() => button.classList.remove('delete'), 3200);
            }
            e.preventDefault();
        }));
    }
  }
});
</script>

<style scoped>

@import "../static/css/truck.css";
@import "../static/css/index.css";
textarea{
  resize: none;
  width: 400px;
  min-height: 20px;
  max-height: 300px;
  line-height: 24px;
  overflow-y: hidden;

}
.context {
    height: 500px;
    width: auto;
    background: #F1F2F6;
}

.datatran{
  display: flex;
  
}
.inputtest, .outputtest{
  flex: 1;
  display:block;
  margin: 20px;
  height: 400px;
  overflow-y: auto;
  overflow-x: hidden;
  background: white;
  text-align:left;
  border: 4px solid rgb(179, 191, 231);
  border-radius:10px;
}

.infoline {
  display: flex;
  width: 100%;
}
.line {
  display: inline-block;
  padding-top : 3px;
  width: 100%;
  border-top: 1px solid #666666;
}

label {
  position: relative;
  left:10px;
  font-weight: bold;
  font-size: 30px;
}

.infoline label{
  flex:5;
}
/* 修改为相对位置 */

label[class='argsname']{
  font-size: 20px;
  font-weight: lighter;
}

label[class="radiolabel"]{
  font-size: 15px;
}

form{
  display: block;
  margin: 20px 50px;
}

div[class="trashbutton"],div[class="truckbuttonflex"]{
  display: flex;
  justify-content: center;
}

input {
  font-size: 20px;
  margin: 10px 0px 0px 30px;
}

div[class='codeline']{
  position: relative;
  left:20px;
}

span[class='order']{
  display: block;
  width: 40px;
  text-align: center;
  margin: 10px 10px;
  font-weight: bold;
}

span[class='codeshow']{
  display: block;
  margin: 10px 20px 10px 0px;
  line-height: 1em;
}

.parent {
  width: 500px;
  font: 20px monospace;
  position: relative;
  max-height: 120px;
  word-break:break-all;
}
.dummy {
  padding: 2px;
  border: 1px solid;
  visibility: hidden;
  white-space: pre-wrap;
  overflow-y:auto;
}
.dummy::after {
  content: " ";
}
.textarea {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  resize: none;
  width: 100%;
  font: inherit;
  overflow-y:auto;
}

.inputtype{
  flex:3.5;
  position: relative;
  top:8px;
  border: none;
  display: inline-block;
  padding: 10px 15px;
  margin: 0px 20px;
  text-transform: uppercase;
  font-weight: 500;
  letter-spacing: 2px;
  color:#5a94a2;
  border-radius: 40px;
  box-shadow: -2px -2px 8px rgba(255, 255, 255, 1),-2px -2px 12px rgba(255, 255, 255, 0.5),
            inset 2px 2px 4px rgba(255, 255, 255, 0.5),2px 2px 8px rgba(0, 0, 0, 0.15);
}

.inputtype:hover{
  box-shadow: inset -2px -2px 8px rgba(255, 255, 255, 1),inset -2px -2px 12px rgba(255, 255, 255, 0.5),
            inset 2px 2px 4px rgba(255, 255, 255, 0.5),inset 2px 2px 8px rgba(0, 0, 0, 0.15);
}

.inputtype:hover:span{
  display: inline-block;
  font-size:30px;
  transform: scale(0.98);
}

.jsonsubmit{
  position: relative;
  top:2px;
  border: none;
  display: flex;
  width: 100px;
  justify-content: center;
  padding: 10px 30px;
  margin: 20px auto;
  text-transform: uppercase;
  font-weight: 500;
  letter-spacing: 2px;
  color:#5a94a2;
  border-radius: 40px;
  box-shadow: -2px -2px 8px rgba(255, 255, 255, 1),-2px -2px 12px rgba(255, 255, 255, 0.5),
            inset 2px 2px 4px rgba(255, 255, 255, 0.5),2px 2px 8px rgba(0, 0, 0, 0.15);
}

.jsonsubmit:hover{
  box-shadow: inset -2px -2px 8px rgba(255, 255, 255, 1),inset -2px -2px 12px rgba(255, 255, 255, 0.5),
            inset 2px 2px 4px rgba(255, 255, 255, 0.5),inset 2px 2px 8px rgba(0, 0, 0, 0.15);
}

.jsonsubmit:hover:span{
  display: inline-block;
  transform: scale(0.98);
}

#parent {
  width: 600px;
  min-height: 120px;
  max-height: 180px;
  font: 20px monospace;
  word-break:break-all;
  position: relative;
}
#dummy {
  padding: 2px;
  border: 1px solid;
  visibility: hidden;
  white-space: pre-wrap;
}
#dummy::after {
  content: " ";
}
#textarea {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  resize: none;
  width: 100%;
  font: inherit;
  overflow-y:auto;
}
form[class="fileinput"]{
  text-align: center;
}
.drag-area {
  height: 200px;
  width: 300px;
  border: dashed 1px gray;
  margin-bottom: 10px;
  color: #777;
}
.uploader-tips {
  text-align: center;
  height: 200px;
  line-height: 200px;
}
.file-name {
  text-align: center;
  height: 200px;
  line-height: 200px;
}
div[class="content"]{
  display: flex;
  justify-content: center;
}
div[class="footer"]{
  display: flex;
  justify-content: center;
  flex-direction: column;
  text-align: center;
}
.upfile{
  font-size: 20px;
}
</style>
