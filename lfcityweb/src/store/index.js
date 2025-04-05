import {createStore} from "vuex";
import createPersistedState from "vuex-persistedstate"

const store = createStore({
    plugins: [createPersistedState()],
    state(){
        return {
            user: {},
            cart_count: 0
        }
    },
    getters:{
        getUserInfo(state){
            let now = parseInt(((new Date() - 0) / 1000));
            // 未登录 或者 已过期
            if(state.user.exp === undefined || now > parseInt(state.user.exp)){
                state.user = {};
                localStorage.removeItem("token");
                sessionStorage.removeItem("token");
                return null;
            }
            return state.user;
        }
    },
    mutations:{
        login(state, payload){
            state.user = payload;
        },
        logout(state){
            state.user = {};
            localStorage.removeItem("token");
            sessionStorage.removeItem("token");
        },
        cart_count(state, count){
            state.cart_count = count;
        }
    }
})

export default store;