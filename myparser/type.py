

class Symbols_Table:
    def __init__(self):
        # table是一个字典，键是标识符的名称，值是对应的Symbol_Table_Entry
        self.table = dict()

    def add_symbol_entry(self, entry):
        '''
        将一个符号表条目加入到符号表中
        :param entry:
        :return:
        '''
        if entry.name in self.table.keys():
            raise TypeError
        else:
            self.table[entry.name] = entry

    def lookup(self, name):
        if name not in self.table.keys():
            raise TypeError
        return self.table[name]



class Symbol_Table_Entry:
    def __init__(self, name, type, addr):
        self.name = name
        self.type = type
        self.addr = addr

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_addr(self):
        return self.addr

    def __eq__(self, other):
        if not isinstance(Symbol_Table_Entry, other):
            return False
        if (self.name, self.type, self.addr) == (other.name, other.type, other.addr):
            return True
        return False

    def __str__(self):
        return '(%s, %s, %s)' % (self.name , self.type, self.addr)


class Type:
    def __init__(self, type_str, width):
        self.type_str = type_str
        self.width = width

    def __eq__(self, other):
        if not isinstance(Type, other):
            return False
        if other.type_str == self.type_str :
            return True
        return False
    def __str__(self):
        return self.type_str + str(self.width)

class Array(Type):
    def __init__(self, type_str, num, stype):
        width = num * stype.width
        super().__init__(type_str, width)
        self.num = num
        self.stype = stype
    def element(self):
        '''
        获得数组的中的子类型
        :return:
        '''
        return self.stype

class Struct(Type):
    def __init__(self, type_str, field_list):
        '''

        :param type_str:
        :param field_list: [(字段名和类型), ...]
        '''
        self.fields = {}
        width = 0
        for field in field_list:
            self.fields[field[0]] = field[1]
            width += field[1].width
        super().__init__(type_str, width)
    def get_field(self, field_name):
        '''
        获得结构体中的特定字段
        :param field_name: 字符串类型
        :return:
        '''
        return self.fields[field_name]


class Function(Type):
    def __init__(self, type_str, name, result_type, params_list):
        '''

        :param type_str:
        :param name:
        :param result_type:
        :param params_list: [(type,id)]
        '''
        super().__init__(type_str, width=0)
        self.identify = name
        self.result_type = result_type
        self.params_list = params_list
    def get_result_type(self):
        '''
        获得函数的返回值类型
        :return:
        '''
        return self.result_type

    def get_params(self):
        '''
        获得函数的参数列表
        :return:
        '''
        return self.params_list

class Pointer(Type):
    """
    Pointer类用于
    """
    def __init__(self, type_str, stype):
        super().__init__(type_str, width=8)
        self.type_str = type_str
        self.stype = stype

