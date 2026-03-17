import { useEffect,useState } from "react"
import { getHistory } from "../services/api"
import { Navbar } from "../components/Navbar"
import {PieChart,Pie,Cell,Tooltip,BarChart,Bar,XAxis,YAxis,CartesianGrid} from 'recharts'

const Dashboard = () => {
    const [history,setHistory]=useState([]);

    useEffect(()=>{
        getHistory().then(setHistory);
    },[]);
    const analyzeCount=history?.filter(h=>h.action==="analyze")?.length;
    const fixCount=history?.filter(h=>h.action=='fix')?.length

    const data=[
        {name:"Analyze",value:analyzeCount},
        {name:"Fix",value:fixCount}
    ];
    const COLORS=['#3b82f6','#10b981']
  return (
    <div className="min-h-screen bg-gray-900 text-white">
        <Navbar/>
        <div className="max-w-7xl mx-auto p-6">
            <h1 className="text-2xl font-bold mb-6">
                Dashboard
            </h1>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Pie Chart */}
                <div className="bg-gray-800 p-6 rounded-xl">
                    <h2 className="mb-4 font-semibold">
                        Analyze vs Fix
                    </h2>
                    <PieChart width={300} height={300}>
                        <Pie
                        data={data}
                        cx="50%"
                        cy='50%'
                        outerRadius={100}
                        dataKey="value"
                        >
                        {data?.map((entry,index)=>{
                            <Cell key={index} fill={COLORS[index]}/>
                        })}
                        </Pie>
                    </PieChart>
                </div>
            </div>
        </div>
    </div>
  )
}

export default Dashboard