import http from "../utils/http.js"
import {reactive} from "vue";


const nav = reactive({
    header_list: [],
    footer_list: [],
    get_header_list(){
        http.get("/home/header/").then(response=>{
            this.header_list = response.data;
        })
    },
    get_footer_list(){
        http.get("/home/footer/").then(response=>{
            this.footer_list = response.data;
        })
    }
})

export default nav;