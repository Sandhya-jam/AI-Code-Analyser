from fastapi import FastAPI
from pydantic import BaseModel
from analyzers.python_analyzer import analyze_python_code
from rules.rule_engine import apply_rules,calculate_risk_score
from ai_analyzer import analyze_code_with_ai,generate_fixed_code
from utils.ai_filter import filter_ai_results
from utils.ai_severity_processor import merge_ai_findings

app=FastAPI()

class CodeInput(BaseModel):
    source:str

@app.get("/health")
def health():
    return {"status":"Python service running"}

@app.post("/analyze")
def analyze_code(code:CodeInput):
    result=analyze_python_code(code.source)
    
    critical=[]
    high=[]
    medium=[]
    low=[]
    if result.get("syntax_error"):
        pass
    else:
        rule_result=apply_rules(result,code.source)
    
        for f in rule_result:
            
            if f["severity"]=="CRITICAL":
                critical.append(f)
            elif f["severity"]=="HIGH":
                high.append(f)
            elif f["severity"]=="MEDIUM":
                medium.append(f)
            elif f["severity"]=="LOW":
                low.append(f)
                
    # ai_result=analyze_code_with_ai(code.source)
    # ai_result=filter_ai_results(
    #     ai_result,
    #     {
    #         "critical":critical,
    #         "high":high,
    #         "medium":medium,
    #         "low":low
    #     }
    # )
    
    # critical,high,medium,low=merge_ai_findings(
    #     ai_result,
    #     critical,
    #     high,
    #     medium,
    #     low
    # )
    risk_score=calculate_risk_score(result,critical,high,medium,low)
    
    return{
        "analysis":result,
        "critical":critical,
        "high":high,
        "medium":medium,
        "low":low,
        "risk_score":risk_score,
        # "ai_analysis":ai_result
    }
    
@app.post("/fix")
def fix_code(code: CodeInput):

    try:
        fixed = generate_fixed_code(code.source)

        return fixed

    except Exception as e:

        print("Fix error:", e)

        return {
            "error": "AI code fix failed",
            "details": str(e)
        }