from lexer.Tag import Tag
from lexer.lexer import Lexer
from myparser.cfg import Cfg, Terminal
from myparser.item import Item
from myparser.parser import Parser

if __name__ == '__main__':
    def test_cfg():
        cfg = Cfg()
        print(cfg)
    def test_item():
        cfg = Cfg()
        test = Item(cfg.get_rules(cfg.S)[0], ['$'])
        # 测试对象
        print(test)

        def test_next_item():
            print(test.next_item())

        def test_beta_a():
            print(test.beta_a())

        def test_next_symbol():
            test1 = test.next_symbol()
            for r in cfg.get_rules(test1):
                print(r)

        print("beta_a")
        test_beta_a()
        print("next_item")
        test_next_item()
        print("next_symbol")
        test_next_symbol()

    def test_parser_items():
        lexer = Lexer()
        parser = Parser(lexer)
        parser.table(parser.cfg)
        k = 0
        for items in parser.item_family:
            print("S" + str(k))
            for i in items:
                print(i)
            k += 1

    def test():
        lexer = Lexer()
        parser = Parser(lexer)
        parser.table(parser.cfg)
        print("goto表")
        for i, v in parser.gotos.items():
            print(str(i) + ':')
            for j in v:
                print(str(j[0]), str(j[1]))

        print("action表")
        for i, v in parser.actions.items():
            print(str(i) + ':')
            for j in v:
                print(str(j[0]), str(j[1]), str(j[2]))
    def test_parser_program():
        lexer = Lexer()
        lexer.program="int m;z=0x12;m = 2+3*4;char c= 'a';double b = 1;int[2][4] h;int[3] a;a[0] = 2;while(m>2)doif(m<8)m = m +1;else m = m*2;"
        lexer.initDFA("lexer/dfa_table")
        parser = Parser(lexer)
        parser.program()



    # test_cfg()
    # test_item()
    # test_parser_items()
    #test()
    test_parser_program()