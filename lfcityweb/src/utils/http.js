import axios from "axios";


const http = axios.create({
    baseURL: "http://api.lfcity.cn:8000/",
    withCredentials: false,
});

http.interceptors.request.use(
    config => {
        // console.log(config);
        return config;
    },
    error => {
        console.log("request error: ", error.message);
        return error;
    }
);

http.interceptors.response.use(
    response => {
        // console.log(config);
        return response;
    },
    error => {
        console.log("response error: ", error.message);
        return Promise.reject(error);
    }
);

export default http;