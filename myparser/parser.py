from lexer.lexer import Lexer
from myparser.cfg import Cfg, Nonterminal, Terminal, Empty
from myparser.item import Item
from lexer.Tag import Tag

class Parser:

    def __init__(self, lexer):
        # 语法分析器
        self.lexer = lexer
        # 产生式的集合
        self.cfg = Cfg()
        # 项集族
        self.item_family = []
        # ACTION函数
        # 该结构为一个字典，actions[i] = [(a, 0, j), .(b, 1, k)..]
        # 其中i是状态，a, b是终结符，j是移入之后的转态, 0表示移入，1表示规约，k表示所用的产生式标号
        self.actions = {}
        # GOTO函数
        # 其结构是一个字典 goto[i] = [(a, j), ()]
        self.gotos = {}

    def closure(self, i) -> []:
        '''
        求项集i的闭包
        :param i:项集 列表
        :return: 项集i的闭包的一个列表 []
        '''
        symbols = []  # 记录所有非终结符
        firsts = []  # 记录所有非终结符的first集

        def containNull(list):
            for i in list:
                if isinstance(i, Empty):
                    return True
            return False

        def addFirst(source,target):
            for i in source:
                if i not in target and not isinstance(i , Empty):
                    target.append(i)
            return target

        def reduction(symbol):
            '''
            递归求非终结符的first集
            :param symbol 非终结符号
            :return symbol 的 first集[]
            '''
            # 判断是否查询过
            if len(symbols) > 0 and symbol in symbols:
                # print('当前符号：'+symbol.__str__()+' first: ')
                # for i in firsts[symbols.index(symbol)]:
                #     print(i.__str__())
                return firsts[symbols.index(symbol)]

            results = []
            record = []  # 记录 产生式右部含有产生式左部的非终结符 的产生式集合
            for production in self.cfg.get_rules(symbol):  # 终结符和空产生式先加入
                if len(production.body) != 1:
                    continue
                    # 若为终结符，终结符加入
                temp = production.body[0]
                if isinstance(temp, Terminal):
                    if temp not in results:
                        results.append(temp)
                        # break
                # 若为非终结符，则跳过
                elif isinstance(temp, Nonterminal):
                    continue
                # 若为空产生式，则加入
                elif isinstance(temp,Empty):
                    if not containNull(results):
                        results.append(Empty())

            for production in self.cfg.get_rules(symbol):
                curBody = production.body
                if len(curBody) == 1 and not isinstance(curBody[0],Nonterminal) :
                    continue
                if symbol in curBody:  # 若产生式左部出现在产生式右部，延后处理
                    record.append(production)
                    continue
                for temp in curBody:  # 取出产生式右部，遍历：
                    # 若为非终结符,判断空产生式
                    if isinstance(temp, Nonterminal):
                        listOfTer = reduction(temp)
                        if containNull(listOfTer):  # 含有空产生式，跳过找下一个的first集, 若为最后一个则加入空
                            results = addFirst(listOfTer, results)
                            if temp is not production.body[-1]:
                                continue
                            if not containNull(results): # 全空
                                results.append(Empty())
                                break
                        else:  # 不含有空产生式，当前符号first加入到symbolfirst集中
                            results = addFirst(listOfTer, results)
                            break
                    # 若为终结符，终结符加入
                    elif isinstance(temp, Terminal):
                        if temp not in results:
                            results.append(temp)
                            break

            if len(record) != 0:
                for production in record:
                    for temp in production.body:  # 取出产生式右部，遍历：
                        # 若为非终结符,判断空产生式
                        if isinstance(temp, Nonterminal):
                            if symbol == temp:
                                listOfTer = results
                            else:
                                listOfTer = reduction(temp)
                            if containNull(listOfTer):  # 含有空产生式，跳过找下一个的first集, 若为最后一个则加入空
                                results = addFirst(listOfTer, results)
                                if temp is not production.body[-1]:
                                    continue
                                if not containNull(results):
                                    results.append(Empty())
                                    break
                            else:
                                results = addFirst(listOfTer,results)
                                break
                        # 若为终结符，终结符加入
                        elif isinstance(temp, Terminal) and temp not in results:
                            results.append(temp)
                            break

            symbols.append(symbol)
            firsts.append(results)

            return results

        def first(a):
            '''
            获得从文法符号串a推到得到的串的首符号的集合(a 表示alpha)
            :param a:文法符号串[]  nonter ter
            :return: 终结符符号集合
            '''
            beta = a[0]
            alpha = a[1]
            result = []
            if beta is None:
                return alpha
            list = []
            list.extend(beta)
            list.extend(alpha)
            for symbol in list:
                # 查询
                currentFirst = []  # 当前符号first集
                if isinstance(symbol, Terminal):  # 终结符
                    if symbol not in result:
                        result.append(symbol)
                    return result

                currentFirst.extend(reduction(symbol))  # 非终结符
                if containNull(currentFirst):
                    # print('当前符号：' + symbol.__str__() + ' first: ')
                    # for i in currentFirst:
                    #     print(i.__str__())
                    result = addFirst(currentFirst,result)
                    continue
                else:
                    result = addFirst(currentFirst,result)
                    return result
            return alpha

        Items = []
        Items.extend(i)
        productions = []
        lenth = 0
        while 1:
            if lenth == len(Items):  # 项目集不再变化
                break
            lenth = len(Items)
            for item in Items:
                # 判断下一个字符是否为终结符或者当前状态为规约状态
                if item.next_symbol() is not None and isinstance(item.next_symbol(), Nonterminal):
                    nonTerminalSymbol = item.next_symbol()
                    symbolString = []
                    symbolString.extend(item.beta_a())
                    lookahead = first(symbolString)  # 展望符列表
                    for production in self.cfg.get_rules(nonTerminalSymbol):  # 遍历增广文法产生式
                        if production not in productions:
                            productions.append(production)
                            Items.append(Item(production, lookahead))
        return Items

    def goto(self, i, x) -> []:
        '''
        移入x时项集i的转换 [A -> a.Xp, a]
        :param i:项集
        :param x: 文法符号
        :return: 转换后的项集
        '''
        items = []
        for a in i:
            if a.next_symbol() is None:
                continue
            if a.next_symbol() == x:
                items.append(a.next_item())
        return self.closure(items)

    def table(self, G) -> [[]]:
        '''
        求G上的项集族, 同时求的actions表和gotos表
        :param G: 增广文法
        :return:
        '''
        # 初始化项集族为[G->.p, $]
        start_production = G.get_rules(G.start_symbol())[0]
        start_items = Item(start_production, [Terminal(Tag.END, '$')])
        self.item_family = []
        temp_family = [self.closure([start_items, ]),]
        self.item_family.extend(temp_family)
        # while len(temp_family) != 0:
        #     temp_family_temp = []
        #     for I in temp_family:
        #         # 获得该项集中所有的下一个symbol
        #         all_symbols = []
        #         for i in I:
        #             one_symbol = i.next_symbol()
        #             if one_symbol is not None:
        #                 all_symbols.append(one_symbol)
        #         for s in all_symbols:
        #             new_I = self.goto(I, s)
        #             if new_I is not None and new_I not in self.item_family and new_I not in temp_family_temp:
        #                 temp_family_temp.append(new_I)
        #     temp_family = temp_family_temp[:]
        #     self.item_family.extend(temp_family)

        for I in self.item_family:
            index_I = self.item_family.index(I)

            # 获得该项集中所有的下一个symbol
            all_symbols = []
            for i in I:
                one_symbol = i.next_symbol()
                # 如果存在某一项没有next symbol,那么以及进行规约，加入到action中
                if one_symbol is None:
                    if index_I in self.actions.keys():
                        self.actions[index_I] = self.actions[index_I].union({(look_symbol, 1, i.get_production()) for look_symbol in i.symbols})
                    else:
                        self.actions[index_I] = {(look_symbol, 1, i.get_production()) for look_symbol in i.symbols}
                if one_symbol is not None:
                    all_symbols.append(one_symbol)
            for s in all_symbols:
                new_I = self.goto(I, s)
                if new_I is not None and new_I not in self.item_family:
                    self.item_family.append(new_I)
                index_new_I = self.item_family.index(new_I)
                # 如果此时s是终结符，那么加入到actions中，并设为移入
                if isinstance(s, Terminal):
                    if index_I in self.actions.keys():
                        self.actions[index_I].add((s, 0, index_new_I))
                    else:
                        self.actions[index_I] = {(s, 0, index_new_I),}
                else:  # 如果为非终结符，那么加入到gotos中
                    if  index_I in self.gotos.keys():
                        self.gotos[index_I].add((s, index_new_I))
                    else:
                        self.gotos[index_I] = {(s, index_new_I),}

    def program(self):
        '''
        进行语法分析
        :return:
        '''

        def move():
            nonlocal look
            token = self.lexer.getnexttoken()
            look = Terminal.init_token(token[1])



        self.table(self.cfg)

        # 初始化时将0状态放入状态栈中
        state_stack = [0,]

        # look为将下一个token变成的终结符
        look = None
        move()
        while look.character != Tag.FINISH:
            state_actions =  self.actions[state_stack[-1]]
            error_flag1 = True
            print(state_stack)
            print(look)
            for action in state_actions:
                # print(action[0].character)
                if action[0] == look:
                    error_flag1 = False
                    # 移入操作
                    if action[1] == 0:
                        print('s')
                        state_stack.append(action[2])
                        move()
                        break
                    # 规约操作
                    else:
                        print('r')
                        production = action[2]
                        num_of_s = production.get_num_body_smybol()
                        print(production)
                        for i in range(num_of_s):
                            state_stack.pop()
                        goto_action = self.gotos[state_stack[-1]]
                        error_flag = True
                        for action in goto_action:
                            if action[0] == production.header:
                                error_flag = False
                                state_stack.append(action[1])
                        if error_flag:
                            print("error...")
                            return
                        # 表明在该状态下该字符对应的动作为空
            if error_flag1:
                print("error")
                return


