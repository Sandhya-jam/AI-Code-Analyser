import ast
import builtins

class PythonAnalyzer(ast.NodeVisitor):

    def __init__(self):

        self.functions = 0
        self.function_metrics = {}

        self.global_assigned = set()
        self.global_used = set()

        self.function_assigned = {}
        self.function_used = {}

        self.loops = 0
        self.conditionals = 0

        self.variables = set()

        self.recursion = False

        self.current_function = None

        self.max_depth = 0
        self.current_depth = 0

        self.cyclomatic_complexity = 1

        self.function_returns = {}

        # ignore builtin names like print, range
        self.builtin_names = set(dir(builtins))

        # scope tracking
        self.scope_stack = [{
            "type": "global",
            "name": "global",
            "assigned": set(),
            "used": set()
        }]

    def current_scope(self):
        return self.scope_stack[-1]

    def enter_scope(self, scope_type, name=None):

        self.scope_stack.append({
            "type": scope_type,
            "name": name,
            "assigned": set(),
            "used": set()
        })

    def exit_scope(self):

        scope = self.scope_stack.pop()

        if scope["type"] == "function":
            self.function_assigned[scope["name"]] = scope["assigned"]
            self.function_used[scope["name"]] = scope["used"]

        elif scope["type"] == "global":
            self.global_assigned.update(scope["assigned"])
            self.global_used.update(scope["used"])

    def visit_FunctionDef(self, node):

        function_name = node.name

        self.functions += 1

        self.enter_scope("function", function_name)

        self.current_function = function_name

        # parameters count as assigned
        for arg in node.args.args:
            self.current_scope()["assigned"].add(arg.arg)

        self.function_metrics[function_name] = {
            "complexity": 1,
            "lines": len(node.body),
            "nesting_depth": 0
        }

        self.function_returns[function_name] = False

        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)

        self.generic_visit(node)

        self.current_depth -= 1

        self.exit_scope()

        self.current_function = None

    def visit_Assign(self, node):

        for target in node.targets:

            if isinstance(target, ast.Name):
                self.current_scope()["assigned"].add(target.id)

        self.generic_visit(node)
        
    def visit_For(self, node):

        self.loops += 1
        self.cyclomatic_complexity += 1

        # assign loop variable
        if isinstance(node.target, ast.Name):
            self.current_scope()["assigned"].add(node.target.id)

        elif isinstance(node.target, ast.Tuple):
            for elt in node.target.elts:
                if isinstance(elt, ast.Name):
                    self.current_scope()["assigned"].add(elt.id)

        if self.current_function:
            self.function_metrics[self.current_function]["complexity"] += 1

        self._handle_nesting(node)

    def visit_While(self, node):

        self.loops += 1
        self.cyclomatic_complexity += 1

        if self.current_function:
            self.function_metrics[self.current_function]["complexity"] += 1

        self._handle_nesting(node)

    def visit_If(self, node):

        self.conditionals += 1
        self.cyclomatic_complexity += 1

        if self.current_function:
            self.function_metrics[self.current_function]["complexity"] += 1

        self._handle_nesting(node)

    def visit_Name(self, node):

        if node.id in self.builtin_names:
            self.generic_visit(node)
            return

        if isinstance(node.ctx, ast.Load):
            self.current_scope()["used"].add(node.id)

        self.variables.add(node.id)

        # recursion detection
        if self.current_function and node.id == self.current_function:
            self.recursion = True

        self.generic_visit(node)

    def _handle_nesting(self, node):

        self.current_depth += 1

        self.max_depth = max(self.current_depth, self.max_depth)

        self.generic_visit(node)

        self.current_depth -= 1

    def visit_Return(self, node):

        if self.current_function:
            self.function_returns[self.current_function] = True

        self.generic_visit(node)

def analyze_python_code(source_code):

    try:

        lines = source_code.split("\n")

        total_lines = len(lines)

        blank_lines = sum(1 for line in lines if line.strip() == "")

        comment_lines = sum(
            1 for line in lines if line.strip().startswith("#")
        )

        tree = ast.parse(source_code)

        analyzer = PythonAnalyzer()

        analyzer.visit(tree)

        global_scope = analyzer.scope_stack[0]

        analyzer.global_assigned.update(global_scope["assigned"])
        analyzer.global_used.update(global_scope["used"])

        return {

            "total_lines": total_lines,
            "blank_lines": blank_lines,
            "comment_lines": comment_lines,

            "functions": analyzer.functions,
            "function_metrics": analyzer.function_metrics,
            "function_returns": analyzer.function_returns,

            "global_assigned": list(analyzer.global_assigned),
            "global_used": list(analyzer.global_used),

            "function_assigned": analyzer.function_assigned,
            "function_used": analyzer.function_used,

            "loops": analyzer.loops,
            "conditionals": analyzer.conditionals,

            "variables": list(analyzer.variables),

            "recursion": analyzer.recursion,

            "max_nesting_depth": analyzer.max_depth,

            "cyclomatic_complexity": analyzer.cyclomatic_complexity
        }

    except SyntaxError as e:

        return {
            "error": "Syntax error",
            "details": str(e)
        }