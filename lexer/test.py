from lexer.lexer import Lexer
test = Lexer()

while(True):
    token = test.getnexttoken()
    print(token)
    if(token.code == "end"):
        break