<template>
    <div class="context">
        <div class="datatran">
          <div class="inputtest">
            <div class="infoline">
              <label>输入</label>
              <button class='inputtype' @click="input(1)"><span>表单输入</span></button>
              <button class='inputtype' @click="input(0)"><span>JSON输入</span></button>
            </div>
            <span style="white-space:pre"></span><span class="line"></span>
            <form name="argsform" v-if="inputtypeindex===1">
              <!-- 需要知道变量名和变量类型，变量数量-->
              <!-- {% for %} -->
              <div v-for="(inputone,i) in inputlist" :key="inputone">
                <label class="argsname">{{inputone.name}}:</label>
                <label class="radiolabel">输入方式选择：</label>
                  <label class="radiolabel"><input v-model=nofileshow[i] type="radio" :name=inputone.name value='1' @click="inputtypeshow(i,1)"/>文本框输入</label>
                  <label class="radiolabel"><input v-model=nofileshow[i] type="radio" checked :name=inputone.name value='0' @click="inputtypeshow(i,0)"/>文件输入</label><br/>
                <div class="parent" v-if="nofileshow[i]==='1'">
                  <div class="dummy" name='point'></div>
                  <textarea class="textarea" v-on:input="test(i)" v-model="valuelist[i]"></textarea>
                </div>
                <input type="file" v-else/>
              </div>
              <!-- {% endfor %} -->
              <!-- <input type="button" value="清空" onclick="argsform.reset()"/> -->
              <div class="trashbutton">
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
              <div class="truckbuttonflex">
                <button type="submit" class="truck-button" @click="pagechange(2,1)">
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
            <form v-else>
              <div id="parent">
                <div id="dummy"></div>
                <textarea id="textarea" oninput="document.getElementById('dummy').textContent = this.value"></textarea>
              </div>
              <button type="submit" class='jsonsubmit' @click="pagechange(2,0)"><span>提交</span></button>
            </form>
          </div>
          <div class="outputtest">
            <label>输出</label>
            <span style="white-space:pre"></span><span class="line"></span>
            <!-- {% for %} -->
            <div class="codeline">
              <span class="order"> 1 </span>
              <span class="codeshow"> {} </span>
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
      outputlist:[],
      store: useStore(),
      valuelist:[],
      nofileshow:[],
      inputtypeindex:1,
    }
  },
  methods:{
    inputtypeshow(i:number,index:number){
      // this.nofileshow[i] = index; 
    },
    input(index:number){
      this.inputtypeindex = index;
    },
    test(i:number){
      let s1=document.getElementsByName("point")[i];
      s1.textContent = this.valuelist[i];
    },
    pagechange(index:number,inputtypeindex:number){
      this.$emit('pagechange',index);
      this.inputtypeindex = inputtypeindex;
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
          if(res.data.status==='success'){
            this.inputlist = res.data.input;
            this.outputlist = res.data.output;
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
  overflow: auto;
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
  display: flex;
  height: 1em;
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
  margin: 10px 0px;
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
  flex:2;
  position: relative;
  top:8px;
  border: none;
  display: inline-block;
  padding: 10px 30px;
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
  transform: scale(0.98);
}

.jsonsubmit{
  position: relative;
  top:8px;
  border: none;
  display: flex;
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
</style>
