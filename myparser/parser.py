from myparser.cfg import Cfg
from myparser.item import Item
from lexer.Tag import Tag

class Parser:

    def __init__(self):
        # 产生式的集合
        self.cfg = Cfg()
        # 项集族
        self.item_family = []
        # ACTION函数
        self.actions = []
        # GOTO函数
        self.gotos = []

    def closure(self, i) -> []:
        '''
        求项集i的闭包
        :param i:项集 列表
        :return: 项集i的闭包的一个列表 []
        '''

        def first(a):
            '''
            获得从文法符号串a推到得到的串的首符号的集合(a 表示alpha)
            :param a:文法符号串
            :return: 终结符符号集合
            '''

    def goto(self, i, x) -> []:
        '''
        移入x时项集i的转换 [A -> a.Xp, a]
        :param i:项集
        :param x: 文法符号
        :return: 转换后的项集
        '''
        pass

    def items(self, G) -> [[]]:
        '''
        求G上的项集族
        :param G: 增广文法
        :return:
        '''
        # 初始化项集族为[G->.p, $]
        self.item_family = [self.closure(Item(G.start_symbol(), ['$'])),]
        for I in self.item_family:
            # 获得该项集中所有的下一个symbol
            all_symbols = []
            for i in I:
                one_symbol = i.next_symbol()
                if one_symbol is not None:
                    all_symbols += one_symbol
            for s in all_symbols:
                new_I = self.goto(I, s)
                if new_I is not None and new_I not in self.item_family:
                    self.item_family.append(new_I)



    def table(self, G):
        '''
        G的规范LR语法分析器的函数action和goto
        :param G:  增广文法
        :return:
        '''
        pass

    def program(self):
        '''
        进行语法分析
        :return:
        '''

        self.table(self.cfg)
        pass

