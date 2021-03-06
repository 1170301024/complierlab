


class Symbols_Table:
    def __init__(self):

        # table是一个字典，键是标识符的名称，值是对应的Symbol_Table_Entry
        self.table = {}


    def add_symbol_entry(self, entry, line):
        '''
        将一个符号表条目加入到符号表中
        :param entry:
        :return:
        '''
        if entry.name in self.table.keys():
            from myparser.functions import Functions
            Functions.add_error(line, '变量重复声明')
        else:
            self.table[entry.get_name()] = entry

    def lookup(self, name):
        if name in self.table.keys():
            return self.table[name]
        return None



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
        return self.name


class Type:
    def __init__(self, type_str, width):
        self.type_str = type_str
        self.width = width

    def __eq__(self, other):
        if not isinstance(other, Type):
            raise TypeError
        return self.type_str == other.type_str and self.width == self.width

    def __str__(self):
        return self.type_str


class Array(Type):
    def __init__(self, type_str, num, stype):
        width = int(num) * stype.width
        super().__init__(type_str, width)
        self.num = num
        self.stype = stype
    def element(self):
        '''
        获得数组的中的子类型
        :return:
        '''
        return self.stype

    def __str__(self):
        return 'array('+ str(self.num) + ',' + str(self.stype) + ')'

class Struct(Type):
    def __init__(self, type_str, field_list):
        '''

        :param type_str:
        :param field_list: [(字段名和类型), ...]
        '''
        self.fields = {}
        width = 0
        for field in field_list:
            self.fields[field[0]] = field
            width += field[1].width
        super().__init__(type_str, width)
    def get_field(self, field_name):
        '''
        获得结构体中的特定字段
        :param field_name: 字符串类型
        :return:
        '''
        return self.fields[field_name]

    def __str__(self):
        str_list = []
        for key in self.fields.keys():
            field = self.fields[key]
            str_list.append('(%s * %s)' %(field[0],field[1]))
        str = ' * '.join(str_list)
        return 'struct('+str+')'


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

    def __str__(self):
        return 'pointer(%s)' %str(self.stype)

