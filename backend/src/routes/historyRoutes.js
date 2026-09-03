import express, { Router } from 'express'
import { analyze,fix} from '../controllers/analyzeController.js'
import { getUserhistory,getHistoryById,getHistoryStats } from '../controllers/historyController.js'
import { protect } from '../middleware/authMiddleware.js';
const router=Router();

router.post("/analyze",protect,analyze)
router.post("/fix",protect,fix)
router.get("/history",protect,getUserhistory)
router.get("/history/stats",protect,getHistoryStats)
router.get("/history/:id",protect,getHistoryById)

export default router;