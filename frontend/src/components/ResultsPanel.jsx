import React from 'react'

const ResultsPanel = ({result}) => {
   if(!result){
      return (
      <div className='text-gray-400'>
        Run analysis to see results.
      </div>
    );
   }

   return(
     <div className='space-y-6'>
        {/* Risk Score */}
        <div>
            <h2 className='text-xl font-semibold mb-2'>
                Code Quality Score
            </h2>
            <div className="bg-gray-700 rounded-full h-4">
                <div className="bg-green-500 h-4 rounded-full"
                style={{width:`${result.risk_score}%`}}
                />
            </div>
            <p className="mt-2 text-yellow-400">
                Risk Score:{result.risk_score}
            </p>
        </div>

        {/* BUGS */}
        <div>
            <h2 className="text-red-400 font-semibold">
                Critical Issues
            </h2>
            {result.critical?.length===0 ? (
                <p className='text-gray-400'>None</p>
            ):(
                result.critical?.map((bug,index)=>(
                    <div key={index} className='text-sm'>
                        Line {bug.line} : {bug.message}
                    </div>
                ))
            )}
        </div>
        {/* HIGH */}
        <div>
            <h2 className="text-orange-900 font-semibold">
                high Issues
            </h2>
            {result.high?.length===0 ? (
                <p className='text-gray-400'>None</p>
            ):(
                result.high?.map((bug,index)=>(
                    <div key={index} className='text-sm'>
                        Line {bug.line} : {bug.message}
                    </div>
                ))
            )}
        </div>
        {/* MEDIUM */}
        <div>
            <h2 className="text-yellow-500 font-semibold">
                medium Issues
            </h2>
            {result.medium?.length===0 ? (
                <p className='text-gray-400'>None</p>
            ):(
                result.medium?.map((bug,index)=>(
                    <div key={index} className='text-sm'>
                        Line {bug.line} : {bug.message}
                    </div>
                ))
            )}
        </div>
        {/* LOW */}
        <div>
            <h2 className="text-green-400 font-semibold">
                low Issues
            </h2>
            {result.low?.length===0 ? (
                <p className='text-gray-400'>None</p>
            ):(
                result.low?.map((bug,index)=>(
                    <div key={index} className='text-sm'>
                        Line {bug.line} : {bug.message}
                    </div>
                ))
            )}
        </div>
        {/* AI Complexity */}
        {result.ai_analysis && (
            <div>
                <h2 className="text-blue-400 font-semobold">
                    Complexity
                </h2>
                <p className='text-blue-400'>Time:{result.ai_analysis.time_complexity}</p>
                <p className='text-blue-400'>Space:{result.ai_analysis.space_complexity}</p>
            </div>
        )}
     </div>
   );
}

export default ResultsPanel