import ast 

class PythonAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.functions=0
        self.function_metrics={}
        self.global_assigned=set()
        self.global_used=set()
        self.function_assigned={}
        self.function_used={}
        self.loops=0
        self.conditionals=0
        self.variables=set()
        self.recursion=False
        self.current_function=None
        self.max_depth=0
        self.current_depth=0
        self.cyclomatic_complexity=1
        self.function_returns={}
        
    def visit_FunctionDef(self,node):
        function_name=node.name
        self.function_assigned[function_name]=set()
        self.function_used[function_name]=set()
        
        self.function_returns[function_name]=False
        self.functions+=1
        
        self.current_function=function_name
        
        # Initialise fn metrics
        self.function_metrics[function_name]={
            "complexity":1,
            "lines":len(node.body),
            "nesting_depth":0
        }
        
        self.current_depth+=1
        self.max_depth=max(self.max_depth,self.current_depth)
        
        self.generic_visit(node)
        
        self.current_depth-=1
        self.current_function=None
        
    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target,ast.Name):
                if self.current_function:
                    self.function_assigned[self.current_function].add(target.id)
                else:
                    self.global_assigned.add(target.id)
        self.generic_visit(node)
        
    def visit_For(self, node):
        self.loops+=1
        self.cyclomatic_complexity+=1
        if self.current_function:
            self.function_metrics[self.current_function]["complexity"] += 1
        self._handle_nesting(node)
    
    def visit_While(self, node):
        self.loops+=1
        self.cyclomatic_complexity+=1
        if self.current_function:
            self.function_metrics[self.current_function]["complexity"] += 1
        self._handle_nesting(node)
    
    def visit_If(self, node):
        self.conditionals+=1
        self.cyclomatic_complexity+=1
        if self.current_function:
            self.function_metrics[self.current_function]["complexity"] += 1
        self._handle_nesting(node)
    
    def visit_Name(self,node):
        if isinstance(node.ctx,ast.Load):
            if self.current_function:
                self.function_used[self.current_function].add(node.id)
            else:
                self.global_used.add(node.id)
                
        self.variables.add(node.id)
        
        if self.current_function and node.id==self.current_function:
            self.recursion=True
        
        self.generic_visit(node)
    
    def _handle_nesting(self,node):
        self.current_depth+=1
        self.max_depth=max(self.current_depth,self.max_depth)
        self.generic_visit(node)
        self.current_depth-=1
        
    def visit_Return(self, node):
        if self.current_function:
            self.function_returns[self.current_function]=True
        self.generic_visit(node)

def analyze_python_code(source_code):
    try:
        lines=source_code.split("\n")
        
        total_lines=len(lines)
        blank_lines=sum(1 for line in lines if line.strip()=="")
        comment_lines=sum(1 for line in lines if line.strip().startswith("#"))
        
        tree=ast.parse(source_code)
        analyzer=PythonAnalyzer()
        analyzer.visit(tree)
        
        return{
            "total_lines":total_lines,
            "blank_lines":blank_lines,
            "comment_lines":comment_lines,
            
            "functions":analyzer.functions,
            "function_metrics":analyzer.function_metrics,
            "function_returns":analyzer.function_returns,
            
            "global_assigned":list(analyzer.global_assigned),
            "global_used":list(analyzer.global_used),
            "function_assigned":analyzer.function_assigned,
            "function_used":analyzer.function_used,
            
            "loops":analyzer.loops,
            "conditionals":analyzer.conditionals,
            "variables":list(analyzer.variables),
            "recursion":analyzer.recursion,
            "max_nesting_depth":analyzer.max_depth,
            "cyclomatic_complexity":analyzer.cyclomatic_complexity,
        }
    except SyntaxError as e:
        return{
            "error":"Syntax error",
            "details":str(e)
        }