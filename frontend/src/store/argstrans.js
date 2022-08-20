
import { createStore } from 'vuex';

export default createStore({
    state:{
        username: "未登录",
        password: "",
        modelname:'test2',
    },
    mutations:{
        // 保存当前菜单栏的路径
        saveusername(state,username){
            state.username = username;
        },
        savepassword(state,password){
            state.password = password;
        },
        savemodelname(state,modelname){
            state.modelname=modelname;
        },        
    }
})