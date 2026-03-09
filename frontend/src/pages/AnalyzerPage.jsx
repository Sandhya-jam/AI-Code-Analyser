import { useState } from "react"
import { CodeEditor } from "../components/CodeEditor"
import ResultsPanel from "../components/ResultsPanel"
import AIInsights from "../components/AIInsights"
import FixComparison from "../components/FixComparision";

const AnalyzerPage = () => {

const [result,setResult]=useState(null);
const [markers,setMarkers]=useState([]);
const [code,setCode] = useState(`# Paste your python code here
print("hello")
`);
const [fixedCode,setFixedCode] = useState("");

async function analyzeCode(code){

        const response=await fetch("http://localhost:5000/analyze",{
        method:"POST",
        headers:{
        "Content-Type":"application/json"
        },
        body:JSON.stringify({code})
        });

        const data=await response.json();

        setResult(data);

        const newMarkers=[];

        ["critical","high","medium","low"].forEach(level=>{
        data[level]?.forEach(bug=>{
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

async function fixCode(code){
try {
  const res = await fetch("http://localhost:5000/fix",{
  method:"POST",
  headers:{
  "Content-Type":"application/json"
  },
  body:JSON.stringify({code})
  });

  const data = await res.json();

  console.log("Fix Response",data)
  if(data.fixed_code){
  setFixedCode(data.fixed_code);
}
} catch (error) {
  console.error("Fix Error:",error);
}
};

return (

    <div className="min-h-screen bg-gray-900 text-white">

    <div className="max-w-7xl mx-auto p-6">

    {/* Header */}
    <div className="mb-6 border-b border-gray-700 pb-4">
        <h1 className="text-3xl font-bold">
        AI CODE ANALYZER
        </h1>
    </div>

    {/* ROW-1 */}

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">

    <div className="bg-gray-800 rounded-xl p-4 shadow-lg flex flex-col">
    <CodeEditor
        onAnalyze={analyzeCode}
        onFix={fixCode}
        markers={markers}
        code={code}
        setCode={setCode}
        />
    </div>

    <div className="bg-gray-800 rounded-xl p-4 shadow-lg">
    <FixComparison
    originalCode={code}
    fixedCode={fixedCode}
    onApply={()=>{
        setCode(fixedCode);
        setFixedCode("");
    }}/>
    </div>
    </div>

    {/* ROW-2 */}

    <div className="grid grid-cols-1 lg:grid-cols-2 mb-6 gap-4">
       <div className="bg-gray-800 rounded-xl p-4 shadow-lg">
         <ResultsPanel result={result}/>
       </div>
       <div className="bg-gray-800 rounded-xl p-4 shadow-lg">
         <h2 className="text-xl font-semibold mb-3">
                    Code Explanation
          </h2>
         <AIInsights type="explanation" result={result}/>
       </div>
    </div>
    {/* ROW-3*/}
    <div className="grid grid-cols-1 lg:grid-cols-2 mb-6 gap-4">
       <div className="bg-gray-800 rounded-xl p-4 shadow-lg">
        <h2 className="text-xl font-semibold mb-3">Optimization Suggestions</h2>
         <AIInsights type="optimizations" result={result}/>
       </div>
       <div className="bg-gray-800 rounded-xl p-4 shadow-lg">
        <h2 className="text-xl font-semibold mb-3">
                    Suggested Fixes
        </h2>
         <AIInsights type="bugfixes" result={result}/>
       </div>
    </div>
    </div>
    </div>

    );
};

export default AnalyzerPage