from myparser.functions import *
stack = [{}]
top = 3
class Rules:
    '''
    语义规则类，包含所有的语义规则
    '''
    # 基本表达式
    def primary_expression_rule_1(self):
        stack[top]['addr'] = lookup(stack[top]['lexeme'].get_addr())
        stack[top]['type'] = lookup(stack[top]['lexeme'].get_type())

    def primary_expression_rule_2(self):
        stack[top]['addr'] = stack[top]['addr']
        stack[top]['type'] = stack[top]['type']

    def primary_expression_rule_3(self):
        stack[top-2]['addr'] = stack[top-1]['addr']
        stack[top-2]['type'] = stack[top-1]['type']
        top -= 2

    # 后缀表达式
    def postfix_expression_rule_1(self):
        stack[top]['addr'] = stack[top]['addr']
        stack[top]['type'] = stack[top]['type']

    def postfix_expression_rule_2(self):
        temp_addr = stack[top-3]['addr']
        stack[top-3]['addr'] = temp()
        '''需指正'''
        array_offest_addr = temp()
        gen('*', stack[top-1]['addr'],stack[top-3]['type'].elem.width, array_offest_addr)
        gen('+', temp_addr, array_offest_addr, stack[top-3]['addr'])
        stack[top-3]['type'] = stack[top-3]['type'].elem
        top -= 3

    def postfix_expression_rule_3(self, postfix_expression, postfix_expression_1):
        temp_addr = stack[top-3]['addr']
        stack[top-3]['addr'] = temp()
        '''需改正'''
        temp_argument = [] # 参数列表，不该此处声明
        for r_args, f_args in zip(temp_argument,postfix_expression.type.get_argvs()):
            if can_trans(r_args,f_args): # 可以类型转化
                gen('param',r_args)
            else:
                raise None # 参数类型不匹配
            gen('call', temp_addr, len(temp_argument), stack[top-3]['addr'])
            '''改了'''
            stack[top-3]['type'] = stack[top-3]['type'].get_result_type()
        top -= 3

    def argument_expression_list_1(self,assiginment_expression):
        temp_argument = [assiginment_expression]

    def argument_expression_list_2(self,assiginment_expression):
        '''需改正'''
        temp_argument.append(assiginment_expression)

    # 一元表达式
    def unary_expression_1(self):
        stack[top]['addr'] = stack[top]['addr']
        stack[top]['type'] = stack[top]['type']

    def unary_expression_2(self):
        stack[top]['addr'] = temp()
        '''需改正'''
        top -= 1

    # 一元操作符
    def unary_operator_1(self):
        stack[top]['op'] = '*'

    def unary_operator_2(self):
        stack[top]['op'] = '+'

    def unary_operator_3(self):
        stack[top]['op'] = '-'

    # cast表达式
    def cast_expression_1(self):
        stack[top]['addr'] = stack[top]['addr']
        stack[top]['type'] = stack[top]['type']

    def cast_expression_2(self):
        stack[top-3]['addr'] = temp()
        gen(stack[top-2]['addr'], stack[top]['addr'], result=stack[top-3]['addr'])
        stack[top-3]['type'] = stack[top]['type']
        top -= 3

    # 乘除表达式
    def multiplicative_expression_1(self):
        stack[top]['addr'] = stack[top]['addr']
        stack[top]['type'] = stack[top]['type']

    def multiplicative_expression_2(self):
        temp_addr = stack[top-2]['addr']
        temp_type = stack[top-2]['type']
        stack[top-2]['type'] = max(temp_type, stack[top]['type'])
        a = widen(temp_addr, temp_type, stack[top-2]['type'])
        b = widen(stack[top]['addr'], stack[top]['type'], stack[top-2]['type'])
        stack[top-2]['addr'] = temp()
        '''改了'''
        gen('*', a, b, stack[top-2]['addr'])
        top -= 2

    def multiplicative_expression_3(self):
        temp_addr = stack[top - 2]['addr']
        temp_type = stack[top - 2]['type']
        stack[top - 2]['type'] = max(temp_type, stack[top]['type'])
        a = widen(temp_addr, temp_type, stack[top - 2]['type'])
        b = widen(stack[top]['addr'], stack[top]['type'], stack[top - 2]['type'])
        stack[top - 2]['addr'] = temp()
        '''改了'''
        gen('/', a, b, stack[top - 2]['addr'])
        top -= 2

    def multiplicative_expression_4(self):
        temp_addr = stack[top - 2]['addr']
        temp_type = stack[top - 2]['type']
        stack[top - 2]['type'] = max(temp_type, stack[top]['type'])
        a = widen(temp_addr, temp_type, stack[top - 2]['type'])
        b = widen(stack[top]['addr'], stack[top]['type'], stack[top - 2]['type'])
        stack[top - 2]['addr'] = temp()
        '''改了'''
        gen('%', a, b, stack[top - 2]['addr'])
        top -= 2

    def additive_expression_1(self):
        stack[top]['addr'] = stack[top]['addr']
        stack[top]['type'] = stack[top]['type']

    def additive_expression_2(self):
        temp_addr = stack[top - 2]['addr']
        temp_type = stack[top - 2]['type']
        stack[top - 2]['type'] = max(temp_type, stack[top]['type'])
        a = widen(temp_addr, temp_type, stack[top - 2]['type'])
        b = widen(stack[top]['addr'], stack[top]['type'], stack[top - 2]['type'])
        stack[top - 2]['addr'] = temp()
        '''改了'''
        gen('+', a, b, stack[top - 2]['addr'])
        top -= 2

    def additive_expression_3(self):
        temp_addr = stack[top - 2]['addr']
        temp_type = stack[top - 2]['type']
        stack[top - 2]['type'] = max(temp_type, stack[top]['type'])
        a = widen(temp_addr, temp_type, stack[top - 2]['type'])
        b = widen(stack[top]['addr'], stack[top]['type'], stack[top - 2]['type'])
        stack[top - 2]['addr'] = temp()
        '''改了'''
        gen('-', a, b, stack[top - 2]['addr'])
        top -= 2

    # 关系操作符
    def relational_expression_1(self):
        stack[top]['addr'] = stack[top]['addr']
        stack[top]['type'] = stack[top]['type']

    def relational_expression_2(self):
        temp_addr = stack[top-2]['addr']
        stack[top-2]['addr'] = temp()
        '''改了'''
        gen('<',temp_addr,stack[top]['addr'],stack[top-2]['addr'])
        '''需改正'''
        stack[top-2]['type'] = INT
        top -= 2

    def relational_expression_3(self):
        temp_addr = stack[top-2]['addr']
        stack[top-2]['addr'] = temp()
        '''改了'''
        gen('>',temp_addr,stack[top]['addr'],stack[top-2]['addr'])
        '''需改正'''
        stack[top-2]['type'] = INT
        top -= 2

    def relational_expression_4(self):
        temp_addr = stack[top-2]['addr']
        stack[top-2]['addr'] = temp()
        '''改了'''
        gen('<=',temp_addr,stack[top]['addr'],stack[top-2]['addr'])
        '''需改正'''
        stack[top-2]['type'] = INT
        top -= 2

    def relational_expression_5(self):
        temp_addr = stack[top-2]['addr']
        stack[top-2]['addr'] = temp()
        '''改了'''
        gen('>=',temp_addr,stack[top]['addr'],stack[top-2]['addr'])
        '''需改正'''
        stack[top-2]['type'] = INT
        top -= 2

    # 等价操作符文法没实现，逻辑与、或没写完
    def logical_AND_expression_1(self):
        stack[top]['addr'] = stack[top]['addr']
        stack[top]['type'] = stack[top]['type']

    def logical_AND_expression_2(self):
        stack[top-2]['addr'] = temp()
        '''需改正'''

        top -= 2

    # 条件操作符

    # 赋值表达式
    def assignment_expression_1(self):
        stack[top]['addr'] = stack[top]['addr']
        stack[top]['type'] = stack[top]['type']

    def assignment_expression_2(self):
        gen('=', stack[top]['addr'], result=stack[top-2]['addr'])
        '''改了'''
        stack[top]['addr'] = stack[top]['addr']
        stack[top]['type'] = stack[top]['type']

    # 赋值操作符
    def assignment_operator_1(self):
        stack[top]['op'] = '='

    # 逗号操作符
    def expression_1(self):
        stack[top]['addr'] = stack[top]['addr']
        stack[top]['type'] = stack[top]['type']

    def expression_2(self):
        stack[top-2]['addr'] = stack[top]['addr']
        stack[top-2]['type'] = stack[top]['type']
        top -= 2

    # selection statements
    def selection_statement_rule_1(self):
        stack[top - 5]['nextlist'] = merge(stack[top - 3]['falselist'], stack[top]['nextlist'])
        backpatch(stack[top - 3]['falselist'], stack[top - 1]['quad'])
        top -= 5


    def selection_statement_rule_2(self):
        stack[top - 9]['nextlist'] = merge(merge(stack[top - 4]['nextlist'], stack[top-3]['nextlist']),stack[top]['nextlist'])
        backpatch(stack[top - 7]['truelist'], stack[top - 5]['quad'])
        backpatch(stack[top - 7]['falselist'], stack[top - 1]['quad'])
        stack[top - 3]['nextlist'] = makelist('nextquad')
        top -= 9

    # iteration statements
    def iteration_statement_rule_1(self):
        stack[top - 7]['nextlist'] = stack[top-3]['falselist']
        backpatch(stack[top]['nextlist'], stack[top-5]['quad'])
        backpatch(stack[top-3]['nextlist'], stack[top - 1]['quad'])
        top -= 6

