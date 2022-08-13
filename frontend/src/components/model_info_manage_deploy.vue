<template>
    <div class="context">
      <div class="deployblock">
          <div class="infoline">
            <label>部署</label>
            <button @click="pagechange(4)"><span>添加服务</span></button>
            <button><span>添加任务</span></button>
          </div>
          <span style="white-space:pre"></span><span class="line"></span>
          <table>
            <tr>
              <th>名称</th>
              <th>类型</th>
              <th>开始时间</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
            <tr>
              <td>名称</td>
              <td>类型</td>
              <td>开始时间</td>
              <td>状态</td>
              <td>操作</td>
            </tr>
          </table>
      </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'model_info_deploy',
  props: {
    msg: String,
  },
  methods:{
    pagechange(index:number){
      this.$emit('pagechange',index);
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

.deployblock {
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

.line {
  display: inline-block;
  padding-top : 3px;
  width: 100%;
  border-top: 1px solid #666666;
}

table{
  width: 100%;
  background: white;
}

table th{
  background: #FAFAFA;
}

.infoline{
  display: flex;
  width: 100%;
}

label {
  position: relative;
  left:10px;
  font-weight: bold;
  font-size: 30px;
  flex:4;
}

button{
  flex:1;
  position: relative;
  top:8px;
  border: none;
  display: inline-block;
  padding: 10px 30px;
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
