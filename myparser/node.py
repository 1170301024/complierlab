
# Node表示抽象语法树的内结点
class Node:
    def __init__(self, symbol, lex_line = 0):
        self.lex_line = lex_line
        self.grammar_symbol = symbol
        self.sub_nodes = []
    def add_subnode(self, node):
        '''
        增加子结点
        :param node:
        :return:
        '''
        self.sub_nodes.append(node)
    def get_subnodes(self):
        '''
        获得该结点的所有子结点
        :return:
        '''
        return self.sub_nodes
    def __str__(self):
        return str(self.grammar_symbol)

# 语句
class Stmt(Node):
    pass



class Prog(Node):
    pass


# 控制流语句
class Ctrl(Stmt):
    pass



# 过程调用语句
class Proc_call(Stmt):

    pass

# 叶子节点

class leaf(Node):
    pass



