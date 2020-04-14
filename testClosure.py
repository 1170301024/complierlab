from lexer.Tag import Tag
from myparser.cfg import Production, Nonterminal, Terminal
from myparser.item import Item
from myparser.parser import Parser

if __name__ == '__main__':
        parser = Parser()
        items = []
        items.append(Item(Production(Nonterminal('G'), [Nonterminal('P')]),[Terminal(Tag.END,'$')]))
        for item in items:
            print(item.__str__())
        print("")
        for item in parser.closure(items):
            print(item.__str__())