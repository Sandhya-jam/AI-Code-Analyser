import express, { Router } from 'express'
import { analyze,fix,getUserhistory } from '../controllers/analyzeController.js'
import { protect } from '../middleware/authMiddleware.js';
const router=Router();

router.post("/analyze",protect,analyze)
router.post("/fix",protect,fix)
router.get("/history",protect,getUserhistory)

export default router;