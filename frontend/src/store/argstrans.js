
import { createStore } from 'vuex';

export default createStore({
    state:{
        username: "未登录",
        password: "",
    },
    mutations:{
        // 保存当前菜单栏的路径
        saveusername(state,username){
            state.username = username;
        },
        savepassword(state,password){
            state.password = password;
        },
    }
})