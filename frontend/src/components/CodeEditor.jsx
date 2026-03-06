import Editor from '@monaco-editor/react'
import { useState } from 'react'

export const CodeEditor = ({onAnalyze,markers}) => {
    const [code,setCode]=useState(`# Paste your python Code here
        print('hello')
    `);

    function handleAnalyze(){
        onAnalyze(code)
    }
    
    function handleEditorDidMount(editor,monaco){
        if(markers && markers.length>0){
            monaco.editor.setModelMarkers(
                editor.getModel(),
                "analysis",
                markers
            );
        }
    }

  return (
    <div className='flex flex-col gap-4'>
       <Editor
       height="400px"
       defaultLanguage='python'
       value={code}
       theme='vs-dark'
       onChange={(value)=>setCode(value)}
       onMount={handleEditorDidMount}
       />

       <button
       onClick={handleAnalyze}
       className='bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg font-semibold'
       >
        Analyze Code 
       </button>
    </div>
  );
}
