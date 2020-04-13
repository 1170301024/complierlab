
# Node表示抽象语法树的内结点
class Node:
    def __init__(self):
        self.lex_line = 0
        self.grammar_symbol = 0
        sub_nodes = []

# 语句
class Stmt(Node):
    def __init__(self):
        super().__init__()



class Prog(Node):
    stmt1 = Stmt()
    stmt2 = Stmt()


# 控制流语句
class Ctrl(Stmt):
    pass



# 过程调用语句
class Proc_call(Stmt):

    pass

# 叶子节点

class leaf(Node):
    pass



