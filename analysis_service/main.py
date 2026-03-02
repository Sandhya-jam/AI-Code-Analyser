from fastapi import FastAPI
from pydantic import BaseModel
from analyzers.python_analyzer import analyze_python_code
from rules.rule_engine import apply_rules

app=FastAPI()

class CodeInput(BaseModel):
    source:str

@app.get("/health")
def health():
    return {"status":"Python service running"}

@app.post("/analyze")
def analyze_code(code:CodeInput):
    result=analyze_python_code(code.source)
    
    if "error" in result:
        return result
    
    rule_result=apply_rules(result,code.source)
    
    result["warnings"]=rule_result["warnings"]
    result["critical"]=rule_result["critical"]
    
    return result