import { useState } from "react";
import { signup } from "../services/api";
import { useNavigate } from "react-router-dom";

export const SignUp=()=>{
   const navigate=useNavigate();
   const [form,setForm]=useState({
    name:"",
    email:"",
    password:"",
   });
   const [confirmPass,SetConfirmPass]=useState("");

   async function handleSubmit(e) {
      e.preventDefault();
      if(form.password!==confirmPass){
         alert("Passwords did'nt matched");
      }
      else{
        try {
        const data=await signup(form)
        localStorage.setItem("token",data.token);
        navigate("/analyzer");
      } catch (error) {
        console.error(err);
        alert("SignUp Failed");
      }
      }
   }

   return(
    <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white">
        <form onSubmit={handleSubmit} className="bg-gray-800 p-8 rounded-xl w-96">
            <h2 className="text-2xl font-bold mb-6 text-center">
                Create Account
            </h2>
            <input 
            type="text" 
            placeholder="Name"
            className="w-full p-2 mb-4 bg-gray-700 rounded"
            onChange={(e)=>setForm({...form,name:e.target.value})}
            />
            <input 
            type="email" 
            placeholder="Email"
            className="w-full p-2 mb-4 bg-gray-700 rounded"
            onChange={(e)=>setForm({...form,email:e.target.value})}
            />
            <input 
            type="password" 
            placeholder="password"
            className="w-full p-2 mb-4 bg-gray-700 rounded"
            onChange={(e)=>setForm({...form,password:e.target.value})}
            />
            <input
            value={confirmPass} 
            type="password" 
            placeholder="Confirm password"
            className="w-full p-2 mb-4 bg-gray-700 rounded"
            onChange={(e)=>SetConfirmPass(e.target.value)}
            />
            <button className="w-full bg-blue-500 p-2 rounded hover:bg-blue-600">
                SignUp
            </button>
            <p className="text-sm mt-4 text-center">
                Already have an account? <span
                className="text-blue-400 cursor-pointer"
                onClick={()=>navigate("/login")}
                >Login</span>
            </p>
        </form>
    </div>
   )
}