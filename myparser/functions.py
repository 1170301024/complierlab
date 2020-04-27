from myparser.type import Symbols_Table, Symbol_Table_Entry, Type


class Functions:

    def __init__(self):
        # 初始化指令为0
        self.quad = 0
        self.temp_label = 1
        self.instructions = []
        self.symbol_table = Symbols_Table()
        self.i = 0

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
        list = []
        list.extend(list1)
        list.extend(list2)
        return list

    def backpatch(self, list, quad):
        '''
        将quad作为目标标号插入到list所指列表中的各条指令中
        :param list:
        :param quad:
        :return:
        '''

        for i in list:
            inst = self.instructions[i]
            print(inst)
            if inst[0] == 'goto_':
                self.instructions[i] = ('goto', '_', '_', quad)
            elif inst[3] == 'goto_':
                self.instructions[i] = (inst[0], inst[1], inst[2], quad)
            else:
                raise TypeError

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
        self.quad += 1

    # 符号表相关的
    def lookup(self, name):
       return self.symbol_table.lookup(name)

    def newtemp(self, ):
        label = 't' + str(self.temp_label)
        self.temp_label += 1
        return label

    def max(self, type1, type2):
        if not isinstance(type1, Type) or not isinstance(type2, Type):
            raise TypeError
        priority_list = [Type('double',8),Type('float',4),Type('int',4),Type('char',1)]
        index_type1 = priority_list.index(type1)
        index_type2 = priority_list.index(type2)
        return priority_list[max(index_type1,index_type2)]

    def widen(self, addr, type1, type2):
        if not isinstance(type1, Type) or not isinstance(type2, Type):
            raise TypeError
        if type1 == type2:
            return addr
        priority_list = [Type('double',8),Type('float',4),Type('int',4),Type('char',1)]
        if type1 == priority_list[2] or type1 == priority_list[3]:
            pass


    def enter(self, name, type):
        self.i += 1
        entry = Symbol_Table_Entry(name, type, 0)
        self.symbol_table.add_symbol_entry(entry)

    # 类型转换
    def type_conversion(self, type1, type2):
        return True
