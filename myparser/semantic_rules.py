stack = []#= [{属性：值}]
top = 0 #栈顶



#    $   A    |   B   |   C   |   D  <- LR stack
#      addr :v|                      <- 属性
# #    type :t|
class Rules:
    '''
    语义规则类，包含所有的语义规则
    '''

    def primary_expression_rule_1(self):
        stack[top]['addr'] = lookup(stack[top].lexeme).getaddr()
    def postfix_expression_rule_1(self):
        pass
