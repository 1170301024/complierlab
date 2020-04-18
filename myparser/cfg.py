from lexer.Tag import Tag
from token import Token


class Cfg:
    '''
    G = (V, E, R, S)
    V 是非终结符集合
    E 是终结符集合
    R 是产生式集合
    S 是开始符号
    '''
    def __init__(self):

        # 非终结符
        self.V = []
        # 终结符集合
        self.E = []
        # 产生式集合
        self.R = []
        # 开始符号
        self.S = Nonterminal("G'")
        self.grammer()

    # def grammer(self):
    #     def reserve(header, body):
    #         self.R.append(Production(header, body))
    #
    #     reserve(Nonterminal('G'), [Nonterminal('S')])
    #     reserve(Nonterminal('S'), [Nonterminal('C'), Nonterminal('C')])
    #     reserve(Nonterminal('C'), [Terminal(0, 'c'), Nonterminal('C')])
    #     reserve(Nonterminal('C'), [Terminal(1, 'd')])

    def grammer(self):
        def reserve(header, body):
            self.R.append(Production(header, body))
        # 增广文法
        reserve(Nonterminal("G'"), [Nonterminal('G')])
        reserve(Nonterminal('G'), [Nonterminal('program')])
        reserve(Nonterminal('program'), [Nonterminal('program'),Nonterminal('program')])
        reserve(Nonterminal('program'),[Nonterminal('declaration')])
        reserve(Nonterminal('program'), [Nonterminal('function-definition')])

        # 基本表达式
        # primary-expression -> ID | constant | string-literal | ( expression )
        for i in [[Terminal(Tag.ID,'ID')],[Nonterminal('constant')],
                  [Nonterminal('string-literal')],[Terminal(Tag.SLP,'('),Nonterminal('expression'),Terminal(Tag.SRP,')')]]:
            reserve(Nonterminal('primary-expression'),i)

        # 后缀操作符
        # postfix-expression -> primary-expression
        # postfix-expression -> postfix-expression[expression]
        # postfix-expression -> postfix-expression(argument-expression-listopt)
        # postfix-expression -> postfix-expression . ID
        # postfix-expression -> postfix-expression -> ID
        # postfix-expression -> postfix-expression ++
        # postfix-expression -> postfix-expression --
        # argument-expression-listopt -> argument-expression-list | e
        # argument-expression-list -> assignment-expression
        # argument-expression-list -> argument-expression-list, assignment-expression
        reserve(Nonterminal('postfix-expression'),
                [Nonterminal('primary-expression')])
        reserve(Nonterminal('postfix-expression'),
                [Nonterminal('postfix-expression'),Terminal(Tag.LRP,'['),Nonterminal('expression'),Terminal(Tag.RRP,']')])
        reserve(Nonterminal('postfix-expression'),
                [Nonterminal('postfix-expression'),Terminal(Tag.SLP,'('),Nonterminal("argument-expression-listopt"),Terminal(Tag.SRP,')')])

        reserve(Nonterminal('argument-expression-listopt'),
                [Nonterminal('argument-expression-list')])
        reserve(Nonterminal('argument-expression-listopt'),
                [Empty()])
        reserve(Nonterminal('argument-expression-list'),
                [Nonterminal('assignment-expression')])
        reserve(Nonterminal('argument-expression-list'),
                [Nonterminal('argument-expression-list'),Terminal(Tag.COM,','),Nonterminal('assignment-expression')])
        # 一元操作符
        # unary-expression -> postfix-expression
        # unary-expression -> ++ unary-expression
        # unary-expression -> -- unary-expression
        # unary-expression -> unary-operator cast-expression
        # unary-operator -> & | * | + |-| ~ | !
        reserve(Nonterminal('unary-expression'),
                [Nonterminal('postfix-expression')])
        reserve(Nonterminal('unary-expression'),
                [Nonterminal('unary-operator'),Nonterminal('cast-expression')])
        for i in [[Terminal(Tag.MUILT,'*')],[Terminal(Tag.ADD,'+')],[Terminal(Tag.SUB,'-')]]:
            reserve(Nonterminal('unary-operator'),i)

        # cast 操作符
        # cast-expression -> unary-expression
        # cast-expression -> (type-name) cast-expression
        reserve(Nonterminal('cast-expression'),
                [Nonterminal('unary-expression')])
        reserve(Nonterminal('cast-expression'),
                [Terminal(Tag.SLP,'('),Nonterminal('type-name'),
                 Terminal(Tag.SRP,')'),Nonterminal("cast-expression")])

        # 乘除表达式
        # multiplicative-expression -> cast-expression
        # multiplicative-expression -> multiplicative-expression * cast-expression
        # multiplicative-expression -> multiplicative-expression / cast-expression
        # multiplicative-expression -> multiplicative-expression % cast-expression
        reserve(Nonterminal('multiplicative-expression'),
                [Nonterminal('cast-expression')])
        reserve(Nonterminal('multiplicative-expression'),
                [Nonterminal('multiplicative-expression'),Terminal(Tag.MUILT,'*'),Nonterminal('cast-expression')])
        reserve(Nonterminal('multiplicative-expression'),
                [Nonterminal('multiplicative-expression'),Terminal(Tag.DIV,'/'),Nonterminal('cast-expression')])
        reserve(Nonterminal('multiplicative-expression'),
                [Nonterminal('multiplicative-expression'),Terminal(Tag.MOD,'%'),Nonterminal('cast-expression')])


        # 加减表达式
        # additive-expression -> multiplicative-expression
        # additive-expression -> additive-expression + multiplicative-expression
        # additive-expression -> additive-expression-multiplicative-expression
        reserve(Nonterminal('additive-expression'),
                [Nonterminal('multiplicative-expression')])
        reserve(Nonterminal('additive-expression'),
                [Nonterminal('additive-expression'), Terminal(Tag.ADD, '+'), Nonterminal('multiplicative-expression')])
        reserve(Nonterminal('additive-expression'),
                [Nonterminal('additive-expression'), Terminal(Tag.SUB, '-'), Nonterminal('multiplicative-expression')])

        # 移位操作符
        # shift-expression -> additive-expression
        # shift-expression -> shift-expression << additive-expression
        # shift-expression -> shift-expression >> additive-expression(h)
        # reserve(Nonterminal('shift-expression'), [Nonterminal('additive-expression')])
        # reserve(Nonterminal('shift-expression'), [Nonterminal('additive-expression')])

        # 关系操作符
        # relational-expression -> additive-expression
        # relational-expression -> relational-expression < additive-expression
        # relational-expression -> relational-expression > additive-expression
        # relational-expression -> relational-expression <= additive-expression
        # relational-expression -> relational-expression >= additive-expression
        reserve(Nonterminal('relational-expression'),
                [Nonterminal('additive-expression')])
        reserve(Nonterminal('relational-expression'),
                [Nonterminal('relational-expression'),Terminal(Tag.REL,'REL'),Nonterminal('additive-expression')])

        # 等价操作符
        # equality-expression -> relational-expression
        # equality-expression -> equality-expression == relational-expression
        # equality-expression -> equality-expression != relational-expression
        # 位与操作符
        # AND-expression -> relational-expression
        # AND-expression -> AND-expression & relational-expression
        # 位异或操作符
        # exclusive-OR-expression -> AND-expression
        # exclusive-OR-expression -> exclusive-OR-expression ^ AND-expression
        # 位或操作符
        # inclusive-OR-expression -> exclusive-OR-expression
        # inclusive-OR-expression -> inclusive-OR-expression | exclusive-OR-expression

        # 逻辑与操作符
        # logical-AND-expression -> relational-expression
        # logical-AND-expression -> logical-AND-expression && relational-expression
        reserve(Nonterminal('logical-AND-expression'),
                [Nonterminal('relational-expression')])
        reserve(Nonterminal('logical-AND-expression'),
                [Nonterminal('logical-AND-expression'),Terminal(Tag.AND,'&&'),Nonterminal('relational-expression')])

        # 逻辑或操作符
        # logical-OR-expression -> logical-AND-expression
        # logical-OR-expression -> logical-OR-expression || logical-AND-expression
        reserve(Nonterminal('logical-OR-expression'),
                [Nonterminal('logical-AND-expression')])
        reserve(Nonterminal('logical-OR-expression'),
                [Nonterminal('logical-OR-expression'), Terminal(Tag.OR, '||'), Nonterminal('logical-AND-expression')])

        # 条件操作符
        # conditional-expression -> logical-OR-expression
        # conditional-expression -> logical-OR-expression ? expression: conditional-expression
        reserve(Nonterminal('conditional-expression'),
                [Nonterminal('logical-OR-expression')])
        reserve(Nonterminal('conditional-expression'),
                [Nonterminal('logical-OR-expression'), Terminal(Tag.QM, '?'),
                 Nonterminal('expression'),Terminal(Tag.COL, ':'),Nonterminal('conditional-expression')])

        # 赋值操作符
        # assignment-expression -> conditional-expression
        # assignment-expression -> unary-expression assignment-operator assignment-expression
        # assignment-operator -> = | *= | /= | %= | += | -= | <<= | >>= | &= | ^= | |=
        reserve(Nonterminal('assignment-expression'),
                [Nonterminal('conditional-expression')])
        reserve(Nonterminal('assignment-expression'),
                [Nonterminal('assignment-expression'),Nonterminal('assignment-operator'),Nonterminal('assignment-expression')])
        for i in [[Terminal(Tag.ASSIGN,'=')],
                  [Terminal(Tag.MUILT,'*'),Terminal(Tag.ASSIGN,'=')],
                  [Terminal(Tag.DIV,'/'),Terminal(Tag.ASSIGN,'=')],
                  [Terminal(Tag.MOD,'%'),Terminal(Tag.ASSIGN,'=')],
                  [Terminal(Tag.ADD,'+'),Terminal(Tag.ASSIGN,'=')],
                  [Terminal(Tag.SUB,'-'),Terminal(Tag.ASSIGN,'=')]]:
            reserve(Nonterminal('assignment-operator'), i)

        # 逗号操作符
        # expression -> assignment-expression
        # expression -> expression, assignment-expression
        # expressionopt -> expression | e
        reserve(Nonterminal('expression'),
                [Nonterminal('assignment-expression')])
        reserve(Nonterminal('expression'),
                [Nonterminal('expression'),Terminal(Tag.COM,','),Nonterminal('assignment-expression')])
        reserve(Nonterminal('expressionopt'),
                [Nonterminal('expression')])
        reserve(Nonterminal('expressionopt'),
                [Empty()])

        # 2.常量表达式
        # constant-expression -> conditional-expression
        reserve(Nonterminal('constant-expression'),
                [Nonterminal('conditional-expression')])


        # 3.声明
        # declaration -> declaration-specifiers init-declarator-listopt ;
        # declaration-specifiers -> type-specifier declaration-specifiersopt
        # declaration-specifiersopt -> declaration-specifiers | e
        # init-declarator-list -> init-declarator
        # init-declarator-list -> init-declarator-list, init-declarator
        # init-declarator -> declarator
        # init-declaractor -> declarator = initializer
        reserve(Nonterminal('declaration'),
                [Nonterminal('declaration-specifiers'),Nonterminal('init-declarator-listopt'),Terminal(Tag.SEMI,';')])
        reserve(Nonterminal('declaration-specifiers'),
                [Nonterminal('type-specifier'), Nonterminal('declaration-specifiersopt')])
        reserve(Nonterminal('declaration-specifiersopt'),
                [Nonterminal('declaration-specifiers')])
        reserve(Nonterminal('declaration-specifiersopt'),
                [Empty()])
        reserve(Nonterminal('init-declarator-list'),
                [Nonterminal('init-declarator')])
        reserve(Nonterminal('init-declarator-list'),
                [Nonterminal('init-declarator-list'),Terminal(Tag.COM,','),Nonterminal('init-declarator')])
        reserve(Nonterminal('init-declarator'),
                [Nonterminal('declarator')])
        reserve(Nonterminal('init-declarator'),
                [Nonterminal('declarator'),Terminal(Tag.ASSIGN,'='),Nonterminal('initializer')])
        reserve(Nonterminal('init-declarator-listopt'),
                [Nonterminal('init-declarator-list')])
        reserve(Nonterminal('init-declarator-listopt'),
                [Empty()])

        # 类型标识符
        # type-specifier -> VOID | CHAR | SHORT | INT | LONG | FLOAT | DOUBLE | SIGNED | UNSIGNED
        # type-specifier -> struct-or-union-specifier
        # struct-or-union-specifier -> struct-or-union  { struct-declaration-list }
        # struct-or-union-specifier -> struct-or-union ID
        # IDopt -> ID | e
        # struct-or-union -> STRUCT | UNION
        for i in [[Terminal(Tag.VOID,'VOID')],[Terminal(Tag.CHAR,'CHAR')],[Terminal(Tag.SHORT,'SHORT')],
                  [Terminal(Tag.INT,'INT')],[Terminal(Tag.LONG,'LONG')],[Terminal(Tag.FLOAT,'FLOAT')],
                  [Terminal(Tag.DOUBLE,'DOUBLE')],[Terminal(Tag.SIGNED,'SIGNED')],[Terminal(Tag.UNSIGNED,'UNSIGNED')]]:
            reserve(Nonterminal('type-specifier'),i)
        reserve(Nonterminal('type-specifier'),
                [Nonterminal('struct-or-union-specifier')])
        reserve(Nonterminal('struct-or-union-specifier'),
                [Nonterminal('struct-or-union'),Terminal(Tag.LP,'{'),
                 Nonterminal('struct-declaration-list'),Terminal(Tag.RP,'}')])
        reserve(Nonterminal('struct-or-union-specifier'),
                [Nonterminal('struct-or-union'),Terminal(Tag.ID,'ID')])
        reserve(Nonterminal('IDopt'),
                [Terminal(Tag.ID, 'ID')])
        reserve(Nonterminal('IDopt'),
                [Empty()])
        reserve(Nonterminal('struct-or-union'),
                [Terminal(Tag.STRUCT, 'STRUCT')])
        reserve(Nonterminal('struct-or-union'),
                [Terminal(Tag.UNION, 'UNION')])


        # # 所有的声明语句 int x; int y
        # struct-declaration-list -> struct-declaration
        # struct-declaration-list -> struct-declaration-list struct-delaration
        # 
        # struct-declaration -> struct-declarator-listopt ;
        # struct-declarator-listopt -> struct-declarator-list | e
        reserve(Nonterminal('struct-declaration-list'),
                [Nonterminal('struct-declaration')])
        reserve(Nonterminal('struct-declaration-list'),
                [Nonterminal('struct-declaration-list'), Nonterminal('struct-declaration')])
        reserve(Nonterminal('struct-declaration'),
                [Nonterminal('specifier-qualifier-list'),Nonterminal('struct-declarator-listopt'), Terminal(Tag.SEMI, ';')])
        reserve(Nonterminal('struct-declarator-listopt'),
                [Nonterminal('struct-declarator-list')])
        reserve(Nonterminal('struct-declarator-listopt'),
                [Empty()])
        reserve(Nonterminal('specifier-qualifier-list'),[Nonterminal('type-specifier'),Nonterminal('specifier-qualifier-listopt')])
        reserve(Nonterminal('specifier-qualifier-listopt'),[Nonterminal('specifier-qualifier-list')])
        reserve(Nonterminal('specifier-qualifier-listopt'),[Empty()])

        # # 一条声明语句的所有标识符 int x, y, z;
        # struct-declarator-list -> struct-declarator
        # struct-declarator-list -> struct-declarator-list , struct-declarator
        # 
        # struct-declarator -> declarator
        reserve(Nonterminal('struct-declarator-list'),
                [Nonterminal('struct-declarator')])
        reserve(Nonterminal('struct-declarator-list'),
                [Nonterminal('struct-declarator-list'),Terminal(Tag.COM, ','), Nonterminal('struct-declarator')])
        reserve(Nonterminal('struct-declarator'),
                [Nonterminal('declarator')])

        # 声明描述符
        # declarator -> pointeropt direct-declarator
        # pointeropt -> pointer | e
        reserve(Nonterminal('declarator'),
                [Nonterminal('pointeropt'),Nonterminal('direct-declarator')])
        reserve(Nonterminal('pointeropt'),
                [Nonterminal('pointer')])
        reserve(Nonterminal('pointeropt'),
                [Empty()])

        # direct-declarator -> ID
        # direct-declarator -> (declarator)
        # direct-declarator -> direct-declarator[assignment-expressionopt]
        # assignment-expressionopt -> assignment-expression | e
        # direct-declarator -> direct-declarator[*]
        # direct-declarator -> direct-declarator(parameter-type-list)
        # direct-declarator -> direct-declarator(identifier-listopt)
        # identifier-listopt -> identifier-list | e
        reserve(Nonterminal('direct-declarator'),
                [Terminal(Tag.ID,'ID')])
        reserve(Nonterminal('direct-declarator'),
                [Terminal(Tag.SLP, '('),Nonterminal('declarator'),Terminal(Tag.SRP,')')])
        reserve(Nonterminal('direct-declarator'),
                [Nonterminal('direct-declarator'),Terminal(Tag.LRP, '['), Nonterminal('assignment-expressionopt'), Terminal(Tag.RRP, ']')])
        reserve(Nonterminal('assignment-expressionopt'),
                [Nonterminal('assignment-expression')])
        reserve(Nonterminal('assignment-expressionopt'),
                [Empty()])
        reserve(Nonterminal('direct-declarator'),
                [Nonterminal('direct-declarator'), Terminal(Tag.LRP, '['), Terminal(Tag.MUILT,'*'),Terminal(Tag.RRP, ']')])
        reserve(Nonterminal('direct-declarator'),
                [Nonterminal('direct-declarator'),Terminal(Tag.SLP, '('), Nonterminal('parameter-type-list'), Terminal(Tag.SRP, ')')])
        reserve(Nonterminal('direct-declarator'),
                [Nonterminal('direct-declarator'), Terminal(Tag.SLP, '('), Nonterminal('identifier-listopt'),Terminal(Tag.SRP, ')')])
        reserve(Nonterminal('identifier-listopt'),
                [Nonterminal('identifier-list')])
        reserve(Nonterminal('identifier-listopt'),
                [Empty()])

        # pointer -> *
        # pointer -> *pointer
        # 
        # parameter-type-list -> parameter-list
        # parameter-type-list -> parameter-list, ...
        # 
        # parameter-list -> parameter-declaration
        # parameter-list -> parameter-list, parameter-declaration
        # 
        # parameter-declaration -> declaration-specifiers declarator
        # parameter-declaration -> declaration-specifiers abstract-declaratoropt
        # 
        # identifier-list -> ID
        # identifier-list ->identifier-list, ID
        reserve(Nonterminal('pointer'),
                [Terminal(Tag.MUILT,'*')])
        reserve(Nonterminal('pointer'),
                [Terminal(Tag.MUILT, '*'),Nonterminal('pointer')])
        reserve(Nonterminal('parameter-type-list'),
                [Nonterminal('parameter-list')])
        reserve(Nonterminal('parameter-type-list'),
                [Nonterminal('parameter-list'),Terminal(Tag.COM,','),Terminal(Tag.DOT,'.'),Terminal(Tag.DOT,'.'),Terminal(Tag.DOT,'.')])
        reserve(Nonterminal('parameter-list'),
                [Nonterminal('parameter-declaration')])
        reserve(Nonterminal('parameter-list'),
                [Nonterminal('parameter-list'),Terminal(Tag.COM,','),Nonterminal('parameter-declaration')])
        reserve(Nonterminal('parameter-declaration'),
                [Nonterminal('declaration-specifiers'), Nonterminal('declarator')])
        reserve(Nonterminal('parameter-declaration'),
                [Nonterminal('declaration-specifiers'), Nonterminal('abstract-declaratoropt')])
        reserve(Nonterminal('identifier-list'),
                [Terminal(Tag.ID, 'ID')])
        reserve(Nonterminal('identifier-list'),
                [Nonterminal('identifier-list'),Terminal(Tag.COM,','),Terminal(Tag.ID, 'ID')])

        # 类型名称
        # type-name -> abstract-declaratoropt
        # abstract-declarator -> pointer
        # abstract-declarator -> pointeropt direct-abstract-declarator
        # abstract-declaratoropt -> abstract-declarator | e
        # 
        # direct-abstract-declarator -> (abstract-declarator)
        # direct-abstract-declarator -> direct-abstract-declaratoropt[assignment-expression]
        # direct-abstract-declarator -> direct-abstract-declaratoropt[*]
        # direct-abstract-declarator -> direct-abstract-declaratoropt(parameter-type-listopt)
        # direct-abstract-declaratoropt -> direct-abstract-declarator | e
        # parameter-type-listopt -> parameter-type-list | e
        reserve(Nonterminal('type-name'),
                [Nonterminal('specifier-qualifier-list'),Nonterminal('abstract-declaratoropt')])
        reserve(Nonterminal('abstract-declarator'),
                [Nonterminal('pointer')])
        reserve(Nonterminal('abstract-declarator'),
                [Nonterminal('pointeropt'),Nonterminal('direct-abstract-declarator')])

        reserve(Nonterminal('abstract-declaratoropt'),
                [Nonterminal('abstract-declarator')])
        reserve(Nonterminal('abstract-declaratoropt'),
                [Empty()])
        reserve(Nonterminal('direct-abstract-declarator'),
                [Terminal(Tag.SLP,'('),Nonterminal('abstract-declarator'), Terminal(Tag.SRP,')')])
        reserve(Nonterminal('direct-abstract-declarator'),
                [Nonterminal('direct-abstract-declaratoropt'), Terminal(Tag.LRP, '['), Nonterminal('assignment-expression'), Terminal(Tag.RRP, ']')])
        reserve(Nonterminal('direct-abstract-declarator'),
                [Nonterminal('direct-abstract-declaratoropt'), Terminal(Tag.LRP, '['),Terminal(Tag.MUILT,'*'), Terminal(Tag.RRP, ']')])
        reserve(Nonterminal('direct-abstract-declarator'),
                [Nonterminal('direct-abstract-declaratoropt'), Terminal(Tag.SLP, '('), Nonterminal('parameter-type-listopt'), Terminal(Tag.SRP, ')')])
        reserve(Nonterminal('direct-abstract-declaratoropt'),
                [Nonterminal('direct-abstract-declarator')])
        reserve(Nonterminal('direct-abstract-declaratoropt'),
                [Empty()])
        reserve(Nonterminal('parameter-type-listopt'),
                [Nonterminal('parameter-type-list')])
        reserve(Nonterminal('parameter-type-listopt'),
                [Empty()])

        # 初始化
        # initializer -> assignment-expression
        # initializer -> {initializer-list}
        # initializer -> {initializer-list, }
        reserve(Nonterminal('initializer'),
                [Nonterminal('assignment-expression')])
        reserve(Nonterminal('initializer'),
                [Terminal(Tag.LP,'{'),Nonterminal('initializer-list'),Terminal(Tag.RP,'}')])
        reserve(Nonterminal('initializer'),
                [Terminal(Tag.LP, '{'), Nonterminal('initializer-list'), Terminal(Tag.COM,','), Terminal(Tag.RP, '}')])

        # initializer-list -> designationopt initializer
        # initializer-list -> initializer-list, designationopt initializer
        # designationopt -> designation | e
        # 
        # designation -> designator-list =
        # 
        # designator-list -> designator
        # designator-list -> designator-list designator
        # 
        # designator -> [constant-expression]
        # designator ->.ID
        reserve(Nonterminal('initializer-list'),
                [Nonterminal('designationopt'),Nonterminal('initializer')])
        reserve(Nonterminal('initializer-list'),
                [Nonterminal('initializer-list'),Terminal(Tag.COM,','), Nonterminal('designationopt'), Nonterminal('initializer')])
        reserve(Nonterminal('designationopt'),
                [Nonterminal('designation')])
        reserve(Nonterminal('designationopt'),
                [Empty()])
        reserve(Nonterminal('designation'),
                [Nonterminal('designation-list'),Terminal(Tag.ASSIGN,'=')])
        reserve(Nonterminal('designator-list'),
                [Nonterminal('designator')])
        reserve(Nonterminal('designator-list'),
                [Nonterminal('designator-list'),Nonterminal('designator')])
        reserve(Nonterminal('designator'),
                [Terminal(Tag.LRP,'['),Nonterminal('constant-expression'),Terminal(Tag.RRP,']')])
        reserve(Nonterminal('designator'),
                [Terminal(Tag.DOT, '.'), Terminal(Tag.ID, 'ID')])

        # 4.语句和块
        # statement -> labeled-statement | compound-statement | expression-statement
        #                   | selection-statement | iteration-statement | jump-statement
        reserve(Nonterminal('statement'), [Nonterminal('labeled-statement')])
        reserve(Nonterminal('statement'), [Nonterminal('compound-statement')])
        reserve(Nonterminal('statement'), [Nonterminal('expression-statement')])
        reserve(Nonterminal('statement'), [Nonterminal('selection-statement')])
        reserve(Nonterminal('statement'), [Nonterminal('iteration-statement')])
        reserve(Nonterminal('statement'), [Nonterminal('jump-statement')])

        # labeled statements
        # labeled-statement -> ID : statement
        # labeled-statement -> CASE constant-expression: statement
        # labeled-statement -> DEFAULT : statement
        reserve(Nonterminal('labeled-statement'),
                [Terminal(Tag.ID,'ID'),Terminal(Tag.COL,':'),Nonterminal('statement')])
        reserve(Nonterminal('labeled-statement'),
                [Terminal(Tag.CASE, 'CASE'), Nonterminal('constant-expression'), Terminal(Tag.COL, ':'), Nonterminal('statement')])
        reserve(Nonterminal('labeled-statement'),
                [Terminal(Tag.DEFAULT, 'DEFAULT'), Terminal(Tag.COL, ':'), Nonterminal('statement')])

        # compound statements
        # compound-statement -> {block-item-listopt}
        # block-item-listopt -> e | block-item-list
        # block-item-list -> block-item
        # block-item-list -> block-item-list block-item
        # block-item -> declaration
        # block-item -> statement
        reserve(Nonterminal('compound-statement'),
                [Terminal(Tag.LP,'{'),Nonterminal('block-item-listopt'),Terminal(Tag.RP,'}')])
        reserve(Nonterminal('block-item-listopt'),
                [Nonterminal('block-item-list')])
        reserve(Nonterminal('block-item-listopt'),
                [Empty()])
        reserve(Nonterminal('block-item-list'),
                [Nonterminal('block-item')])
        reserve(Nonterminal('block-item-list'),
                [Nonterminal('block-item-list'),Nonterminal('block-item')])
        reserve(Nonterminal('block-item'),
                [Nonterminal('declaration')])
        reserve(Nonterminal('block-item'),
                [Nonterminal('statement')])

        # expression and null statements
        # expression-statement -> expressionopt ;
        reserve(Nonterminal('expression-statement'),
                [Nonterminal('expressionopt'),Terminal(Tag.SEMI,';')])

        # selectiong statements
        # selection-statement -> IF(expression) statement
        # selection-statement -> IF(expression) statement else statement
        # selection-statement -> switch(expression) statement
        reserve(Nonterminal('selection-statement'),
                [Terminal(Tag.IF, 'IF'),Terminal(Tag.SLP, '('),Nonterminal('expression'), Terminal(Tag.SRP, ')'),Nonterminal('statement')])
        reserve(Nonterminal('selection-statement'),
                [Terminal(Tag.IF, 'IF'), Terminal(Tag.SLP, '('), Nonterminal('expression'), Terminal(Tag.SRP, ')'),
                 Nonterminal('statement'),Terminal(Tag.ELSE, 'ELSE'),Nonterminal('statement')])
        reserve(Nonterminal('selection-statement'),
                [Terminal(Tag.SWITCH, 'SWITCH'), Terminal(Tag.SLP, '('), Nonterminal('expression'), Terminal(Tag.SRP, ')'),
                 Nonterminal('statement')])

        # iteration statements
        # iteration-statement -> while ( expression ) statement
        # iteration-statement -> do statement while ( expression ) ;
        # iteration-statement -> for ( expressionopt; expressionopt; expressionopt ) statement
        # iteration-statement -> for ( declaration expressionopt; expressionopt ) statement
        reserve(Nonterminal('iteration-statement'),
                [Terminal(Tag.WHILE, 'WHILE'), Terminal(Tag.SLP, '('), Nonterminal('expression'),
                 Terminal(Tag.SRP, ')'),Nonterminal('statement')])
        reserve(Nonterminal('iteration-statement'),
                [Terminal(Tag.DO,'DO'),Nonterminal('statement'),Terminal(Tag.WHILE, 'WHILE'), Terminal(Tag.SLP, '('), Nonterminal('expression'),
                 Terminal(Tag.SRP, ')'), Terminal(Tag.SEMI,';')])
        reserve(Nonterminal('iteration-statement'),
                [Terminal(Tag.FOR, 'FOR'), Terminal(Tag.SLP, '('), Nonterminal('expressionopt'),Terminal(Tag.SEMI,';'),
                 Nonterminal('expressionopt'),Terminal(Tag.SEMI,';'),Nonterminal('expressionopt'),
                 Terminal(Tag.SRP, ')'), Nonterminal('statement')])
        reserve(Nonterminal('iteration-statement'),
                [Terminal(Tag.FOR, 'FOR'), Terminal(Tag.SLP, '('), Nonterminal('declaration'),
                 Nonterminal('expressionopt'), Terminal(Tag.SEMI, ';'), Nonterminal('expressionopt'),
                 Terminal(Tag.SRP, ')'), Nonterminal('statement')])

        # jump statements
        # jump-statement -> goto id;
        # jump-statement -> continue;
        # jump-statement -> break;
        # jump-statement -> return expressionopt;
        reserve(Nonterminal('jump-statement'),
                [Terminal(Tag.GOTO,'GOTO'),Terminal(Tag.ID,'ID'),Terminal(Tag.SEMI,';')])
        reserve(Nonterminal('jump-statement'),
                [Terminal(Tag.CONTINUE, 'CONTINUE'), Terminal(Tag.SEMI,';')])
        reserve(Nonterminal('jump-statement'),
                [Terminal(Tag.BREAK, 'BREAK'), Terminal(Tag.SEMI,';')])
        reserve(Nonterminal('jump-statement'),
                [Terminal(Tag.RETURN, 'RETURN'),Nonterminal('expressionopt'), Terminal(Tag.SEMI,';')])

        # 5.定义
        # function-definition -> declaration-specifiers declarator declaration-listopt compound-statement
        # declaration-list -> declaration
        # declaration-list -> declaration-list declaration
        reserve(Nonterminal('function-definition'),
                [Nonterminal('declaration-specifiers'),Nonterminal('declarator'),Nonterminal('declaration-listopt'),Nonterminal('compound-statement')])
        reserve(Nonterminal('declaration-list'),
                [Nonterminal('declaration')])
        reserve(Nonterminal('declaration-list'),
                [Nonterminal('declaration-list'),Nonterminal('declaration')])
        reserve(Nonterminal('declaration-listopt'),
                [Nonterminal('declaration-list')])
        reserve(Nonterminal('declaration-listopt'),
                [Empty()])

        # 6.常量
        # constant -> integer-constant | floating-constant | character-constant
        reserve(Nonterminal('constant'), [Nonterminal('integer-constant')])
        reserve(Nonterminal('constant'), [Nonterminal('floating-constant')])
        reserve(Nonterminal('constant'), [Nonterminal('character-constant')])
        # 整形常量
        # integer-constant -> DECIMAL | HEX | OCTAL
        reserve(Nonterminal('integer-constant'), [Terminal(Tag.DECIMAL,'DECIMAL')])
        reserve(Nonterminal('integer-constant'), [Terminal(Tag.HEX, 'HEX')])
        reserve(Nonterminal('integer-constant'), [Terminal(Tag.OCTAL, 'OCTAL')])
        # 浮点常量
        # floating-constant -> FCONST
        reserve(Nonterminal('floating-constant'), [Terminal(Tag.FCONST, 'FCONST')])
        # 字符常量
        # character-constant -> CCONST
        reserve(Nonterminal('character-constant'), [Terminal(Tag.CCONST, 'CCONST')])

        # 7.string-literal
        # string-literal -> STRING
        reserve(Nonterminal('string-literal'), [Terminal(Tag.STRING,'STRING')])


    """def grammer(self):
        '''
        初始化增广文法， 填充cfg列表
        :return:
        '''
        def reserve(header, body):
            self.R.append(Production(header, body))

        # 增广文法
        # G -> P
        reserve(Nonterminal('G'), [Nonterminal('P')])

        # 程序
        # P -> S S
        # S -> e
        reserve(Nonterminal('P'), [Nonterminal('S')])
        reserve(Nonterminal('S'), [Nonterminal('S'), Nonterminal('S')])

        # 语句
        # S ->  DS | IS | WS | DES | DOS | AS | FCS | FRS | FDS | FS
        #     |{ S } | ;
        temp = [[Nonterminal('DS')], [Nonterminal('IS')], [Nonterminal('WS')], [Nonterminal('DES')], [Nonterminal('DOS')],
                [Nonterminal('AS')], [Nonterminal('FCS')], [Nonterminal('FDS')], [Nonterminal('FRS')], [Nonterminal('FS')], [Terminal(Tag.SEMI, ';')],
                [Terminal(Tag.LP, '{'), Nonterminal('S'), Terminal(Tag.RP, '}')]]
        for stmt in temp:
            reserve(Nonterminal('S'), stmt)

        # 声明语句
        # DES -> T ID ; DES
        # DES -> e
        reserve(Nonterminal('DES'), [Nonterminal('T'), Terminal(Tag.ID, 'ID'),Terminal(Tag.SEMI, ';')])

        # 控制流语句
        # if-else语句
        # IS -> IF ( E ) S
        # IS -> IF ( E ) S ELSE S
        reserve(Nonterminal('IS'), [Terminal(Tag.IF,'IF'), Terminal(Tag.SLP, '('), Nonterminal('E'), Terminal(Tag.SRP, ')'), Nonterminal('S')])
        reserve(Nonterminal('IS'), [Terminal(Tag.IF,'IF'), Terminal(Tag.SLP, '('), Nonterminal('E'), Terminal(Tag.SRP, ')'),
                                    Nonterminal('S'), Terminal(Tag.ELSE, 'ELSE'), Nonterminal('S')])

        # while语句
        # WS -> WHILE ( E ) S
        reserve(Nonterminal('WS'), [Terminal(Tag.WHILE, 'WHILE'), Terminal(Tag.SLP, '('), Nonterminal('E'), Terminal(Tag.SRP, ')'), Nonterminal('S')])

        # do-while语句
        # DOS -> DO S WHILE ( E ) ;
        reserve(Nonterminal('DOS'), [Terminal(Tag.DO, 'DO'), Nonterminal('S'), Terminal(Tag.WHILE, 'WHILE'), Terminal(Tag.SLP, '('),
                                     Nonterminal('E'), Terminal(Tag.SRP, ')'),Terminal(Tag.SEMI, ';')])

        # 赋值语句
        # AS -> ID = E ;
        #    | L = E ;
        # L -> ID [ E ]
        #    | L1 [ E ]
        reserve(Nonterminal('AS'), [Terminal(Tag.ID, 'ID'), Terminal(Tag.ASSIGN, '='), Nonterminal('E'),Terminal(Tag.SEMI, ';')])
        reserve(Nonterminal('AS'), [Nonterminal('L'), Terminal(Tag.ASSIGN, '='), Nonterminal('E'), Terminal(Tag.SEMI, ';')])
        reserve(Nonterminal('L'), [Terminal(Tag.ID, 'ID'), Terminal(Tag.LRP, '['), Nonterminal('E'), Terminal(Tag.RRP, ']')])
        reserve(Nonterminal('L'), [Nonterminal('L'), Terminal(Tag.LRP, '['), Nonterminal('E'), Terminal(Tag.RRP, ']')])

        # 函数调用语句
        # FCS -> ID ( A );
        # A -> e | E , A
        reserve(Nonterminal('FCS'), [Terminal(Tag.ID, 'ID'), Terminal(Tag.SLP, '('), Nonterminal('A'), Terminal(Tag.SRP, ')')])
        reserve(Nonterminal('A'), [Empty()])
        reserve(Nonterminal('A'), [Nonterminal('E'), Terminal(Tag.COM, ','), Nonterminal('A')])
        # 函数返回语句
        # FRS -> RETURN E ;
        reserve(Nonterminal('FRS'), [Terminal(Tag.RETURN, 'RETURN'), Nonterminal('E'),Terminal(Tag.SEMI, ';')])
        # 函数声明语句
        # FDS -> T ID ( FA );
        # FA -> e | T ID , FA | T, FA
        reserve(Nonterminal('FDS'), [Nonterminal('T'), Terminal(Tag.ID, 'ID'), Terminal(Tag.SLP, '('), Nonterminal('FAD'),
                                     Terminal(Tag.SRP, ')'), Terminal(Tag.SEMI, ';')])
        # reserve(Nonterminal('FA'), [Empty()])
        # reserve(Nonterminal('FA'), [Nonterminal('T'), Terminal(Tag.ID, 'ID'), Terminal(Tag.COM, ','), Nonterminal('FA')])
        # reserve(Nonterminal('FA'), [Nonterminal('T'), Terminal(Tag.COM, ','), Nonterminal('FA')])

        # 函数定义语句
        # FS -> T ID ( FAD ) { S }
        # FAD -> e | T ID, FAD
        reserve(Nonterminal('FS'), [Nonterminal('T'), Terminal(Tag.ID, 'ID'), Terminal(Tag.SLP, '('), Nonterminal('FAD')
            , Terminal(Tag.SRP, ')'), Terminal(Tag.LP, '{'),   Nonterminal('S'), Terminal(Tag.RP, '}')])
        reserve(Nonterminal('FAD'), [Empty()])
        reserve(Nonterminal('FAD'), [Nonterminal('T'), Terminal(Tag.ID, 'ID'), Terminal(Tag.COM, ','), Nonterminal('FAD')])
        # 表达式
        # E -> EB | EO
        # reserve(Nonterminal('E'), [Nonterminal('EB')])
        # reserve(Nonterminal('E'), [Nonterminal('EO')])
        # 算术表达式
        # EO -> EO + TO | EO-TO | TO
        # TO -> TO * FO | TO / FO | FO
        # FO -> ( EO ) | ID | FCONST | CONST | CCONST
        reserve(Nonterminal('E'), [Nonterminal('E'), Terminal(Tag.ADD, '+'), Nonterminal('TO')])
        reserve(Nonterminal('E'), [Nonterminal('E'), Terminal(Tag.SUB, '-'), Nonterminal('TO')])
        reserve(Nonterminal('E'), [Nonterminal('TO')])
        reserve(Nonterminal('TO'), [Nonterminal('TO'), Terminal(Tag.MUILT, '*'), Nonterminal('FO')])
        reserve(Nonterminal('TO'), [Nonterminal('TO'), Terminal(Tag.DIV, '/'), Nonterminal('FO')])
        reserve(Nonterminal('TO'), [Nonterminal('FO')])
        reserve(Nonterminal('FO'), [Terminal(Tag.SLP, '('), Nonterminal('E'), Terminal(Tag.SRP, ')')])
        reserve(Nonterminal('FO'), [Terminal(Tag.ID, 'ID')])
        for const in [[Terminal(Tag.FCONST, 'FCONST')], [Terminal(Tag.HEX, 'HEX')], [Terminal(Tag.OCTAL, 'OCTAL')],
                      [Terminal(Tag.DECIMAL, 'DECIMAL')], [Terminal(Tag.CCONST, 'CCONST')]]:
            reserve(Nonterminal('FO'), const)

        # 逻辑表达式
        # EB -> EB1 OR EB2
        # EB -> EB1 AND EB2
        # EB -> NOT EB1
        # EB -> E1 REL E2
        for e in [[Nonterminal('E'), Terminal(Tag.OR, '||'), Nonterminal('E')],
                  [Nonterminal('E'), Terminal(Tag.AND, '&&'), Nonterminal('E')],
                  [Terminal(Tag.NOT, '!'), Nonterminal('E')], [Nonterminal('E'), Terminal(Tag.REL, 'REL'), Nonterminal('E')]]:
            reserve(Nonterminal('E'), e)

        # 附加文法
        # 类型
        # T -> B C
        # B -> DOUBLE | FLOAT | INT | LONG
        #    | REGISTER | SHORT
        # 结构体
        # B -> R
        # R -> STRUCT ID
        # 指针
        # p -> e
        # p -> * P1
        # 数组
        # C -> e
        # C -> [ num ] C1
        reserve(Nonterminal('T'), [Nonterminal('B'), Nonterminal('C')])
        for type in [[Terminal(Tag.DOUBLE, 'DOUBLE')], [Terminal(Tag.FLOAT, 'FLOAT')], [Terminal(Tag.INT, 'INT')],
                     [Terminal(Tag.LONG, 'LONG')], [Terminal(Tag.REGISTER, 'REGISTER')], [Terminal(Tag.SHORT, 'SHORT')],
            [Nonterminal('R')]]:
            reserve(Nonterminal('B'), type)
        reserve(Nonterminal('R'), [Terminal(Tag.STRUCT, 'STRUCT'), Terminal(Tag.ID, 'ID')])
        reserve(Nonterminal('PT'), [Empty()])
        reserve(Nonterminal('PT'), [Terminal(Tag.MUILT, 'MUILT'), Nonterminal('PT')])
        reserve(Nonterminal('C'), [Empty()])
        reserve(Nonterminal('C'), [Terminal(Tag.LRP, '['), Nonterminal('num'), Terminal(Tag.RRP, ']'), Nonterminal('C')])

        # 整数常量
        # num -> num + CT | num-CT | CT
        # CT -> CT * CF | CT / CF | CF
        # CF -> ( num ) | CCONST | DECIMAL | HEX | OCTAL
        reserve(Nonterminal('num'), [Nonterminal('num'), Terminal(Tag.ADD, '+'), Nonterminal('CT')])
        reserve(Nonterminal('num'), [Nonterminal('num'), Terminal(Tag.SUB, '-'), Nonterminal('CT')])
        reserve(Nonterminal('num'), [Nonterminal('CT')])
        reserve(Nonterminal('CT'), [Nonterminal('CT'), Terminal(Tag.MUILT, '*'), Nonterminal('CF')])
        reserve(Nonterminal('CT'), [Nonterminal('CT'), Terminal(Tag.DIV, '/'), Nonterminal('CF')])
        reserve(Nonterminal('CT'), [Nonterminal('CF')])
        reserve(Nonterminal('CF'), [Terminal(Tag.SLP, '('), Nonterminal('num'), Terminal(Tag.SRP, ')')])
        for const in [[Terminal(Tag.FCONST, 'FCONST')], [Terminal(Tag.HEX, 'HEX')], [Terminal(Tag.OCTAL, 'OCTAL')],
                      [Terminal(Tag.DECIMAL, 'DECIMAL')], [Terminal(Tag.CCONST, 'CCONST')]]:
            reserve(Nonterminal('CF'), const)"""

    def start_symbol(self):
        '''
        获得文法开始符号
        :return:
        '''
        return self.S

    def get_rules(self, nontermial):
        '''
        获得产生式头部为特定非终结符的所有产生式
        :param nontermial: 非终结符
        :return: 产生式的集合
        '''
        if not isinstance(nontermial, Nonterminal) :

            print("参数错误，需要传入一个Nonterminal类型的变量")
            raise TypeError
        result = []
        for rule in self.R:
            if rule.header == nontermial:
                result.append(rule)
        return result

    def __str__(self):
        productions = ''
        for rule in self.R:
            productions += str(rule)
        return productions


class Terminal:
    '''
    终结符
    '''

    def __init__(self, character, show_str):
        # 终结符名称
        self.character = character
        self.show_str = show_str

    @staticmethod
    def init_token(token):
        if not isinstance(token, Token):
            raise TypeError
        character = token.code
        if character in Tag.show_value:
            show_str = token.attr
        else:
            show_str = Tag.show_strs[str(character)]
        return Terminal(character, show_str)

    def __str__(self):
        return self.show_str

    def __hash__(self):
        return self.character

    def __eq__(self, other):
        if not isinstance(other, Terminal):
            return False
        return self.character == other.character


class Nonterminal:
    '''
    非终结符
    '''

    def __init__(self, character):
        # 非终结符名称
        self.character = character

    def __str__(self):
        return self.character

    def __eq__(self, other):
        if not isinstance(other, Nonterminal):
            return False
        return self.character == other.character

    def __hash__(self):
        return hash(self.character)

class Empty:
    def __init__(self):
        self.character = chr(949)

    def __eq__(self, other):
        if not isinstance(other, Empty):
            return False
        return self.character == other.character

    def __hash__(self):
        return 949

    def __str__(self):
        return self.character


class Production:
    '''
    产生式
    header -> body
    '''
    def __init__(self, header, body):
        self.header = header
        self.body = body

    def get_num_body_smybol(self):
        if len(self.body) == 1 and isinstance(self.body[0], Empty):
            return 0
        return len(self.body)

    def get_header(self):
        return self.header
    def __str__(self):
        '''
        表示一个产生式的字符串
        :return: header -> body
        '''
        pstr = ''
        pstr += str(self.header) + " -> "
        for c in self.body:
            pstr += str(c) + " "
        pstr += '\n'
        return pstr

    def __eq__(self, other):
        if isinstance(other, Production):

            return self.header == other.header and self.body == other.body
        return False
    def __hash__(self):
        hash_value = hash(self.header)
        for c in self.body:
            hash_value += hash(c)
        return hash_value










