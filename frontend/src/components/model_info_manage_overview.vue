<template>
    <div class="context">
        <div class="args">
          <div class="inputblock">
            <label>输入变量</label>
            <span style="white-space:pre">   </span><span class="line"></span>
            <table>
              <tr>
                <th width="30%">字段</th>
                <th width="15%">类型</th>
                <th width="20%">维数</th>
                <th width="35%">取值</th>
              </tr>
              <!-- {% for %} -->
              <tr v-for="inputone in inputlist" :key="inputone">
                <td>{{inputone.name}}</td>
                <td>{{inputone.type}}</td>
                <td>{{inputone.dimension}}</td>
                <td>{{inputone.range}}</td>
                <!-- None没有显示 -->
              </tr>
              <!-- {% endfor %} -->
            </table>
          </div>
          <div class="outputblock">
            <label>目标变量</label>
            <span style="white-space:pre">   </span><span class="line"></span>
            <table>
              <tr>
                <th>字段</th>
                <th>类型</th>
                <th v-if="modeltype==='pmml'">维数</th>
                <th v-else>测量</th>
                <th>取值</th>
              </tr>
              <tr v-for="outputone in outputlist" :key="outputone">
                <td>{{outputone.name}}</td>
                <td>{{outputone.type}}</td>
                <td v-if="modeltype==='pmml'">{{outputone.dimension}}</td>
                <td v-else>{{outputone.optype}}</td>
                <td>{{outputone.range}}</td>
              </tr>
            </table>
          </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';

export default defineComponent({
  name: 'model_info_overview',
  props: {
    msg: String,
  },
  created:function(){
    this.overviewshow();
  },
  data(){
    return {
      inputlist:[],
      outputlist:[],
      store: useStore(),
      modeltype:'',
    }
  },
  methods:{
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
            this.modeltype = res.data.modeltype;
          }
        });
    }
  },
});
</script>

<style scoped>
.context {
    height: 500px;
    width: auto;
    background: #F1F2F6;
}

.args{
  display: flex;
}

label {
  position: relative;
  left:10px;
  font-weight: bold;
  font-size: 30px;
}

.inputblock, .outputblock{
  flex-grow:1;
  display:block;
  margin: 20px;
  height: 400px;
  overflow: auto;
  background: white;
  text-align:left;
  border: 4px solid rgb(179, 191, 231);
  border-radius:10px;
}

table{
  width: 100%;
  font-size:25px;
  background: white;
}

table th{
  background: #FAFAFA;
}
.line {
  display: inline-block;
  padding-top : 3px;
  width: 100%;
  border-top: 1px solid #666666;
}

</style>
