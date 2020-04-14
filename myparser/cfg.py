from lexer.Tag import Tag

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
        self.S = Nonterminal('G')
        self.grammer()

    def grammer(self):
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
        reserve(Nonterminal('P'), [Nonterminal('S'), Nonterminal('S')])
        reserve(Nonterminal('S'), [])

        # 语句
        # S ->  DS | IS | WS | DES | DOS | AS | FCS | FRS | FDS | FS
        #     |{ S } | ;
        temp = [[Nonterminal('DS')], [Nonterminal('IS')], [Nonterminal('WS')], [Nonterminal('DES')], [Nonterminal('DOS')],
                [Nonterminal('AS')], [Nonterminal('FCS')], [Nonterminal('FDS')], [Nonterminal('FS')], [Terminal(Tag.SEMI, ';')],
                [Terminal(Tag.LP, '{'), Nonterminal('S'), Terminal(Tag.RP, '}')]]
        for stmt in temp:
            reserve(Nonterminal('S'), stmt)

        # 声明语句
        # DES -> T ID ; DES
        # DES -> e
        reserve(Nonterminal('DES'), [Nonterminal('T'), Terminal(Tag.ID, 'ID'),Terminal(Tag.SEMI, ';'), Nonterminal('DES')])
        reserve(Nonterminal('DES'), [])

        # 控制流语句
        # if-else语句
        # IS -> IF ( E ) S
        # IS -> IF ( E ) S ELSE S
        reserve(Nonterminal('IS'), [Nonterminal('IF'), Terminal(Tag.SLP, '('), Nonterminal('E'), Terminal(Tag.SRP, ')'), Nonterminal('S')])
        reserve(Nonterminal('IS'), [Nonterminal('IF'), Terminal(Tag.SLP, '('), Nonterminal('E'), Terminal(Tag.SRP, ')'),
                                    Nonterminal('S'), Terminal(Tag.ELSE, 'ELSE'), Nonterminal('S')])

        # while语句
        # WS -> WHILE ( E ) S
        reserve(Nonterminal('WS'), [Terminal(Tag.WHILE, 'WHILE'), Terminal(Tag.SLP, '('), Nonterminal('E'), Terminal(Tag.SRP, ')'), Nonterminal('S')])

        # do-while语句
        # DOS -> DO S WHILE ( E ) ;
        reserve(Nonterminal('DOS'), [Terminal(Tag.DO, 'DO'), Nonterminal('S'), Terminal(Tag.WHILE, 'WHILE'), Terminal(Tag.SLP, '('),
                                     Nonterminal('E'), Terminal(Tag.SRP, ')')])

        # 赋值语句
        # AS -> ID = E ;
        #    | L = E ;
        # L -> ID [ E ]
        #    | L1 [ E ]
        reserve(Nonterminal('AS'), [Terminal(Tag.ID, 'ID'), Terminal(Tag.ASSIGN, '='), Nonterminal('E')])
        reserve(Nonterminal('AS'), [Nonterminal('L'), Terminal(Tag.ASSIGN, '='), Nonterminal('E')])
        reserve(Nonterminal('L'), [Terminal(Tag.ID, 'ID'), Terminal(Tag.LRP, '['), Nonterminal('E'), Terminal(Tag.RRP, ']')])
        reserve(Nonterminal('L'), [Nonterminal('L'), Terminal(Tag.LRP, '['), Nonterminal('E'), Terminal(Tag.RRP, ']')])

        # 函数调用语句
        # FCS -> ID ( A );
        # A -> e | E , A
        reserve(Nonterminal('FCS'), [Terminal(Tag.ID, 'ID'), Terminal(Tag.SLP, '('), Nonterminal('A'), Terminal(Tag.SLP, ')')])
        reserve(Nonterminal('A'), [])
        reserve(Nonterminal('A'), [Nonterminal('E'), Terminal(Tag.COM, ','), Nonterminal('A')])
        # 函数返回语句
        # FRS -> RETURN E ;
        reserve(Nonterminal('FRS'), [Terminal(Tag.RETURN, 'RETURN'), Nonterminal('E')])
        # 函数声明语句
        # FDS -> T ID ( FA );
        # FA -> e | T ID , FA | T, FA
        reserve(Nonterminal('FDS'), [Nonterminal('T'), Terminal(Tag.ID, 'ID'), Terminal(Tag.SLP, '('), Nonterminal('FA'),
                                     Terminal(Tag.SRP, ')'), Terminal(Tag.SEMI, ';')])
        reserve(Nonterminal('FA'), [])
        reserve(Nonterminal('FA'), [Nonterminal('T'), Terminal(Tag.ID, 'ID'), Terminal(Tag.COM, ','), Nonterminal('FA')])
        reserve(Nonterminal('FA'), [Nonterminal('T'), Terminal(Tag.COM, ','), Nonterminal('FA')])

        # 函数定义语句
        # FS -> T ID ( FAD ) { S }
        # FAD -> e | T ID, FAD
        reserve(Nonterminal('FS'), [Nonterminal('T'), Terminal(Tag.ID, 'ID'), Terminal(Tag.SLP, '('), Nonterminal('FAD')
            , Terminal(Tag.SLP, ')'), Terminal(Tag.LP, '{'),   Nonterminal('S'), Terminal(Tag.RP, '}')])
        reserve(Nonterminal('FAD'), [])
        reserve(Nonterminal('FAD'), [Nonterminal('T'), Terminal(Tag.ID, 'ID'), Terminal(Tag.COM, ','), Nonterminal('FAD')])
        # 表达式
        # E -> EB | EO
        reserve(Nonterminal('E'), [Nonterminal('EB')])
        reserve(Nonterminal('E'), [Nonterminal('EO')])
        # 算术表达式
        # EO -> EO + TO | EO - TO | TO
        # TO -> TO * FO | TO / FO | FO
        # FO -> ( EO ) | ID | FCONST | CONST | CCONST
        reserve(Nonterminal('EO'), [Nonterminal('EO'), Terminal(Tag.ADD, '+'), Nonterminal('TO')])
        reserve(Nonterminal('EO'), [Nonterminal('EO'), Terminal(Tag.SUB, '-'), Nonterminal('TO')])
        reserve(Nonterminal('EO'), [Nonterminal('TO')])
        reserve(Nonterminal('TO'), [Nonterminal('TO'), Terminal(Tag.MUILT, '*'), Nonterminal('FO')])
        reserve(Nonterminal('TO'), [Nonterminal('TO'), Terminal(Tag.DIV, '/'), Nonterminal('FO')])
        reserve(Nonterminal('FO'), [Terminal(Tag.SLP, '('), Nonterminal('EO'), Terminal(Tag.SRP, ')')])
        reserve(Nonterminal('FO'), [Terminal(Tag.ID, 'ID')])
        for const in [[Terminal(Tag.FCONST, 'FCONST')], ['CONST'], [Terminal(Tag.CCONST, 'CCONST')]]:
            reserve(Nonterminal('FO'), const)

        # 逻辑表达式
        # EB -> EB1 OR EB2
        # EB -> EB1 AND EB2
        # EB -> NOT EB1
        # EB -> E1 REL E2
        for e in [[Nonterminal('EB'), Terminal(Tag.OR, '||'), Nonterminal('EB')],
                  [Nonterminal('EB'), Terminal(Tag.AND, '&&'), Nonterminal('EB')],
                  [Terminal(Tag.NOT, '!'), Nonterminal('EB')], [Nonterminal('E'), Terminal(Tag.REL, 'REL'), Nonterminal('E')]]:
            reserve(Nonterminal('EB'), e)

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
        reserve(Nonterminal('PT'), [])
        reserve(Nonterminal('PT'), [Terminal(Tag.MUILT, 'MUILT'), Nonterminal('PT')])
        reserve(Nonterminal('C'), [])
        reserve(Nonterminal('C'), [Terminal(Tag.LRP, '['), Nonterminal('num'), Terminal(Tag.RRP, ']'), Nonterminal('C')])

        # 整数常量
        # num -> num + CT | num - CT | CT
        # CT -> CT * CF | CT / CF | CF
        # CF -> ( num ) | CCONST | DECIMAL | HEX | OCTAL
        reserve(Nonterminal('num'), [Nonterminal('num'), Terminal(Tag.ADD, '+'), Nonterminal('CT')])
        reserve(Nonterminal('num'), [Nonterminal('num'), Terminal(Tag.SUB, '-'), Nonterminal('CT')])
        reserve(Nonterminal('num'), [Nonterminal('CT')])
        reserve(Nonterminal('CT'), [Nonterminal('CT'), Terminal(Tag.MUILT, '*'), Nonterminal('CF')])
        reserve(Nonterminal('CT'), [Nonterminal('CT'), Terminal(Tag.DIV, '/'), Nonterminal('CF')])
        reserve(Nonterminal('CF'), [Terminal(Tag.SLP, '('), Nonterminal('num'), Terminal(Tag.SRP, ')')])
        for const in [[Terminal(Tag.FCONST, 'FCONST')], [Terminal(Tag.HEX, 'HEX')], [Terminal(Tag.OCTAL, 'OCTAL')],
                      [Terminal(Tag.DECIMAL, 'DECIMAL')], [Terminal(Tag.CCONST, 'CCONST')]]:
            reserve(Nonterminal('CF'), const)

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

    def __str__(self):
        return self.show_str

    def __eq__(self, other):
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
        return self.character == other.character


class Production:
    '''
    产生式
    header -> body
    '''
    def __init__(self, header, body):
        self.header = header
        self.body = body

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











