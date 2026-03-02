# AI-Enhanced Static Code Analysis & Optimization Engine

A full-stack system that performs static code analysis using:

- AST parsing
- Rule-based bug detection
- Time complexity estimation
- AI-powered optimization suggestions

## Tech Stack

Frontend:
- React (Vite)

Backend:
- Node.js
- Express
- MongoDB

Analysis Engine:
- Python
- FastAPI

## Architecture

Frontend → Node Backend → Python Analysis Service → MongoDB

## Setup Instructions

### Backend
cd backend  
npm install  
npm run dev  

### Frontend
cd frontend  
npm install  
npm run dev  

### Python Service
cd analysis-service  
python -m venv venv  
venv\Scripts\activate  
pip install fastapi uvicorn  
uvicorn main:app --reload --port 8000  