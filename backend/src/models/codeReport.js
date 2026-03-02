import mongoose from "mongoose";

const codeReportSchema=new mongoose.Schema(
    {
        sourceCode:String,
        analysisResult:Object
    },
    {timestamps:true}
);

export default mongoose.model("CodeReport",codeReportSchema);