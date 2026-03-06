import React from 'react'

const AIInsights = ({result}) => {
    if(!result || !result.ai_analysis){
        return null
    }
    const ai=result.ai_analysis

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* OPTIMIZATIONs */}
        <div className="bg-gray-800 p-4 rounded-xl shadow-lg">
            <h2 className="text-lg font-semibold mb-3 text-green-400">
                Optimization Suggestions
            </h2>
            {ai.optimizations?.length===0?(
                <p className="text-gray-400">None</p>
            ):(
                <ul className="list-disc pl-5 space-y-1">
                    {ai.optimizations.map((opt,i)=>(
                        <li key={i}>{opt}</li>
                    ))}
                </ul>
            )}
        </div>

        {/* BUG FIXES */}
        <div className="bg-gray-800 p-4 rounded-xl shadow-lg">
            <h2 className="text-lg font-semibold mb-3 text-purple-400">
                Suggested Fixes
            </h2>
            {ai.bug_fixes?.length===0?(
                <p className="text-gray-400">None</p>
            ):(
                <ul className="list-disc pl-5 space-y-1">
                    {ai.bug_fixes.map((fix,i)=>(
                        <li key={i}>{fix}</li>
                    ))}
                </ul>
            )}
        </div>
        {/* EXPLANATION */}
        <div className="bg-gray-800 p-4 rounded-xl shadow-lg">
            <h2 className="text-lg font-semibold mb-3 text-blue-400">
                Code Explanation 
            </h2>
            <p className="text-gray-300 text-sm leading-relaxed">
                {ai.explanation}
            </p>
        </div>
    </div>
  )
}

export default AIInsights;