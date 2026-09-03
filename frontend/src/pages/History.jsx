import { useEffect,useState } from "react"
import { getHistory,getHistoryById } from "../services/api"
import HistoryCard from "../components/HistoryCard"
import { Navbar } from "../components/Navbar"

const History = () => {
    const [history,setHistory]=useState([]);
    const [selected,setSelected]=useState(null);
    const [loading,setLoading]=useState(false);
    const [filters,setFilters] = useState({
        action:"all",
        severity:"all",
        language:"all"
    });
    const [pagination,setPagination]=useState({
        page:1,
        limit:10,
        total:0,
        totalPages:0
    });
    const fetchHistory=async()=>{
        try{
            setLoading(true);
            const data=await getHistory({
                page:pagination.page,
                limit:pagination.limit,
                action:filters.action,
                severity:filters.severity,
                language:filters.language
            });
            setHistory(data.history);
            setPagination(data.pagination);
        }catch(error){
            console.error("Failed to fetch history",error);
        }finally{
            setLoading(false);
        }
    };

    useEffect(()=>{
        fetchHistory();
    },[pagination.page,filters.action,filters.severity,filters.language]);

    //FILTER CHANGE
    const handleFilterChange=(key,value)=>{
        setFilters(prev=>({
            ...prev,
            [key]:value
        }));
        //when filter changes, reset to page 1
        setPagination(prev=>({
            ...prev,
            page:1
        }));
    };
    //OPEN HISTORY DETAILS
    const handleHistoryClick=async(item)=>{
        try{
            const data=await getHistoryById(item._id);
            setSelected(data);
        }catch(error){
            console.error("Failed to fetch history details",error);
        }
    };
    //PAGINATION
    const handlePrevious=()=>{
        if(pagination.page>1){
            setPagination(prev=>({
                ...prev,
                page:prev.page-1
            }));
        }
    };
    const handleNext=()=>{
        if(pagination.page<pagination.totalPages){
            setPagination(prev=>({
                ...prev,
                page:prev.page+1
            }));
        }
    };
  return (
    <div className="min-h-screen bg-gray-900 text-white">
        <Navbar/>
        <div className="max-w-7xl mx-auto p-6">
            <div className="flex justify-between items-center mb-6">
                <div>
                    <h1 className="text-3xl font-bold">Analysis History</h1>
                    <p className="text-gray-400 mt-1">View and explore your previous code analyses</p>
                </div>
            </div>
            {/* FILTERS */}
            <div className="flex flex-wrap gap-4 mb-6">
                {/* ACTION */}
                <select 
                value={filters.action}
                onChange={(e)=>handleFilterChange("action",e.target.value)}
                className="bg-gray-800 border border-gray-700 px-4 py-2 rounded-lg">
                    <option value="all">All Actions</option>
                    <option value="analyze">Analyze</option>
                    <option value="fix">Fix</option>
                </select>
                {/* SEVERITY */}
                <select 
                value={filters.severity}
                onChange={(e)=>handleFilterChange("severity",e.target.value)}
                className="bg-gray-800 border border-gray-700 px-4 py-2 rounded-lg">
                    <option value="all">All Severities</option>
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                </select>
                {/* LANGUAGE */}
                <select 
                value={filters.language}
                onChange={(e)=>handleFilterChange("language",e.target.value)}
                className="bg-gray-800 border border-gray-700 px-4 py-2 rounded-lg">
                    <option value="all">All Languages</option>
                    {/* <option value="javascript">JavaScript</option> */}
                    <option value="python">Python</option>
                    {/* <option value="java">Java</option> */}
                </select>
            </div>
            {/* LOADING SPINNER */}
            {loading && (
                <div className="text-center py-10 text-gray-400">Loading History...</div>
            )}
            {/* EMPTY STATE */}
            {!loading && history.length===0 && (
                <div className="text-center py-16">
                   <p className="text-gray-400 text-lg">No Analysis history found.</p>
                </div>
            )}
            {/* HISTORY CARDS */}
            {!loading && history.length>0 && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                    {history.map(item=>(
                        <HistoryCard 
                        key={item._id} 
                        item={item}
                        onClick={handleHistoryClick}
                        />
                    ))}
                </div>
            )}
            {/* PAGINATION */}
            {!loading && pagination.totalPages>0 && (
                <div className="flex justify-between items-center mt-8">
                    <p className="text-gray-400">
                        Page {pagination.page} of {" "}{pagination.totalPages}
                    </p>
                    <div className="flex gap-3">
                        <button 
                        onClick={handlePrevious}
                        disabled={pagination.page===1}
                        className="px-4 py-2 bg-gray-800 rounded-lg disabled:opacity-40 disabled:cursor-not-allowed hover:bg-gray-700">
                            Previous
                        </button>
                        <button 
                        onClick={handleNext}
                        disabled={pagination.page===pagination.totalPages}
                        className="px-4 py-2 bg-gray-800 rounded-lg disabled:opacity-40 disabled:cursor-not-allowed hover:bg-gray-700">
                            Next
                        </button>
                    </div>
                </div>
            )}
            {/* DETAIL MODAL */}
            {selected && (
                <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
                    <div className="bg-gray-800 rounded-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto p-6">
                        {/* Header */}
                        <div className="flex justify-between items-center mb-6">
                            <div> 
                                <h2 className="text-2xl font-bold">Analysis Details</h2>
                                <p className="text-gray-400 text-sm mt-1">
                                    {new Date(selected.createdAt).toLocaleString()}
                                </p>
                            </div>
                            <button 
                            onClick={()=>setSelected(null)}
                            className="bg-red-500 hover:bg-red-600 px-3 py-1 rounded-lg">
                                Close
                            </button>
                        </div>
                        {/* OVERVIEW */}
                        <div className="mb-6">
                            <h3 className="text-xl font-semibold mb-3">Overview</h3>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div className="bg-gray-700 p-4 rounded-lg">
                                    <p className="text-gray-400 text-sm">Language</p>
                                    <p className="font-semibold">{selected.language}</p>
                                </div>
                                <div className="bg-gray-700 p-4 rounded-lg">
                                    <p className="text-gray-400 text-sm">Action</p>
                                    <p className="font-semibold capitalize">{selected.action}</p>
                                </div>
                                <div className="bg-gray-700 p-4 rounded-lg">
                                    <p className="text-gray-400 text-sm">Risk Score</p>
                                    <p className="font-semibold">{selected.result?.risk_score??0}</p>
                                </div>
                            </div>
                        </div>
                        {/* COMPLEXITY */}
                        {selected.result?.ai_analysis && (
                            <div className="mb-6">
                                <h3 className="text-xl font-semibold mb-3">
                                    Complexity
                                </h3>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div className="bg-gray-700 p-4 rounded-lg">
                                        <p className="text-gray-400 text-sm">Time Complexity</p>
                                        <p className="font-semibold">{selected.result?.ai_analysis?.time_complexity??"N/A"}</p>
                                    </div>
                                    <div className="bg-gray-700 p-4 rounded-lg">
                                        <p className="text-gray-400 text-sm">Space Complexity</p>
                                        <p className="font-semibold">{selected.result?.ai_analysis?.space_complexity??"N/A"}</p>
                                    </div>
                                </div>
                            </div>
                        )}
                        {/* ISSUES */}
                        <div className="mb-6">
                            <h3 className="text-xl font-semibold mb-3">Detected Issues</h3>
                            {["critical","high","medium","low"].map(level=>{
                                const issues=selected.result?.[level]||[];
                                return issues.map((issue,index)=>(
                                    <div key={`${level}-${index}`} className="bg-gray-700 p-4 rounded-lg mb-3">
                                        <p className="font-semibold mb-1">{level.toUpperCase()}</p>
                                        <p>{issue.message}</p>
                                        {issue.line && (
                                            <p className="text-sm text-gray-400 mt-1">
                                                Line:{issue.line}
                                            </p>
                                        )}
                                    </div>
                                ));
                            })}
                        </div>
                        {/* AI EXPLANATION */}
                        {selected.result?.ai_analysis?.explanation && (
                            <div className="mb-6">
                                <h3 className="text-xl font-semibold mb-3">AI Explanation</h3>
                                <div className="bg-gray-700 p-4 rounded-lg">
                                    <p className="text-gray-200">
                                        {selected.result?.ai_analysis?.explanation}
                                    </p>
                                </div>
                            </div>
                        )}
                        {/* OPTIMIZATIONS */}
                        {selected.result?.ai_analysis?.optimizations?.length>0 &&(
                            <div className="mb-6">
                                <h3 className="text-xl font-semibold mb-3">
                                    Optimization Suggestions
                                </h3>
                                <ul className="list-disc pl-6 space-y-2">
                                    {selected.result?.ai_analysis?.optimizations.map((opt,index)=>(
                                        <li key={index} className="bg-gray-700 p-4 rounded-lg">
                                            {opt}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}
                        {/* LOGICAL BUGS */}
                        {selected.result?.ai_analysis?.logical_bugs?.length>0 &&(
                            <div className="mb-6">
                                <h3 className="text-xl font-semibold mb-3">
                                    Logical Bugs
                                </h3>
                                {selected.result?.ai_analysis?.logical_bugs.map((bug,index)=>(
                                    <div key={index} className="bg-gray-700 p-4 rounded-lg mb-3">
                                        <p>{bug}</p>    
                                    </div>
                                ))}
                            </div>
                        )}
                        {/* SECURITY ISSUES */}
                        {selected.result?.ai_analysis?.security_issues?.length>0 &&(
                            <div className="mb-6">
                                <h3 className="text-xl font-semibold mb-3">
                                    Security Issues
                                </h3>
                                {selected.result?.ai_analysis?.security_issues.map((issue,index)=>(
                                    <div key={index} className="bg-gray-700 p-4 rounded-lg mb-3">
                                        <p>{issue}</p>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    </div>
  )
}

export default History;