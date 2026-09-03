import axios from "axios"

const API=axios.create({
    baseURL:"http://localhost:5000/api",
});

API.interceptors.request.use((req)=>{
    const token=localStorage.getItem("token");
    if(token){
        req.headers.Authorization=`Bearer ${token}`;
    }
    return req;
});

export const signup=async(userData)=>{
    const res=await API.post("/auth/signup",userData);
    return res.data;
}

export const login=async(userData)=>{
    const res=await API.post("/auth/login",userData);
    return res.data;
};

export const analyzeCode=async(code)=>{
    const response=await API.post("/code/analyze",{code});
    return response.data;
};

export const fixCode=async(code)=>{
    const response=await API.post("/code/fix",{code});
    return response.data
};

export const getHistory=async(params={})=>{
    const response=await API.get('/code/history',{params});
    return response.data;
};

export const getHistoryById=async(id)=>{
    const response=await API.get(`/code/history/${id}`);
    return response.data;
}

export const getHistoryStats=async()=>{
    const response=await API.get('/code/history/stats');
    return response.data;
}

export default API;