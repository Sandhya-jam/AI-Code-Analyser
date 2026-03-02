import axios from "axios"

const API=axios.create({
    baseURL:"http://localhost:5000",
});

export const analyzeCode=async(code)=>{
    const response=await API.post("/analyze",{code});
    return response.data;
};