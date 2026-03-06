import Editor from "@monaco-editor/react";
import { useState, useEffect } from "react";

export const CodeEditor = ({ onAnalyze, onFix, markers }) => {

const [code,setCode] = useState(`# Paste your python code here
print("hello")
`);

const [editorInstance,setEditorInstance] = useState(null);

function handleAnalyze(){
onAnalyze(code);
}

function handleFix(){
onFix(code);
}

function handleEditorDidMount(editor,monaco){
setEditorInstance({editor,monaco});
}

useEffect(()=>{

if(editorInstance && markers){

const {editor,monaco} = editorInstance;

monaco.editor.setModelMarkers(
editor.getModel(),
"analysis",
markers
);

}

},[markers,editorInstance]);

return(

<div className="flex flex-col gap-4 w-full">

<div className="w-full h-[420px] rounded-lg overflow-hidden border border-gray-700">

<Editor
height="100%"
defaultLanguage="python"
value={code}
theme="vs-dark"
onChange={(value)=>setCode(value)}
onMount={handleEditorDidMount}
options={{
fontSize:14,
minimap:{enabled:false},
automaticLayout:true
}}
/>

</div>

<div className="flex w-full gap-4">

<button
onClick={handleAnalyze}
className="flex-1 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg font-semibold"
>
Analyze Code
</button>

<button
onClick={()=>handleFix(code)}
className="flex-1 bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg font-semibold"
>
Fix Code with AI
</button>

</div>

</div>

);
};