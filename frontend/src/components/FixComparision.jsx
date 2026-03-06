import { DiffEditor } from "@monaco-editor/react";

const FixComparison = ({ originalCode, fixedCode, onApply }) => {

if (!originalCode || !fixedCode) {
    return (
        <div className="flex items-center justify-center h-[420px] bg-gray-800 rounded-xl">
            <p className="text-gray-400">
                Run "Fix Code with AI" to see comparison
            </p>
        </div>
    );
}

return(

<div className="flex flex-col gap-4">

<h2 className="text-xl font-semibold text-white">
AI Code Fix Comparison
</h2>

<div className="w-full h-[420px] rounded-lg overflow-hidden border border-gray-700">

<DiffEditor
height="100%"
original={originalCode}
modified={fixedCode}
language="python"
theme="vs-dark"
options={{
readOnly:true,
automaticLayout:true
}}
/>

</div>

<button
onClick={onApply}
className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg"
>
Apply Fix
</button>

</div>

);

};

export default FixComparison;