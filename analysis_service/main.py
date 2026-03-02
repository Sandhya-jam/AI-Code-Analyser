from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

class CodeInput(BaseModel):
    source:str

@app.get("/health")
def health():
    return {"status":"Python service running"}

@app.post("/analyze")
def analyze_code(code:CodeInput):
    return{
        "message":"Code received",
        "length":len(code.source)
    }