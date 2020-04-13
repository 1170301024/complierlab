from myparser.cfg import Cfg
from myparser.item import Item

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
            print(test.next_item(['a']))

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


    test_cfg()
    test_item()