from myparser.functions import *

#    $   A    |   B   |   C   |   D  <- LR stack
#      addr :v|                      <- 属性
# #    type :t|
from myparser.type import Type, Array, Pointer, Struct, Function


class Rules:
    '''
    语义规则类，包含所有的语义规则
    '''

    def __init__(self):
        self.functions = Functions()
        self.temp_field = []
        self.temp_argument = []
        self.t = None
        self.args_list = []

    # 基本表达式
    def primary_expression_rule_1(self, stack, top):
        stack[top]['addr'] = self.functions.lookup(stack[top]['lexeme']).get_addr()
        stack[top]['type'] = self.functions.lookup(stack[top]['lexeme']).get_type()

    def primary_expression_rule_2(self, stack, top):

        stack[top]['addr'] = stack[top]['val']
        stack[top]['type'] = stack[top]['type']

    def primary_expression_rule_3(self, stack, top):
        
        stack[top-2]['addr'] = stack[top-1]['addr']
        stack[top-2]['type'] = stack[top-1]['type']
        top -= 2

    # 后缀表达式
    def postfix_expression_rule_1(self, stack, top):
        stack[top]['addr'] = stack[top]['addr']
        stack[top]['type'] = stack[top]['type']

    def postfix_expression_rule_2(self, stack, top):
        temp_addr = stack[top-3]['addr']
        stack[top-3]['addr'] = self.functions.newtemp()
        array_offset = self.functions.newtemp()
        self.functions.gen('*', stack[top-1]['addr'],stack[top-3]['type'].element().width, array_offset)
        self.functions.gen('+', temp_addr, array_offset, stack[top-3]['addr'])
        stack[top-3]['type'] = stack[top-3]['type'].element()
        top -= 3

    def postfix_expression_rule_3(self, stack, top):
        temp_addr = stack[top-3]['addr']
        stack[top-3]['addr'] = self.functions.newtemp()
        for r_args, f_args in zip(self.temp_argument, stack[top-3]['type'].get_params()):
            if self.functions.type_conversion(r_args,f_args): # 可以类型转化
                self.functions.gen('param',r_args[0])
            else:
                raise None # 参数类型不匹配
        self.functions.gen('call', temp_addr, len(self.temp_argument))
        stack[top-3]['type'] = stack[top-3]['type'].get_result_type()
        top -= 3

    def argument_expression_listopt(self, stack, top):
        stack.append({})


    def argument_expression_list_1(self, stack, top):
        self.temp_argument = [(stack[top]['addr'], stack[top]['type']),]

    def argument_expression_list_2(self, stack, top):
        self.temp_argument.append((stack[top]['addr'], stack[top]['type']))
        top -= 2

    # 一元表达式
    def unary_expression_1(self, stack, top):
        stack[top]['addr'] = stack[top]['addr']
        stack[top]['type'] = stack[top]['type']

    def unary_expression_2(self, stack, top):
        stack[top-1]['addr'] = self.functions.newtemp()
        self.functions.gen(stack[top-1]['op'], stack[top], result=stack[top-1]['addr'])
        top -= 1


    # 一元操作符
    def unary_operator_1(self, stack, top):
        stack[top]['op'] = '*'

    def unary_operator_2(self, stack, top):
        stack[top]['op'] = '+'

    def unary_operator_3(self, stack, top):
        stack[top]['op'] = '-'

    # cast表达式
    def cast_expression_1(self, stack, top):
        stack[top]['addr'] = stack[top]['addr']
        stack[top]['type'] = stack[top]['type']

    def cast_expression_2(self, stack, top):
        stack[top-3]['addr'] = self.functions.newtemp()
        self.functions.gen(stack[top-2]['addr'], stack[top]['addr'], result=stack[top-3]['addr'])
        stack[top-3]['type'] = stack[top]['type']
        top -= 3

    # 乘除表达式
    def multiplicative_expression_1(self, stack, top):
        stack[top]['addr'] = stack[top]['addr']
        stack[top]['type'] = stack[top]['type']

    def multiplicative_expression_2(self, stack, top):
        temp_addr = stack[top-2]['addr']
        temp_type = stack[top-2]['type']
        stack[top-2]['type'] = self.functions.max(temp_type, stack[top]['type'])
        a = self.functions.widen(temp_addr, temp_type, stack[top-2]['type'])
        b = self.functions.widen(stack[top]['addr'], stack[top]['type'], stack[top-2]['type'])
        stack[top-2]['addr'] = self.functions.newtemp()
        '''改了'''
        self.functions.gen('*', a, b, stack[top-2]['addr'])
        top -= 2

    def multiplicative_expression_3(self, stack, top):
        temp_addr = stack[top - 2]['addr']
        temp_type = stack[top - 2]['type']
        stack[top - 2]['type'] = self.functions.max(temp_type, stack[top]['type'])
        a = self.functions.widen(temp_addr, temp_type, stack[top - 2]['type'])
        b = self.functions.widen(stack[top]['addr'], stack[top]['type'], stack[top - 2]['type'])
        stack[top - 2]['addr'] = self.functions.newtemp()
        self.functions.gen('/', a, b, stack[top - 2]['addr'])
        top -= 2

    def multiplicative_expression_4(self, stack, top):
        temp_addr = stack[top - 2]['addr']
        temp_type = stack[top - 2]['type']
        stack[top - 2]['type'] = self.functions.max(temp_type, stack[top]['type'])
        a = self.functions.widen(temp_addr, temp_type, stack[top - 2]['type'])
        b = self.functions.widen(stack[top]['addr'], stack[top]['type'], stack[top - 2]['type'])
        stack[top - 2]['addr'] = self.functions.newtemp()
        self.functions.gen('%', a, b, stack[top - 2]['addr'])
        top -= 2

    def additive_expression_1(self, stack, top):
        stack[top]['addr'] = stack[top]['addr']
        stack[top]['type'] = stack[top]['type']

    def additive_expression_2(self, stack, top):
        temp_addr = stack[top - 2]['addr']
        temp_type = stack[top - 2]['type']
        stack[top - 2]['type'] = self.functions.max(temp_type, stack[top]['type'])
        a = self.functions.widen(temp_addr, temp_type, stack[top - 2]['type'])
        b = self.functions.widen(stack[top]['addr'], stack[top]['type'], stack[top - 2]['type'])
        stack[top - 2]['addr'] = self.functions.newtemp()
        self.functions.gen('+', a, b, stack[top - 2]['addr'])
        top -= 2

    def additive_expression_3(self, stack, top):
        temp_addr = stack[top - 2]['addr']
        temp_type = stack[top - 2]['type']
        stack[top - 2]['type'] = self.functions.max(temp_type, stack[top]['type'])
        a = self.functions.widen(temp_addr, temp_type, stack[top - 2]['type'])
        b = self.functions.widen(stack[top]['addr'], stack[top]['type'], stack[top - 2]['type'])
        stack[top - 2]['addr'] = self.functions.newtemp()
        self.functions.gen('-', a, b, stack[top - 2]['addr'])
        top -= 2

    # 关系操作符
    def relational_expression_1(self, stack, top):
        stack[top]['addr'] = stack[top]['addr']
        stack[top]['type'] = stack[top]['type']

    def relational_expression(self, stack, top):
        temp_addr = stack[top-2]['addr']
        stack[top-2]['addr'] = self.functions.newtemp()
        self.functions.gen(stack[top-1]['lexeme'],temp_addr,stack[top]['addr'],stack[top-2]['addr'])
        stack[top-2]['type'] = Type('int', 4)
        top -= 2

    # 等价操作符文法没实现，逻辑与、或没写完
    def logical_AND_expression_1(self, stack, top):
        stack[top]['addr'] = stack[top]['addr']
        stack[top]['type'] = stack[top]['type']

    def logical_AND_expression_2(self, stack, top):
        stack[top-2]['addr'] = self.functions.newtemp()
        '''需改正'''


    # 条件操作符

    # 赋值表达式
    def assignment_expression_1(self, stack, top):
        stack[top]['addr'] = stack[top]['addr']
        stack[top]['type'] = stack[top]['type']

    def assignment_expression_2(self, stack, top):
        self.functions.gen('=', stack[top]['addr'], result=stack[top-2]['addr'])
        stack[top]['addr'] = stack[top]['addr']
        stack[top]['type'] = stack[top]['type']

    # 赋值操作符
    def assignment_operator_1(self, stack, top):
        stack[top]['op'] = '='

    # 逗号操作符
    def expression_1(self, stack, top):
        stack[top]['addr'] = stack[top]['addr']
        stack[top]['type'] = stack[top]['type']

    def expression_2(self, stack, top):
        stack[top-2]['addr'] = stack[top]['addr']
        stack[top-2]['type'] = stack[top]['type']

    #语句和块
    def statement(self, stack, top):
        stack[top]['nextlist'] = stack[top]['nextlist']

    # compound statements
    def compound_statement_1(self, stack, top):
        stack[top-2]['nextlist'] = stack[top-1]['nextlist']

    def block_item_listopt_1(self, stack, top):
        stack[top]['nextlist'] = stack[top]['nextlist']

    def block_item_listopt_2(self, stack, top):
        stack[top]['nextlist'] = []

    def block_item_list_1(self, stack, top):
        stack[top]['nextlist'] = stack[top]['nextlist']

    def block_item_list_2(self, stack, top):
        self.functions.backpatch(stack[top - 1]['nextlist'], self.functions.nextquad())
        stack[top - 1]['nextlist'] = stack[top]['nextlist']

    def block_item_1(self, stack, top):
        stack[top]['nextlist'] = []

    def block_item_2(self, stack, top):
        stack[top]['nextlist'] = stack[top]['nextlist']

    # expression and null statements
    def expression_statement_1(self, stack, top):
        stack[top-1]['nextlist'] = []


    # selection statements
    def selection_statement_rule_1(self, stack, top):
        stack[top - 6]['nextlist'] = self.functions.merge(stack[top - 3]['falselist'], stack[top]['nextlist'])
        self.functions.backpatch(stack[top - 3]['truelist'], stack[top - 1]['quad'])

    def goto_M(self, stack, top):
        stack.append({})
        stack[top+1]['truelist'] = self.functions.makelist(self.functions.nextquad())
        stack[top+1]['falselist'] = self.functions.makelist(self.functions.nextquad()+1)
        self.functions.gen('jne', stack[top]['addr'], 0, 'goto_')
        self.functions.gen('goto_')
    def M_1(self, stack, top):
        stack.append({})
        stack[top+1]['quad'] = self.functions.nextquad()


    def selection_statement_rule_2(self, stack, top):
        stack[top - 9]['nextlist'] = self.functions.merge(self.functions.merge(stack[top - 4]['nextlist'],
                                                                               stack[top-3]['nextlist']),stack[top]['nextlist'])
        self.functions.backpatch(stack[top - 7]['truelist'], stack[top - 5]['quad'])
        self.functions.backpatch(stack[top - 7]['falselist'], stack[top - 1]['quad'])

    def N_1(self, stack, top):
        stack.append({})
        stack[top+1]['nextlist'] = self.functions.makelist(self.functions.nextquad())
        self.functions.gen('goto_')

    # iteration statements
    def iteration_statement_rule_1(self, stack, top):
        stack[top - 7]['nextlist'] = stack[top-3]['falselist']
        self.functions.backpatch(stack[top]['nextlist'], stack[top-6]['quad'])
        self.functions.backpatch(stack[top-3]['truelist'], stack[top - 1]['quad'])
        self.functions.gen('goto', result=stack[top-6]['quad'])

    # 声明
    def declaration_1(self, stack, top):
        self.functions.enter(stack[top-1]['lexeme'],stack[top-2]['type'])

    def type_1(self, stack, top):
        stack[top-2]['type'] = stack[top]['type']

    def M_2(self, stack, top):
        stack.append({})
        self.t = stack[top]['type']

    def type_2(self, stack, top):
        stack[top-1]['type'] = Pointer('pointer',stack[top-1]['type'])

    def type_3(self, stack, top):
        stack[top-3]['type'] = Struct('struct', self.temp_field)

    def struct_declaration_list_1(self, stack, top):
        self.temp_field = [(stack[top]['id'],stack[top]['type'])]

    def struct_declaration_list_2(self, stack, top):
        self.temp_field.append((stack[top]['id'],stack[top]['type']))

    def struct_declaration_1(self, stack, top):
        stack[top-2]['id'] = stack[top - 1]['lexeme']
        stack[top-2]['type'] = stack[top - 2]['type']

    def basic_1(self, stack, top):
        stack[top]['type'] = Type('int', 4)

    def basic_2(self, stack, top):
        stack[top]['type'] = Type('float', 4)

    def basic_3(self, stack, top):
        stack[top]['type'] = Type('void', 0)

    def basic_4(self, stack, top):
        stack[top]['type'] = Type('double', 8)

    def basic_5(self, stack, top):
        stack[top]['type'] = Type('char', 1)

    def C_1(self, stack, top):
        stack.append({})
        stack[top+1]['type'] = self.t

    def C_2(self, stack, top):
        stack[top-3]['type'] = Array('array',stack[top-2]['val'],stack[top]['type'])

    # 函数定义
    def function_definition(self, stack, top):
        stack[top-6]['type'] = Function('function',stack[top-5]['lexeme'],stack[top-6]['type'],self.args_list)
        self.functions.backpatch(stack[top]['nextlist'], self.functions.nextquad())
        self.functions.enter(stack[top-5]['lexeme'],stack[top-6]['type'])

    def args_listopt(self, stack, top):
        stack.append({})
        self.args_list = []

    def args_list_1(self, stack, top):
        self.args_list = []
        self.args_list.append((stack[top]['type'],stack[top]['id']))

    def args_list_2(self, stack, top):
        self.args_list.append((stack[top]['type'], stack[top]['id']))

    def args_1(self, stack, top):
        stack[top-1]['type'] = stack[top-1]['type']
        stack[top-1]['id'] = stack[top]['lexeme']

    def label_M(self, stack, top):
        stack.append({})
        self.functions.newlabel(stack[top-3]['lexeme'])
    # 常量
    def constant_rule_1(self, stack, top):
        stack[top]['type'] = Type('int', 4)
        stack[top]['val'] = stack[top]['val']

    def constant_rule_2(self, stack, top):
        stack[top]['type'] = Type('float', 4)
        stack[top]['val'] = stack[top]['val']

    def constant_rule_3(self, stack, top):
        stack[top]['type'] = Type('char', 1)
        stack[top]['val'] = stack[top]['val']

    def integer_constant_rule_1(self, stack, top):
        stack[top]['val'] = stack[top]['lexeme']

    def integer_constant_rule_2(self, stack, top):
        stack[top]['val'] = stack[top]['lexeme']

    def integer_constant_rule_3(self, stack, top):
        stack[top]['val'] = stack[top]['lexeme']

    def floating_constant_rule(self, stack, top):
        stack[top]['val'] = stack[top]['lexeme']

    def character_constant_rule(self, stack, top):
        stack[top]['val'] = stack[top]['lexeme']
