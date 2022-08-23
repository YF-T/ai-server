 <template>
<!--中间一个模型的信息-->
<div>
  <div id = "bg">
      <p @click = "detail" style="cursor: pointer;">{{modelname}}</p>
      <p @click = "detail" style="cursor: pointer;">{{modeltype}}</p>
      <p @click = "detail" style="cursor: pointer;">{{time}}</p>
      <p><button class="oper" @click="deletemodel" style="cursor: pointer;"><span>删除</span></button></p>
  </div>
</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import {useStore} from "vuex";
import axios from 'axios';

export default defineComponent({
  name: "model_manage_item",
  components:{},
  data(){
    return{
      store: useStore()
    }
  },
  props:['modelname', 'modeltype','time'],
  methods:{
    detail(){
      this.store.commit('savemodelname',this.modelname);
      this.$router.push('/model_info_manage')
    },
    deletemodel(){
      let param=new FormData();
      param.append('user',this.store.state.username);
      param.append('password',this.store.state.password);
      param.append('modelname',this.modelname);
      var path = 'http://127.0.0.1:5000/deletemodel';
      axios
      .post(path,param,{headers:{"Content-Type":"application/x-www-form-urlencoded"}})
      .then(res=> {
          if(res.data.status === 'success'){
            this.$emit('itemdelete');
          }
          else if(res.data.status==='model not found'){
            alert("找不到该名称模型");
          }
          else{
            if(res.data.status==="user not found"){
              alert("用户不存在");
            }
            else if(res.data.status === 'invalid password'){
              alert("密码错误！")
            }
          }
        }
        );
    }
  }
});
</script>

<style scoped>
p{
    text-align:center;
    float: left;
    width:200px;
    height:30px;
    font-size: 20px;
    line-height: 30px;
    color: black;
    display:inline-block;
  }
#bg{
  margin-top: 0px;
  display: inline-block;
  background-color: white;
  border: 4px solid rgb(179, 191, 231)
}
button[class='oper']{
  width: 50%;
  padding: 8px 10px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 0px 2px;
  -webkit-transition-duration: 0.4s; /* Safari */
  transition-duration: 0.4s;
  cursor: pointer;
  background-color: white; 
  color: black; 
  border: 2px solid #90EE90;
}

button[class='oper']:hover {
    background-color: #87CEFA;
    color: white;
}
</style>