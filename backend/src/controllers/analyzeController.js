import History from "../models/historyModel.js";
import { analyzeCode,fixCode } from '../services/pythonService.js';

export const analyze=async(req,res)=>{
    try {
    const result = await analyzeCode(req.body.code);

    const saved = await History.create({
      user:req.user,
      action:"analyze",
      language:"python",
      code:req.body.code,
      result
    });

    console.log("Saved to DB:", saved._id);

    res.json(result);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Analysis Failed" });
  }
};

export const fix=async(req,res)=>{
    try {
    console.log(req.body)
    const result = await fixCode(req.body.code);

    const saved = await History.create({
      user:req.user,
      action:"fix",
      language:"python",
      code:req.body.code,
      fixCode:result
    });

    console.log("Saved to DB:", saved._id);

    res.json(result);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Code Fix Failed Failed" });
  }
};

export const getUserhistory=async(req,res)=>{
   const history = await History.find({ user:req.user })
.sort({ createdAt:-1 });

   res.json(history);
};
