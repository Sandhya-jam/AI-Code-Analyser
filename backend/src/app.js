import express from 'express'
import cors from 'cors'
import authRoutes from './routes/authRoutes.js'
import historyRoutes from './routes/historyRoutes.js'

const app=express();

app.use(cors())
app.use(express.json());

app.use("/api/auth",authRoutes)
app.use("/api/code",historyRoutes)

app.get("/health",(req,res)=>{
    res.json({status:"Backend Running"});
});

export default app;