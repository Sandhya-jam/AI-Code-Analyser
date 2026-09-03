import mongoose from 'mongoose'

const historySchema=new mongoose.Schema({
    user:{
        type:mongoose.Schema.Types.ObjectId,
        ref:"User",
        required:true
    },
    action:{
        type:String,
        enum:["analyze","fix"],
        required:true
    },
    language:{type:String,required:true},
    code:{type:String,required:true},
    result:{type:Object},
    fixedCode:{type:String},
},{timestamps:true});

//Most recent history first
historySchema.index({user:1,createdAt:-1});

//Useful for Filtering
historySchema.index({user:1,action:1,createdAt:-1});
historySchema.index({user:1,language:1,createdAt:-1});

export default mongoose.model("History",historySchema);