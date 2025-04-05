import {computed, reactive} from "vue";
import http from "../utils/http.js";


const cart = reactive({
    course_list: [],
    get_cart_list(token){
        return http.get("/cart/", {
            headers: {
                Authorization: "jwt " + token
            }
        })
    },
    total_price: computed(()=>{
        let price = 0.0;
        cart.selected_course_list.forEach(course=>{
            if(course.discount.price) price += course.discount.price;
            else price += course.price;
        })
        return price;
    }),
    selected_course_list: computed(()=>{
        return cart.course_list.filter(course=>course.selected === 1);
    }),
    all_selected: computed(()=>{
        return cart.selected_course_list.length === cart.course_list.length;
    }),
    add_course(token, course_id){
        return http.post("/cart/", {
            course_id: course_id
        }, {
            headers: {
                Authorization: "jwt " + token
            }
        });
    },
    get_course_list(token){
        return http.get("/cart/", {
            headers: {
                Authorization: "jwt " + token
            }
        })
    },
    alter_course_select(token, course_id, selected){
        return http.put("/cart/", {
            course_id: course_id,
            selected: selected,
        }, {
            headers: {
                Authorization: "jwt " + token
            }
        })
    },
    delete_course(token, course_id){
        return http.delete("/cart/", {
            headers: {
                Authorization: "jwt " + token,
            },
            params:{
                course_id
            }
        });
    }
})

export default cart;