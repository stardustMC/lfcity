import {reactive} from "vue";
import http from "../utils/http.js";

const user = reactive({
    username: "",
    password: "",
    re_password: "",
    phone: "",
    code: "",
    login(){
        return http.post("/user/login/", {
            username: this.username,
            password: this.password,
        })
    },
    register(){
        return http.post("/user/register/", {
            username: this.username,
            password: this.password,
            re_password: this.re_password,
            phone: this.phone,
            code: this.code
        })
    }
});

export default user;