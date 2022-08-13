<template>
    <div class="context">
        <div class="datatran">
          <div class="inputtest">
            <div class="infoline">
              <label>输入变量</label>
              <a href="">JSON</a>
            </div>
            <span style="white-space:pre"></span><span class="line"></span>
            <form name="argsform">
              <!-- 需要知道变量名和变量类型，变量数量-->
              <!-- {% for %} -->
              <label class="argsname">sepal length (cm):</label><br/>
              <input type="number"/>
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
                <button type="submit" class="truck-button" @click="pagechange(2)">
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
          </div>
          <div class="outputtest">
            <label>输出变量</label>
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

export default defineComponent({
  name: 'model_info_test',
  props: {
    msg: String,
  },
  mounted(){
    this.truckanimationadd();
    this.trashanimationadd();
  },
  methods:{
    pagechange(index:number){
      this.$emit('pagechange',index);
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
a{
  flex:1;
  text-decoration: none;
  line-height: 45px;
}

label[class='argsname']{
  font-size: 20px;
  font-weight: lighter;
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
  width: 100%;
  margin-top: 10px;
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


</style>
