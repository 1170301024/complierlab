from myparser.cfg import Cfg, Nonterminal, Terminal
from myparser.item import Item
from lexer.Tag import Tag

class Parser:

    def __init__(self):
        # 产生式的集合
        self.cfg = Cfg()
        # 项集族
        self.item_family = []
        # ACTION函数
        self.actions = []
        # GOTO函数
        self.gotos = []

    def closure(self, i) -> []:
        '''
        求项集i的闭包
        :param i:项集 列表
        :return: 项集i的闭包的一个列表 []
        '''
        firstDict = {}# 记录所有非终结符的first集

        def containNull(list):
            for i in list:
                if not isinstance(i,Terminal) and i == []:
                    return True
            return False

        def reduction(symbol):
            '''
            递归求非终结符的first集
            :param symbol 非终结符号
            :return symbol 的 first集[]
            '''
            results = []
            record = [] #记录 产生式右部含有产生式左部的非终结符 的产生式集合
            for production in self.cfg.get_rules(symbol): # 终结符和空产生式先加入
                if len(production.body) != 1:
                    continue
                    # 若为终结符，终结符加入
                temp = production.body[0]
                if isinstance(temp, Terminal):
                    if temp not in results:
                        results.append(temp)
                        break
                # 若为非终结符，则跳过
                elif isinstance(temp, Nonterminal):
                    continue
                # 若为空产生式，则加入
                elif [] not in results and temp == []:
                    results.append([])
                    break

            for production in self.cfg.get_rules(symbol):
                curBody = production.body
                if symbol in curBody: # 若产生式左部出现在产生式右部，延后处理
                    record.append(production)
                    continue
                for temp in curBody :# 取出产生式右部，遍历：
                    # 若为非终结符,判断空产生式
                    if isinstance(temp,Nonterminal):

                        print('\n规约参数：'+symbol.__str__()+'\n当前产生式：' + production.__str__() + ' 当前符号：'+temp.__str__())
                        print(' 当前first集：')
                        for result in results :
                            print(result.show_str+'  ')

                        listOfTer = reduction(temp)
                        if containNull(listOfTer) : # 含有空产生式，跳过找下一个的first集, 若为最后一个则加入空
                            if temp is not production.body[-1]:
                                continue
                            if not containNull(results):
                                results.append([])
                                break
                        else: #不含有空产生式，当前符号first加入到symbolfirst集中
                            for i in listOfTer:
                                if i not in results:
                                    results.append(i)
                                    break
                    # 若为终结符，终结符加入
                    elif isinstance(temp,Terminal) :
                         if temp not in results:
                            results.append(temp)
                            break
                    # 若为空产生式，则加入
                    elif [] not in results and temp == []:
                        results.append([])
                        break

            if len(record) != 0:
                for production in record:
                    for temp in production.body:  # 取出产生式右部，遍历：
                        # 若为非终结符,判断空产生式
                        if isinstance(temp, Nonterminal):
                            print('\n规约参数：' + symbol.__str__() + '\n当前产生式：' + production.__str__() + ' 当前符号：' + temp.__str__())
                            print(' 当前first集：')
                            for result in results:
                                print(result.show_str + '  ')
                            listOfTer = []
                            if symbol == temp:
                                listOfTer = results
                            else:
                                listOfTer = reduction(temp)
                            if containNull(listOfTer):  # 含有空产生式，跳过找下一个的first集, 若为最后一个则加入空
                                if temp is not production.body[-1]:
                                    continue
                                if not containNull(results):
                                    results.append([])
                                    break
                            else:
                                for i in listOfTer:
                                    if i not in results:
                                        results.append(i)
                                        break
                        # 若为终结符，终结符加入
                        elif isinstance(temp, Terminal) and temp not in results:
                            results.append(temp)
                            break
            return results

        def first(a):
            '''
            获得从文法符号串a推到得到的串的首符号的集合(a 表示alpha)
            :param a:文法符号串[]  nonter ter
            :return: 终结符符号集合
            '''
            result = []
            for symbol in a:
                # 查询
                currentFirst = []  # 当前符号first集
                if isinstance(symbol,Terminal): # 终结符
                    if symbol not in result:
                        result.append(symbol)
                    continue

                # if len(firstDict) > 0 and symbol in firstDict.keys(): # 是否已经查询过
                #     for temp in firstDict.get(symbol):
                #         if temp not in result:
                #             result.append(temp)

                currentFirst.extend(reduction(symbol)) # 非终结符
                for i in currentFirst:
                    if i not in result:
                        result.append(i)

                # firstDict[symbol]=currentFirst

            return result



        Items = []
        Items.extend(i)
        productions = []
        lenth = 0
        while 1:
            if lenth == len(Items): # 项目集不再变化
                break
            lenth = len(Items)
            for item in Items:
                # 判断下一个字符是否为终结符或者当前状态为规约状态
                if item.next_symbol() is not None and isinstance(item.next_symbol(),Nonterminal):
                    nonTerminalSymbol = item.next_symbol()
                    symbolString = []
                    if item.beta_a()[0] is not None:
                        for j in item.beta_a()[0]:
                            symbolString.append(j)
                    symbolString.extend(item.beta_a()[1])
                    lookahead = first(symbolString) #展望符列表
                    for production in self.cfg.get_rules(nonTerminalSymbol): #遍历增广文法产生式
                        if production not in productions:
                            productions.append(production)
                            Items.append(Item(production,lookahead))
        return Items



    def goto(self, i, x) -> []:
        '''
        移入x时项集i的转换 [A -> a.Xp, a]
        :param i:项集
        :param x: 文法符号
        :return: 转换后的项集
        '''
        pass

    def items(self, G) -> [[]]:
        '''
        求G上的项集族
        :param G: 增广文法
        :return:
        '''
        # 初始化项集族为[G->.p, $]
        self.item_family = [self.closure(Item(G.start_symbol(), ['$'])),]
        for I in self.item_family:
            # 获得该项集中所有的下一个symbol
            all_symbols = []
            for i in I:
                one_symbol = i.next_symbol()
                if one_symbol is not None:
                    all_symbols += one_symbol
            for s in all_symbols:
                new_I = self.goto(I, s)
                if new_I is not None and new_I not in self.item_family:
                    self.item_family.append(new_I)

    def table(self, G):
        '''
        G的规范LR语法分析器的函数action和goto
        :param G:  增广文法
        :return:
        '''
        pass

    def program(self):
        '''
        进行语法分析
        :return:
        '''

        self.table(self.cfg)
        pass


