from fastapi import FastAPI
from pydantic import BaseModel
from analyzers.python_analyzer import analyze_python_code
from rules.rule_engine import apply_rules,calculate_risk_score

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
    
    critical=[]
    high=[]
    medium=[]
    low=[]
    
    for f in rule_result:
        
        if f["severity"]=="CRITICAL":
            critical.append(f)
        elif f["severity"]=="HIGH":
            high.append(f)
        elif f["severity"]=="MEDIUM":
            medium.append(f)
        elif f["severity"]=="LOW":
            low.append(f)
            
    risk_score=calculate_risk_score(result,critical,high,medium,low)
    
    return{
        "analysis":result,
        "critical":critical,
        "high":high,
        "medium":medium,
        "low":low,
        "risk_score":risk_score
    }
