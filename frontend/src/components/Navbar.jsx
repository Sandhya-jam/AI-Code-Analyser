import { Link,useNavigate } from "react-router-dom";

export const Navbar=()=>{
    const navigate=useNavigate();

    function logout(){
        localStorage.removeItem("token");
        navigate('/login')
    }

    return(
        <nav className="bg-gray-900 text-white p-4 flex justify-between item-center">
            <h1 className="text-xl font-bold">
                AI Code Analyzer
            </h1>
            <div className="flex gap-6 items-center">
                <Link 
                to='/analyzer'
                className="hover:text-blue-400">
                Analyzer
                </Link>
                <Link 
                to='/history'
                className="hover:text-blue-400">
                History
                </Link>
                <Link 
                to='/dashboard'
                className="hover:text-blue-400">
                Dashboard
                </Link>
                <button 
                className="bg-red-500 px-3 py-1 rounded hover:bg-red-600"
                onClick={logout}>Logout
                </button>
            </div>
        </nav>
    )
}