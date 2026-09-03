import History from "../models/historyModel.js";

export const getUserhistory=async(req,res)=>{
    try{
        const page=Math.max(parseInt(req.query.page) || 1,1);
        const limit=Math.min(Math.max(parseInt(req.query.limit)||10,1),50);
        const skip=(page-1) * limit;

        const {action,language,severity}=req.query;

        const filter={user:req.user};

        //Action Filter
        if(action && action!=="all"){
            filter.action=action;
        }
        //Language Filter
        if(language && language!=="all"){
            filter.language=language;
        }
        //Severity Filter
        if(severity && severity!=="all"){
            filter[`result.analysis.${severity}`] = { 
              $exists: true, 
            };
        }

        const [history,total]=await Promise.all([
          History.find(filter)
            .sort({createdAt:-1})
            .skip(skip)
            .limit(limit)
            .select("-code -fixedCode -result"),

          History.countDocuments(filter)
        ]);
        res.json({
          history,
          pagination:{
            page,
            limit,
            totalPages:Math.ceil(total/limit),
          },
        });
    }catch(error){
        console.error("History error",error);
        res.status(500).json({message:"Failed to fetch history"});
    }
};

export const getHistoryById=async(req,res)=>{
    try{
        const history=await History.findOne({
            _id:req.params.id,
            user:req.user
        })
        if(!history){
            return res.status(404).json({message:"History not found"});
        }
        res.json(history);
    }catch(error){
        console.error("History error",error);
        res.status(500).json({message:"Failed to fetch history"});
    }
};

export const getHistoryStats=async(req,res)=>{
    try{
        const userId=new mongoose.Types.ObjectId(req.user);
        const stats=await History.aggregate([
            {$match:{user:userId}},
            {$facet:{
                overview:[
                    {
                        $group:{
                            _id:null,
                            totalAnalyses:{$sum:{$cond:[{$eq:["$action","analyze"]},1,0]}},
                            totalFixes:{$sum:{$cond:[{$eq:["$action","fix"]},1,0]}},
                            averageRiskScore:{$avg:"$result.analysis.risk_score"},
                            totalIssues:{$sum:{$add:[
                                {$size:{$ifNull:["$result.analysis.critical",[]]}},
                                {$size:{$ifNull:["$result.analysis.high",[]]}},
                                {$size:{$ifNull:["$result.analysis.medium",[]]}},
                                {$size:{$ifNull:["$result.analysis.low",[]]}}
                            ]}}
                        }
                    }
                ],
                severity:[
                    {
                        $group:{
                            _id:null,
                            critical:{$sum:{$size:{$ifNull:["$result.analysis.critical",[]]}}},
                            high:{$sum:{$size:{$ifNull:["$result.analysis.high",[]]}}},
                            medium:{$sum:{$size:{$ifNull:["$result.analysis.medium",[]]}}},
                            low:{$sum:{$size:{$ifNull:["$result.analysis.low",[]]}}}
                        }
                    }
                ],
                language:[
                    {
                        $group:{
                            _id:"$language",
                            count:{$sum:1}
                        },
                    },
                    {
                        $sort:{
                            count:-1
                        }
                    }
                ],
                timeComplexity:[
                    {
                        $match:{"result.ai_analysis.time_complexity":{$exists:true}}
                    },
                    {
                        $group:{_id:"result.ai_analysis.time_complexity",count:{$sum:1}}
                    },
                    {$sort:{count:-1}}
                ],
                spaceComplexity:[
                    {
                        $match:{"result.ai_analysis.space_complexity":{$exists:true}}
                    },
                    {
                        $group:{_id:"result.ai_analysis.space_complexity",count:{$sum:1}}
                    },
                    {$sort:{count:-1}}
                ],
            }}
        ]);
        const data=stats[0];
        res.json({
            overview:data.overview[0]||{
                totalAnalyses:0,
                totalFixes:0,
                averageRiskScore:0,
                totalIssues:0,
            },
            severity:data.severity[0]||{
                critical:0,
                high:0,
                medium:0,
                low:0
            },
            language:data.language||[],
            timeComplexity:data.timeComplexity||[],
            spaceComplexity:data.spaceComplexity||[]
        });
    }catch(error){
        console.error("Stats error:",error);
        res.status(500).json({message:"Failed to fetch stats"});
    }
}
