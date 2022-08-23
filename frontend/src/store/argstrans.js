import { createStore } from 'vuex';

export default createStore({
    state: {
        username: "未登录",
        password: "",
        modelname: 'test2',
        webname: '',
        details: [],
        tasks: [],
        correcttime: '',
    },
    mutations: {
        // 保存当前菜单栏的路径
        saveusername(state, username) {
            state.username = username;
        },
        savepassword(state, password) {
            state.password = password;
        },
        savemodelname(state, modelname) {
            state.modelname = modelname;
        },
        savewebname(state, webname) {
            state.webname = webname;
            console.log(webname);
        },

        savetasks(state, tasks) {
            state.tasks = tasks
        },
        savedetail(state, data) {
            state.details.push(data);
        },
        savecorrecttime(state, time) {
            state.correcttime = time;
        }
    }
})