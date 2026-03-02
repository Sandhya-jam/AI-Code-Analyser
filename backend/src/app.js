import express from 'express'
import cors from 'cors'
import { analyzeCode } from './services/pythonService.js';
import codeReport from './models/codeReport.js';
const app=express();

app.use(cors())
app.use(express.json());

app.post("/analyze",async(req,res)=>{
    try {
    const result = await analyzeCode(req.body.code);

    const saved = await codeReport.create({
      sourceCode: req.body.code,
      analysisResult: result
    });

    console.log("Saved to DB:", saved._id);

    res.json(result);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Analysis Failed" });
  }
});
app.get("/health",(req,res)=>{
    res.json({status:"Backend Running"});
});

export default app;