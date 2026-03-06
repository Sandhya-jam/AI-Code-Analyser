import React from 'react'

const AIInsights = ({result,type}) => {
    if(!result || !result.ai_analysis){
        return null
    }
    
    if(type==="explanation"){
        return(
            <div>
                <p>{result.ai_analysis?.explanation}</p>
            </div>
        );
    }
    if(type==="optimizations"){
        return(
            <div>
                <ul className="list-disc ml-4">
                    {result.ai_analysis?.optimizations?.map((opt,i)=>(
                        <li key={i}>{opt}</li>
                    ))}
                </ul>
            </div>
        );
    }
    if(type==="bugfixes"){
        return(
            <div>
                <ul className="list-disc ml-4">
                    {result.ai_analysis?.bug_fixes?.map((fix,i)=>(
                        <li key={i}>{fix}</li>
                    ))}
                </ul>
            </div>
        );
    }

    return null;
}

export default AIInsights;