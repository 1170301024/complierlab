from myparser.type import Symbols_Table


class Functions:

    def __init__(self):
        # 初始化指令为0
        self.quad = 0
        self.temp_label = 1
        self.instructions = []
        self.symbol_table = Symbols_Table()

    # 回填相关
    def makelist(self, i):
        '''
        创建一个回填指令序号列表
        :param quad:
        :return:
        '''
        return [i, ]

    def merge(self, list1, list2):
        '''
        将两个列表合并，并且它的返回值为一个合并后的列表
        :param list1:
        :param list2:
        :return:
        '''
        return list1.extend(list2)

    def backpatch(self, list, quad):
        '''
        将quad作为目标标号插入到list所指列表中的各条指令中
        :param list:
        :param quad:
        :return:
        '''

        for i in list:
            inst = self.instructions[i]
            if inst[i][0] != 'goto_':
                raise TypeError
            self.instructions[i] = ('goto', '_', '_', quad)


    def nextquad(self, ):
        '''
        返回下一条指令
        :return:
        '''
        return self.quad

    # 三地址码
    def gen(self, op, arg1='_', arg2='_', result='_'):
        inst = (op, arg1, arg2, result)
        self.instructions.append(inst)

    # 符号表相关的
    def lookup(self, name):
        return self.symbol_table.lookup(name)

    def newtemp(self, ):
        label = 't' + str(self.temp_label)
        self.temp_label += 1
        return label


    def widen(self, addr, type1, type2):
        pass

    def enter(self, name, type):
        pass

    # 类型转换
    def type_conversion(self, type1, type2):
        pass
