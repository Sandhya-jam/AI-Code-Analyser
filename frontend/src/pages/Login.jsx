import { useState } from "react";
import { login } from "../services/api";
import { useNavigate } from "react-router-dom";

export const Login=()=>{
  const navigate=useNavigate();

  const [form,setForm]=useState({
    email:"",
    password:""
  });

  async function handleSubmit(e){
    e.preventDefault();
    console.log(form)
    try {
        const data=await login(form);
        localStorage.setItem("token",data.token);
        navigate("/analyzer");
    } catch (error) {
        console.error(error.response.data)
        alert("Login failed")
    }
  }

  return(
    <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white">
        <form onSubmit={handleSubmit} className="bg-gray-800 p-8 rounded-xl w-96">
            <h2 className="text-2xl font-bold mb-6 text-center">
                Login
            </h2>
            <input 
            type="email"
            placeholder="email"
            className="w-full p-2 mb-4 bg-gray-700 rounded"
            onChange={(e)=>setForm({...form,email:e.target.value})} 
            />
            <input 
            type="password"
            placeholder="Password"
            className="w-full p-2 mb-4 bg-gray-700 rounded"
            onChange={(e)=>setForm({...form,password:e.target.value})} 
            />
            <button className="w-full bg-blue-500 p-2 rounded hover:bg-blue-600">
                Login
            </button>
            <p className="text-sm mt-4 text-center">
                Don't have an account? <span
                className="text-blue-400 cursor-pointer"
                onClick={()=>navigate("/signup")}
                >SignUp</span>
            </p>
        </form>
    </div>
  )
}