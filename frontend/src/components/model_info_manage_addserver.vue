<template>
  <div class="context">
    <div class="addserverblock">
      <span class="totaltitle"><label class="totalname">部署服务信息填写</label></span>
      <span style="white-space:pre"></span><span class="line"></span>
      <form onsubmit="return false">
        <label class='servername' >部署服务名称</label>
        <input type="text" v-model="name" />
        <label class='servername' >类型</label>
        <input type="text" v-model="webtype"/>
        <label class='servername'>开始时间</label>
        <input type="text" v-model="starttime"/>
        <label class='servername'>状态</label>
        <input type="text" v-model="state"/>
        <label class='servername'>操作</label>
        <input type="text" v-model="operator"/>
        <div class="buttonspace">
          <button type="button" @click="pagechange(3,0)"><span>返回</span></button>
          <button type="submit" @click="pagechange(3,1)"><span>确认</span></button>
        </div>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useStore } from 'vuex';

export default defineComponent({
  name: 'model_info_addserver',
  props: {
    msg: String,
  },
  data(){
    return {
      store: useStore(),
      name:'',
      webtype:'',
      starttime:'',
      state:'',
      operator:'',
    }
  },
  methods:{
    pagechange(index:number,button:number){
      if(button==0){
        this.$emit('pagechange',index);
      }
      else{
        if(this.name!='' &&
        this.webtype!='' &&
        this.starttime!='' &&
        this.state!='' &&
        this.operator!='' ){
          this.store.commit('savewebinfo',{
            name :this.name ,
            webtype : this.webtype,
            starttime: this.starttime ,
            state : this.state ,
            operator:this.operator ,
            });
          this.$emit('pagechange',index);
        }
      }
    },
  }
});
</script>

<style scoped>
.context {
    height: 500px;
    width: auto;
    background: #F1F2F6;
}

.addserverblock {
  position: relative;
  display:block;
  top:20px;
  margin: 0px 20px;
  height: 400px;
  overflow: auto;
  background: white;
  text-align:left;
  border: 4px solid rgb(179, 191, 231);
  border-radius:10px;
}
span[class='totaltitle']{
  display: inline-block;
  width: 100%;
  text-align: center;
}
label[class='totalname'] {
  font-weight: bold;
  font-size: 30px;
}
.line {
  display: inline-block;
  padding-top : 3px;
  width: 100%;
  border-top: 1px solid #666666;
}
label[class='servername']{
  left:10px;
  font-size: 20px;
  font-weight: lighter;
}
form{
  display: block;
  margin: 20px 50px;
}

input {
  font-size: 20px;
  width: 100%;
  margin-top: 10px;
}

.buttonspace{
  display: flex;
  margin: 30px 0px;
}

button{
  flex:1;
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

button:hover{
  box-shadow: inset -2px -2px 8px rgba(255, 255, 255, 1),inset -2px -2px 12px rgba(255, 255, 255, 0.5),
            inset 2px 2px 4px rgba(255, 255, 255, 0.5),inset 2px 2px 8px rgba(0, 0, 0, 0.15);
}

button:hover:span{
  display: inline-block;
  transform: scale(0.98);
}
</style>
