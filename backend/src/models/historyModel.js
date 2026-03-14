import mongoose from 'mongoose'

const historySchema=new mongoose.Schema({
    user:{
        type:mongoose.Schema.Types.ObjectId,
        ref:"User"
    },
    action:{
        type:String,
        enum:["analyze","fix"] 
    },
    language:{type:String},
    code:{type:String,required:true},
    result:{type:Object},
    fixedCode:{type:String},
},{timestamps:true});

export default mongoose.model("History",historySchema);