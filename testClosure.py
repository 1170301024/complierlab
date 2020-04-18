from lexer.Tag import Tag
from lexer.lexer import Lexer
from myparser.cfg import Production, Nonterminal, Terminal
from myparser.item import Item
from myparser.parser import Parser

if __name__ == '__main__':
    lexer = Lexer()
    parser = Parser(lexer)
    items = []
    items.append(Item(Production(Nonterminal('G'), [Nonterminal('program')]),[Terminal(Tag.END,'$')]))
    for item in parser.closure(items):
        print(item.__str__())