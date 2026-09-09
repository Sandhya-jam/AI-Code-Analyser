import { useEffect, useState } from "react";
import {getHistory,getHistoryStats} from "../services/api";
import { Navbar } from "../components/Navbar";
import {PieChart,Pie,Cell,Tooltip,ResponsiveContainer,BarChart,Bar,XAxis,YAxis,CartesianGrid} from "recharts";

const Dashboard = () => {
    const [stats, setStats] = useState(null);
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadDashboard = async () => {
            try {
                setLoading(true);
                const [statsData, historyData] = await Promise.all([
                    getHistoryStats(),
                    getHistory({
                        page: 1,
                        limit: 5
                    })
                ]);
                console.log(statsData)
                setStats(statsData);
                setHistory(historyData.history || []);
            } catch (error) {
                console.error("Dashboard error:", error);
                setError("Failed to load dashboard");
            } finally {
                setLoading(false);
            }
        };
        loadDashboard();
    }, []);


    if (loading) {
        return (
            <div className="min-h-screen bg-gray-900 text-white">
                <Navbar />
                <div className="max-w-7xl mx-auto p-6">
                    <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
                    <div className="text-gray-400">
                        Loading dashboard...
                    </div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-gray-900 text-white">
                <Navbar />
                <div className="max-w-7xl mx-auto p-6">
                    <h1 className="text-2xl font-bold mb-6">
                        Dashboard
                    </h1>
                    <div className="bg-red-900/30 border border-red-700 p-4 rounded-xl">
                        {error}
                    </div>
                </div>
            </div>
        );
    }

    const overview = stats?.overview || {};
    const severity = stats?.severity || {};
    const actionData = [{name: "Analyze",value: overview.totalAnalyses || 0},
        {name: "Fix",value: overview.totalFixes || 0}];

    const severityData = [
        {name: "Critical",value: severity.critical || 0},
        {name: "High",value: severity.high || 0},
        {name: "Medium",value: severity.medium || 0},
        {name: "Low",value: severity.low || 0}
    ];

    const COLORS = ["#3b82f6","#10b981"];

    return (
        <div className="min-h-screen bg-gray-900 text-white">
            <Navbar />
            <div className="max-w-7xl mx-auto p-6">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold">Dashboard</h1>
                    <p className="text-gray-400 mt-1">
                        Overview of your code analysis activity</p>
                </div>
                {/* ================= STATS ================= */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-6">
                    {/* Total Analyses */}
                    <div className="bg-gray-800 p-5 rounded-xl border border-gray-700">
                        <p className="text-gray-400 text-sm">
                            Total Analyses</p>
                        <h2 className="text-3xl font-bold mt-2">
                            {overview.totalAnalyses || 0}
                        </h2>
                    </div>
                    {/* Total Fixes */}
                    <div className="bg-gray-800 p-5 rounded-xl border border-gray-700">
                        <p className="text-gray-400 text-sm">
                            Total Fixes</p>
                        <h2 className="text-3xl font-bold mt-2">
                            {overview.totalFixes || 0}</h2>
                    </div>
                    {/* Average Risk */}
                    <div className="bg-gray-800 p-5 rounded-xl border border-gray-700">
                        <p className="text-gray-400 text-sm">
                            Average Risk</p>
                        <h2 className="text-3xl font-bold mt-2">
                            {Math.round(
                                overview.averageRiskScore || 0
                            )}
                        </h2>
                    </div>
                    {/* Total Issues */}
                    <div className="bg-gray-800 p-5 rounded-xl border border-gray-700">
                        <p className="text-gray-400 text-sm">Total Issues</p>
                        <h2 className="text-3xl font-bold mt-2">{overview.totalIssues || 0}</h2>
                    </div>
                </div>
                {/* ================= CHARTS ================= */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Analyze vs Fix */}
                    <div className="bg-gray-800 p-6 rounded-xl">
                        <h2 className="font-semibold mb-4">Analyze vs Fix</h2>
                        <div className="flex justify-center">
                            <PieChart width={300} height={300}>
                                <Pie
                                    data={actionData}
                                    cx="50%"
                                    cy="50%"
                                    outerRadius={100}
                                    dataKey="value"
                                    label
                                >
                                    {actionData.map(
                                        (entry, index) => (
                                            <Cell
                                                key={index}
                                                fill={COLORS[index]}
                                            />
                                        )
                                    )}
                                </Pie>
                                <Tooltip />
                            </PieChart>
                        </div>
                    </div>
                    {/* Severity */}
                    <div className="bg-gray-800 p-6 rounded-xl">
                        <h2 className="font-semibold mb-4">Issue Severity</h2>
                        <ResponsiveContainer
                            width="100%"
                            height={300}
                        >
                            <BarChart
                                data={severityData}
                            >
                                <CartesianGrid
                                    strokeDasharray="3 3"
                                    stroke="#374151"
                                />
                                <XAxis
                                    dataKey="name"
                                    stroke="#9ca3af"
                                />
                                <YAxis stroke="#9ca3af"/>
                                <Tooltip />
                                <Bar
                                    dataKey="value"
                                    fill="#ef4444"
                                    radius={[6, 6, 0, 0]}
                                >
                                {severityData.map((entry, index) => {
                                    const colors = {
                                        Critical: "#ef4444",
                                        High: "#f97316",
                                        Medium: "#eab308",
                                        Low: "#22c55e"
                                    };
                                    return (
                                        <Cell
                                            key={`cell-${index}`}
                                            fill={colors[entry.name]}
                                        />
                                    );
                                })}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
                {/* ================= COMPLEXITY ================= */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
                    {/* Time Complexity */}
                    <div className="bg-gray-800 p-6 rounded-xl">
                        <h2 className="font-semibold mb-4">Time Complexity</h2>
                        {stats?.timeComplexity?.length === 0 ? (
                            <p className="text-gray-500">
                                No data available
                            </p>
                        ) : (
                            stats?.timeComplexity?.map((item) => (
                                <div
                                    key={item._id}
                                    className="flex justify-between py-3 border-b border-gray-700 last:border-0">
                                    <span className="text-gray-300">{item._id}</span>
                                    <span className="font-semibold">{item.count}</span>
                                </div>
                            ))
                        )}
                    </div>
                    {/* Space Complexity */}
                    <div className="bg-gray-800 p-6 rounded-xl">
                        <h2 className="font-semibold mb-4">Space Complexity</h2>
                        {stats?.spaceComplexity?.length === 0 ? (
                            <p className="text-gray-500">
                                No data available</p>
                        ) : (
                            stats?.spaceComplexity?.map((item) => (
                                <div
                                    key={item._id}
                                    className="flex justify-between py-3 border-b border-gray-700 last:border-0">
                                    <span className="text-gray-300">
                                        {item._id}
                                    </span>
                                    <span className="font-semibold">{item.count}</span>
                                </div>
                            ))
                        )}
                    </div>
                </div>
                {/* ================= LANGUAGES ================= */}
                <div className="bg-gray-800 p-6 rounded-xl mt-6">
                    <h2 className="font-semibold mb-4">Languages</h2>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                        {stats?.language?.map((item) => (
                            <div
                                key={item._id}
                                className="bg-gray-700/50 rounded-lg p-4"
                            >
                                <p className="text-gray-400 text-sm">{item._id}</p>
                                <p className="text-2xl font-bold mt-1">{item.count}</p>
                            </div>
                        ))}
                    </div>
                </div>
                {/* ================= RECENT ACTIVITY ================= */}
                <div className="bg-gray-800 p-6 rounded-xl mt-6">
                    <div className="flex justify-between items-center mb-4">
                        <h2 className="font-semibold">Recent Activity</h2>
                        <button
                            className="text-blue-400 hover:text-blue-300 text-sm"
                            onClick={() => {
                                window.location.href = "/history";
                            }}
                        >
                            View All →
                        </button>
                    </div>
                    {history.length === 0 ? (
                        <p className="text-gray-500">
                            No analysis history yet.
                        </p>
                    ) : (
                        <div className="space-y-3">
                            {history.map((item) => (
                                <div
                                    key={item._id}
                                    className="flex justify-between items-center bg-gray-700/40 p-4 rounded-lg"
                                >
                                    <div>
                                        <p className="font-medium">{item.action.toUpperCase()}</p>
                                        <p className="text-sm text-gray-400">{item.language}</p>
                                    </div>
                                    <div className="text-right">
                                        <p className="text-sm">
                                            Risk:{" "}
                                            {item.result?.risk_score ?? "-"}
                                        </p>
                                        <p className="text-xs text-gray-500">
                                            {new Date(
                                                item.createdAt
                                            ).toLocaleString()}
                                        </p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Dashboard;