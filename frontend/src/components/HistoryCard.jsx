import React from 'react'

const HistoryCard = ({item,onClick}) => {
  return (
    <div 
    onClick={()=>onClick(item)}
    className="bg-gray-800 p-4 rounded-xl cursor-pointer hover:bg-gray-700 transition-transform duration-300 hover:scale-110">
    <h2 className="text-lg font-semibold">
        {item.action.toUpperCase()}
    </h2>
    <p>Language:{item.language}</p>
    <p>
    Risk Score: {item.result?.risk_score || "N/A"}
    </p>
    <p>
    Complexity:
    {item.result?.ai_analysis?.time_complexity || "-"}
    </p>
    <p>
    Issues:
    {(item.result?.critical?.length || 0) +
    (item.result?.high?.length || 0) +
    (item.result?.medium?.length || 0) +
    (item.result?.low?.length || 0)}
    </p>
    <p>
        Date:{new Date(item.createdAt).toLocaleString()}
    </p>
    </div>
  )
}

export default HistoryCard