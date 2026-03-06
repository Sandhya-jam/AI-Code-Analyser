import { useState } from "react"
import { CodeEditor } from "../components/CodeEditor"
import ResultsPanel from "../components/ResultsPanel"
import AIInsights from "../components/AIInsights"

const AnalyzerPage = () => {
    const [result,setResult]=useState(null);
    const [markers,setMarkers]=useState([])

    async function analyzeCode(code) {
        const response=await fetch("http://localhost:5000/analyze",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({code})
        });

        const data=await response.json()

        setResult(data);

        const newMarkers=[];

        ["critical","high","medium","low"].forEach(level=>{
            data[level].forEach(bug=>{
                if(!bug.line) return;

                newMarkers.push({
                    startLineNumber:bug.line,
                    endLineNumber:bug.line,
                    startColumn:1,
                    endColumn:1,
                    message:bug.message,
                    severity:8
                });
            });
        });
        setMarkers(newMarkers);
    }
  return (
    <div className="min-h-screen bg-gray-900 text-white">
        {/* Header */}
        <div className="p-6 border-b border-gray-700">
            <h1 className="text-3xl font-bold">
                AI CODE ANALYZER 
            </h1>
        </div>
        {/* TOP SECTION */}
        <div className="p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* code editor */}
            <div className="bg-gray-800 rounded-xl p-4 shadow-lg">
                <CodeEditor 
                onAnalyze={analyzeCode}
                markers={markers}
                />
            </div>
            {/* Results */}
            <div className="bg-gray-800 rounded-xl p-4 shadow-lg overflow-auto">
                <ResultsPanel result={result}/>
            </div>
        </div>
        {/* BOTTOM SECTION */}
        <div className="px-6 pb-10">
            <AIInsights result={result}/>
        </div>
    </div>
  );
}

export default AnalyzerPage