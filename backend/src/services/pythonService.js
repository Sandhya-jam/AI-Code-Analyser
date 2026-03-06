import axios from 'axios';

export const analyzeCode=async(code)=>{
    const response=await axios.post(
        'http://localhost:8000/analyze',
        {source:code}
    );
    return response.data;
};

export const fixCode=async(code)=>{
    const response=await axios.post(
        'http://localhost:8000/fix',
        {source:code}
    );
    return response.data
}