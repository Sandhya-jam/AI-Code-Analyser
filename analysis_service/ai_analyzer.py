from groq import Groq
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()

client=Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL="llama-3.3-70b-versatile"

def extract_json(text):
    """
    Extract JSON safely from AI response
    """

    text = text.strip()

    # remove markdown blocks
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    # find JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return match.group(0)

    return text

def HelperFn(prompt,role):
    try:
        response=client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role":"system","content":role},
                {"role":"user","content":prompt}
            ],
            temperature=0
        )
        content=response.choices[0].message.content
        
        # Remove markdown code blocks
        if content.startswith("```"):
            content=content.split("```")[1]
            if content.startswith("json"):
                content=content[4:]
        
        content=content.strip()
        # attempt to prepare JSON
        try:
            return json.loads(content)
        except:
            return{
                "error":"AI returned non-JSON response",
                "raw_output":content
            }
    except Exception as e:
        return{
            "error":"AI analysis failed",
            "details":str(e)
        }

def analyze_code_with_ai(source_code:str):
    prompt=f"""
    You are an expert Python code reviewer.

Analyze the following Python code and return a JSON response.

Tasks:
1. Detect logical bugs
2. Estimate time complexity
3. Estimate space complexity
4. Suggest optimizations
5. Suggest bug fixes
6. Detect security vulnerabilities
7. Explain the code issues

Important rules:
- Do NOT treat Python builtins like print, len, range as variables.
- Avoid false positives like "used before assignment" for builtins.
- Assume variables like n, arr, input parameters may be defined elsewhere.
- Focus on meaningful issues only.

The system already performs static analysis for:

Do NOT repeat these issues unless deeper reasoning is required.
Focus on logical bugs, algorithm inefficiencies, and security issues.
-index out of range
- division by zero
- unused variables
- redundant assignments
- duplicate conditions
- unreachable code
- shadowed variables

Return STRICT JSON in this format:
Do NOT include markdown or explanations outside JSON.

Required JSON format:
{{
 "logical_bugs": [
    {{
   "issue": "",
   "line": "",
   "severity": ""
  }} 
 ],
 "time_complexity": "",
 "space_complexity": "",
 "security_issues": [
    {{
   "issue": "",
   "severity": ""
  }}
  ],
 "optimizations": [],
 "bug_fixes": [],
 "explanation": ""
}}

Code:
{source_code}
"""
    role="You are a strict JSON code analysis assistant."
    result=HelperFn(prompt,role)
    return result
        
def generate_fixed_code(source_code:str):
    prompt=f"""
    You are an expert Python code reviewer.

Your task is to fix and improve the following Python code.

Tasks:
1. Fix logical bugs
2. Fix syntax errors
3. Improve readability
4. Improve performance if possible
5. Follow Python best practices

IMPORTANT RULES:
- Return ONLY the corrected Python code.
- Do NOT include explanations.
- Do NOT include markdown formatting.

Return STRICT JSON in this format:
Do NOT include markdown or explanations outside JSON.

Code:
{source_code}

Required JSON format:
{{
    "fixed_code":""
}}
"""
    role="You fix Python code."
    result=HelperFn(prompt,role)
    return result