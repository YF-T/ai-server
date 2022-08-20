 <template>
<!--中间一个模型的信息-->
<div @click = "detail">
  <div id = "bg">
      <p>{{modelname}}</p>
      <p>{{modeltype}}</p>
      <p>{{time}}</p>
      <p>{{op}}</p>
  </div>
</div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import {useStore} from "vuex";


export default defineComponent({
  name: "model_manage_item",
  components:{},
  data(){
    return{
      store: useStore()
    }
  },
  props:['modelname', 'modeltype','time', 'op'],
  methods:{
    detail(){
      this.store.commit('savemodelname',this.modelname);
      this.$router.push('/model_info_manage')
    }

  }



});
</script>

<style scoped>
p{
    text-align:center;
    float:left;
    width:100px;
    height:30px;
    font-size: large;
    color:pink;
    display:inline-block;
  }
#bg{
  display: inline-block;
  background-image: linear-gradient( 135deg, skyblue 10%, lightslategrey 100%);
  outline:solid black thin;
}

</style>