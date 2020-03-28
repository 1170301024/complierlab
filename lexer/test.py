from lexer.lexanalysis import LexAnalysis
test = LexAnalysis()

while(True):
    token = test.getnexttoken()
    print(token)
    if(token.code == "end"):
        break