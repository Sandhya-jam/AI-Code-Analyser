import { useEffect,useState } from "react"
import { getHistory } from "../services/api"
import HistoryCard from "../components/HistoryCard"
import { Navbar } from "../components/Navbar"

const History = () => {
    const [history,setHistory]=useState([]);
    const [selected,setSelected]=useState(null);
    const [filters,setFilters] = useState({
        action:"all",
        severity:"all"
        });
    const filteredHistory = history.filter(item=>{
    if(filters.action !== "all" && item.action !== filters.action){
    return false;
    }

    if(filters.severity !== "all"){

    const issues = item.result?.[filters.severity];
    if(!issues || issues.length === 0){
        return false;
    }
    }
    return true;
    });
    useEffect(()=>{
        async function fetchHistory() {
            const data=await getHistory();
            setHistory(data)
        }
        fetchHistory();
    },[]);

  return (
    <div className="min-h-screen bg-gray-900 text-white">
        <Navbar/>
        <div className="max-w-7xl mx-auto p-6">
            <h1 className="text-2xl font-bold mb-6">
                History
            </h1>
            <div className="flex gap-4 mb-6">
                <select 
                onChange={(e)=>setFilters({...filters,action:e.target.value})}
                className="bg-gray-800 p-2 rounded">
                    <option value="all">All Actions</option>
                    <option value="analyze">Analyze</option>
                    <option value="fix">Fix</option>
                </select>
                <select
                    className="bg-gray-800 p-2 rounded"
                    onChange={(e)=>setFilters({...filters,severity:e.target.value})}
                    >
                    <option value="all">All Severity</option>
                    <option value="critical">Critical</option>
                    <option value="high">High</option>
                    <option value="medium">Medium</option>
                    <option value="low">Low</option>

                </select>
            </div>
            {/* Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {filteredHistory?.map(item=>(
                    <HistoryCard
                    key={item._id}
                    item={item}
                    onClick={setSelected}
                    />
                ))}
            </div>
            {/* Detailed view */}
            {selected &&(
                <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center p-4">
                    <div className="bg-gray-800 rounded-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto p-6">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-2xl font-bold">Analysis Details</h2>
                            <button 
                            onClick={()=>setSelected(null)}
                            className="bg-red-500 px-3 py-1 rounded">Close</button>
                        </div>
                        {/* Overview */}
                        <div className="mb-6">
                            <h3 className="text-xl font-semibold mb-2">Overview</h3>
                            <p>Language:{selected.language}</p>
                            <p>Date:{new Date(selected.createdAt).toLocaleString()}</p>
                            {selected.result?.risk_score && (
                                <p>Risk Score:{selected.result.risk_score}</p>
                            )}
                        </div>
                        {/* Complexity */}
                        {selected.result?.ai_analysis && (
                            <div className="mb-6">
                                <h3 className="text-xl font-semibold mb-2">Complexity</h3>
                                <p>Time Complexity:{selected.result.ai_analysis.time_complexity}</p>
                                <p>Space Complexity:{selected.result.ai_analysis.space_complexity}</p>
                            </div>
                        )}
                        {/* Issues */}
                        <div className="mb-6">
                            <h3 className="text-xl font-semibold mb-2">
                            Detected Issues
                            </h3>

                        {["critical","high","medium","low"].map(level=>

                        selected.result?.[level]?.map((issue,i)=>(
                        <div
                            key={i}
                            className="bg-gray-700 p-3 rounded mb-2"
                            >

                            <p className="font-semibold">
                            {level.toUpperCase()}
                            </p>

                            <p>{issue.message}</p>

                            {issue.line && (
                            <p className="text-sm text-gray-300">
                            Line: {issue.line}
                            </p>
                            )}

                        </div>
                        ))
                        )}
                        </div>
                        {/* Explanation */}
                        {selected.result?.ai_analysis?.explanation && (
                            <div className="mb-6">
                                <h3 className="text-xl font-semibold mb-2">Explanation</h3>
                                <p>{selected.result.ai_analysis.explanation}</p>
                            </div>
                        )}
                        {/* Optimizations */}
                        {selected.result?.ai_analysis?.optimizations && (
                            <div>
                                <h3 className="text-xl font-semibold mb-2">Optimization Suggestions</h3>
                                <ul className="list-disc pl-6">
                                    {selected.result.ai_analysis.optimizations.map((opt,i)=>(
                                        <li key={i}>{opt}</li>
                                    ))}
                                </ul>
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