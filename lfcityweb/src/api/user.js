import {reactive} from "vue";
import http from "../utils/http.js";

const user = reactive({
    username: "",
    password: "",
    re_password: "",
    phone: "",
    code: "",

    order_list: [],
    status_choices: [],
    order_count: 0,
    order_status: -1,
    order_size: 5,
    order_page: 1,

    course_list: [],
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
    },
    get_order_list(token){
        let params = {
            page: this.order_page,
            size: this.order_size,
            status: this.order_status,
        }
        return http.get("/order/list/", {
            params,
            headers: {
                Authorization: "jwt " + token
            }
        })
    },
    get_order_status_choices(token){
        return http.get("/order/status/", {
            headers: {
                Authorization: "jwt " + token
            }
        })
    },
    cancel_order(token, order_number){
        return http.post(`/order/cancel/${order_number}/`, {}, {
            headers: {
                Authorization: "jwt " + token
            }
        })
    }
});

export default user;