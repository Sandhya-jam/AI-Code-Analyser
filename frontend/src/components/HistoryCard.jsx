import React from 'react'

const HistoryCard = ({item,onClick}) => {
  const result=item.result||{};
  const ai_analysis=result.ai_analysis||{};

  const issueCount=(result?.critical?.length||0)+(result?.high?.length||0)+(result?.medium?.length||0)+(result?.low?.length||0);
  return (
    <div 
    onClick={()=>onClick(item)}
    className="bg-gray-800 p-5 rounded-xl cursor-pointer hover:bg-gray-700 transition-transform duration-300 hover:scale-[1.02]">
        <div className="flex justify-between items-center mb-3">
          <h2 className="text-lg font-semibold">
            {item.action.toUpperCase()}
          </h2>
          <span className="text-gray-400 text-sm">{item.language}</span>
        </div>
        {/* Risk Score */}
        <div className="mb-2">
          <p className="text-gray-400 text-sm">Risk Score:</p>
          <p className="text-lg font-semibold">{result?.risk_score ?? 0}</p>
        </div>
        {/* COMPLEXITY */}
        <div className="mb-2">
          <p className="text-gray-400 text-sm">Time Complexity:</p>
          <p className="font-medium">{ai_analysis?.time_complexity ?? "-"}</p>
        </div>
        {/* Issues */}
        <div className="mb-2">
          <p className="text-gray-400 text-sm">Issues:</p>
          <p className="font-medium">{issueCount}</p>
        </div>
        {/* DATE */}
        <p className="text-sm text-gray-500">
          {new Date(item.createdAt).toLocaleString()}
        </p>
      </div>
    );
};

export default HistoryCard