from datetime import datetime

from myparser.cfg import Cfg, Nonterminal, Terminal, Empty, Production
from myparser.item import Item
from lexer.Tag import Tag
from myparser.node import Node


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
        # first 集
        self.firsts = {}
        # 树结构
        self.root_node = None
        # 错误，其中每个错误项是一个元组，(错误行号， 可能的错误的字符)
        self.errors = []

    def closure(self, items) -> []:
        '''
        求项集i的闭包
        :param i:项集 列表
        :return: 项集i的闭包的一个列表 []
        '''
        first_dict = {}
        derive_list = []
        def derive_empty(a):
            '''
            输入一个非终结符，判断该非终结符是否能导出空
            :param a: 符号
            :return: 是否能够导入空
            '''
            if isinstance(a, Terminal) or isinstance(a, Empty):
                return False
            if not isinstance(a, Nonterminal):
                raise TypeError

            derive_list.append(a)
            rules = self.cfg.get_rules(a)
            for rule in rules:
                if Empty() in rule.body:
                    return True
            for rule in rules:
                body_list = rule.body
                if body_list[0] in derive_list:
                    continue
                return derive_empty(body_list[0])

        def first(a):

            '''
            获得从文法a推到得到的串的首符号的集合(a 表示alpha)
            :param a:文法符号
            :return: 终结符符号和空串集合
            '''
            if isinstance(a, Terminal):
                return [a,]
            elif isinstance(a, Empty):
                return [Empty()]
            elif not isinstance(a, Nonterminal):
                raise TypeError

            result = set()
            if a not in first_dict.keys():
                first_dict[a] = []
            rules = self.cfg.get_rules(a)
            for rule in rules:
                for s in rule.body:
                    # 说明在求first集是产生了循环
                    if s in first_dict.keys():
                        first_s = first_dict[s]
                        if derive_empty(s):
                            first_s.append(Empty())
                    else:
                        first_s = first(s)
                    result = result.union(first_s)
                    if Empty() not in first_s:
                        break
            return set(result)

        def first_beta_a(item):
            '''
            求项集item的beta_a 的first集
            :param item:
            :return:
            '''
            beta_a = item.beta_a()
            beta_a_s = []
            beta_a_s.extend(beta_a[0])
            first_set = set()
            p_is_empty = False
            for s in beta_a_s:
                if s == beta_a_s[-1]:
                    p_is_empty = True
                if s not in self.firsts.keys():
                    temp_first = first(s)
                    self.firsts[s] = temp_first
                else:
                    temp_first = first(s)
                first_set = first_set.union(temp_first)
                first_set.discard(Empty())
                if Empty() not in temp_first:
                    p_is_empty = False
                    break
            if p_is_empty:
                first_set = first_set.union(beta_a[1])
            return first_set


        # items
        # items1
        scan_items = items[:]
        set_scan_items = set(scan_items)
        for item in scan_items:
            #print(len(scan_items))
            next_symbol = item.next_symbol()
            if not isinstance(next_symbol, Nonterminal):
                continue
            first_set = first_beta_a(item)
            productions = self.cfg.get_rules(next_symbol)
            for p in productions:
                new_item = Item(p, list(first_set))
                if new_item.next_symbol() is not None:
                    if new_item in set_scan_items:
                        continue
                    scan_items.append(new_item)
                    set_scan_items.add(new_item)
                flag = True
                for i in items:
                    if i.union_symbol(new_item):
                        flag = False
                        for s in first_set:
                            if s not in i.symbols:
                                i.symbols.append(s)
                        break
                if flag:
                    items.append(new_item)
        return items

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
        start_items = [Item(start_production, [Terminal(Tag.END, '$')])]
        temp_family = self.closure(start_items)
        self.item_family.append(temp_family)
        max_int = datetime.now() - datetime.now()
        index = 0
        for I in self.item_family:
            index_I =  index
            index += 1
            # 获得该项集中所有的下一个symbol
            all_symbols = []
            for i in I:
                one_symbol = i.next_symbol()
                # 如果存在某一项没有next symbol,那么以及进行规约，加入到action中
                if one_symbol is None:
                    # 设置接收状态

                    if index_I in self.actions.keys():
                        if i.production.header == self.cfg.start_symbol():
                            self.actions[index_I] = self.actions[index_I].add((i.symbols[0], -1, i.symbols))
                        else:
                            self.actions[index_I] = self.actions[index_I].union({(look_symbol, 1, i.get_production()) for look_symbol in i.symbols})
                    else:
                        if i.production.header == self.cfg.start_symbol():
                            self.actions[index_I] = {(i.symbols[0], -1, -1)}
                        else:
                            self.actions[index_I] = {(look_symbol, 1, i.get_production()) for look_symbol in i.symbols}
                if one_symbol is not None:
                    all_symbols.append(one_symbol)
            for s in all_symbols:
                t1 = datetime.now()
                new_I = self.goto(I, s)
                t2 = datetime.now()
                #print(t2 -t1)
                if t2 - t1 > max_int:
                    max_int = t2-t1

                if new_I is not None and new_I not in self.item_family:
                    self.item_family.append(new_I)
                    index_new_I = len(self.item_family)-1
                else:
                    index_new_I = self.item_family.index(new_I)

                # 如果此时s是终结符，那么加入到actions中，并设为移入
                if isinstance(s, Terminal):

                    if index_I in self.actions.keys():
                        self.actions[index_I].add((s, 0, index_new_I))
                    else:
                        self.actions[index_I] = {(s, 0, index_new_I),}
                else:  # 如果为非终结符，那么加入到gotos中
                    if  index_I in self.gotos.keys():
                        # 设置接收状态
                        if s == self.cfg.get_rules(self.cfg.start_symbol())[0].body[0]:
                            self.gotos[index_I].add((s, -1))
                        else:
                            self.gotos[index_I].add((s, index_new_I))
                    else:
                        self.gotos[index_I] = {(s, index_new_I),}
        print("求一个项集花费的最长时间为:" + str(max_int))

    def program(self):
        '''
        进行语法分析
        :return:
        '''
        def move():
            nonlocal look
            token = self.lexer.getnexttoken()
            look = Terminal.init_token(token[1])

        # 2 -> A ->3 -> action token
        def error_handler():
            '''
            错误处理
            :return:
            '''
            self.errors.append((self.lexer.row, look))
            top_state = state_stack[-1]
            sub_nodes = []
            while top_state not in self.gotos.keys():
                state_stack.pop()
                sub_nodes.append(node_stack.pop())
                top_state = state_stack[-1]
            goto_actions = self.gotos[top_state]

            # 遍历当前栈顶状态下可以移入的所有非终结符
            # 这样做的目的就是尽可能少的忽略token
            while True:
                if len(state_stack) == 1:
                    state_stack[1] = 2
                    return
                move()
                for action in goto_actions:
                    restore_flag = False
                    # 对应于移入一个非终结符之后的状态
                    infer_state = action[1]
                    flag1 = False
                    if look == Terminal(Tag.END, '$'):
                        flag1 = True
                    for action_action in self.actions[infer_state]:
                        # 找到了一个可以进行回复的look
                        if action_action[0] == look:
                            restore_flag = True
                            flag1 = False
                            break
                    if flag1:
                        while top_state not in self.gotos.keys():
                            state_stack.pop()
                            node_stack.pop()
                            top_state = state_stack[-1]
                        goto_actions = self.gotos[top_state]
                    if restore_flag:
                        state_stack.append(action[1])
                        node_stack.append(Node(action[0], self.lexer.row))
                        node_stack[-1].sub_nodes = sub_nodes
                        return


        t1 = datetime.now()
        self.table(self.cfg)
        t2 = datetime.now()
        print("求闭包花费的时间为：" + str(t2-t1))

        # 初始化时将0状态放入状态栈中
        state_stack = [0,]
        node_stack = []
        # look为将下一个token变成的终结符
        look = None
        move()
        while True:
            # print(look)
            # print(state_stack)
            state_actions =  self.actions[state_stack[-1]]
            error_flag1 = True
            for action in state_actions:
                if action[0] == look:
                    error_flag1 = False
                    #接收状态
                    if action[1] == -1:
                        if len(state_stack) != 2:
                            raise None # 规约完G之后还有问题
                        self.root_node = Node(self.cfg.start_symbol())
                        self.root_node.add_subnode(node_stack[0])
                        return

                    # 移入操作
                    elif action[1] == 0:
                        state_stack.append(action[2])
                        node_stack.append(Node(look, self.lexer.row))
                        move()
                        break
                    # 规约操作
                    else:
                        production = action[2]
                        num_of_s = production.get_num_body_smybol()
                        r_node = Node(production.header)
                        r_row = self.lexer.row
                        for i in range(num_of_s):
                            state_stack.pop()
                            r_row = node_stack[-1].lex_line
                            r_node.add_subnode(node_stack.pop())
                        r_node.lex_line = r_row
                        goto_action = self.gotos[state_stack[-1]]
                        error_flag = True
                        for action in goto_action:
                            if action[0] == production.header:
                                error_flag = False
                                state_stack.append(action[1])
                                node_stack.append(r_node)
                        if error_flag:
                            error_handler()
                        # 表明在该状态下该字符对应的动作为空
            if error_flag1:
                error_handler()






