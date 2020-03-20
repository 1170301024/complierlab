# DFA中的状态，自动机的输入只识别ascii码
class State():
    # 初始化每个状态的转移函数
    def __init__(self):
        #每个状态转换函数表示为字典的形式
        self.transfunc = {}



    # 设置该状态的接受token 并且将该状态设为接受状态
    def settoken(self, token):
        self.token = token
        self.acc = True

    # 判断该状态是否为接受状态
    def ifaccept(self):
        return self.acc

    # 增加状态转换函数
    def addtrans(self, input, targetstate):
        self.transfunc[input] = targetstate

    # 获得下一个状态
    def trans(self, input):
        if self.transfunc[input] is None:
            return -1
        return self.transfunc[input]

    def __str__(self):
        return str(self.transfunc)
