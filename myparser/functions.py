from myparser.type import Symbols_Table, Symbol_Table_Entry, Type


class Functions:

    def __init__(self):
        # 初始化指令为0
        self.quad = 0
        self.temp_label = 1
        self.instructions = []
        self.symbol_table = Symbols_Table()

        # label和label所在的指令索引
        self.label_dict = {}
        self.label_name_index = 0

    @staticmethod
    def triple2addr(triple):
        ops = ['+', '-', '*', '/']

        # x = y op z

        if triple[0]  in ops and (triple[1], triple[2]) != ('_', '_'):
            return "%s = %s %s %s" % (triple[3], triple[1], triple[2], triple[0])
        # x = op y
        elif triple[0] in ['+', '-'] :
            return "%s = %s %s" % (triple[3], triple[0], triple[1])

        # x = y
        elif triple[0] in ['=']:
            return "%s = %s" % (triple[3], triple[1])

        # goto L
        elif triple[0] == 'goto':
            return "goto %s" % (triple[1])

        # if x goto L
        elif triple[0] == 'jne':
            return "if %s != 0 goto %s" % (triple[1], triple[3])

        # params x
        elif triple[0] == 'params':
            return 'params %s' % (triple[1])

        # call p, n
        elif triple[0] == 'call':
            return 'call %s, %s' % (triple[1], triple[2])
        else:
            return str(triple) + '没有对应的三地址码'


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

    def newlabel(self, label_name=None):
        if label_name is not None:
            self.label_dict[label_name] = self.nextquad()
        else:
            label_name = 'L' + str(self.label_name_index)
            self.label_dict[label_name] = self.nextquad()


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
        entry = Symbol_Table_Entry(name, type, 0)
        self.symbol_table.add_symbol_entry(entry)

    # 类型转换
    def type_conversion(self, type1, type2):
        return True
