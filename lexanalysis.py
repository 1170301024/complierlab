from state import State


# Non-printable characters
from token import Token

NPC = ['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', '\x0b', '\x0c', '\x0e',
       '\x0f', '\x10', '\x11', '\x12', '\x13', '\x14', '\x15', '\x16', '\x17', '\x18', '\x19', '\x1a',
       '\x1b', '\x1c', '\x1d', '\x1e', '\x1f']


blank = ['\n', '\r', '\t', ' ']

class LexAnalysis:
    def __init__(self):
        self.init()

    # 获得下一个token
    def getnexttoken(self):
        if(self.forward == len(self.program)):
            return Token("end")
        self.lexmeBegin = self.forward
        curstate = 0
        while(True):
            prestate = curstate
            if (self.forward == len(self.program)):
                break
            input = self.program[self.forward]
            curstate = self.states[curstate].trans(input)
            if(curstate < 0):
                break
            self.forward += 1
        if(self.forward == self.lexmeBegin):
            print(".error in program")
        elif(self.states[prestate].ifaccept()):
            if(self.states[prestate].ifneedattri()):
                token = Token(self.states[prestate].code, self.program[self.lexmeBegin:self.forward])
            else:
                token = Token(self.states[prestate].code, self.states[prestate].attr)
            if(token.code == "delimiter"):
                return self.getnexttoken()
            else:
                return token
        else:
            print("error in program")

    # 初始化词法分析类，从文件读入DFA以及程序实例
    def init(self):
        file_dfa = input("请输入DFA文件名：")

        self.initDFA(file_dfa)
        #self.testinitDFA()
        path_program = input("请输入程序实例文件名：")
        file_program = open(path_program, "r")
        self.program = file_program.read()
        self.lexmeBegin = 0
        self.forward = 0
        #从文件读入程序放入缓存区

    def initDFA(self, path):
        row = 0
        file = open(path, "r")
        for line in file.readlines():
            row += 1
            line = line.strip()
            # 忽略空行
            if len(line) == 0:
                continue
            # 忽略注释
            if(line[0] == '#'):
                continue

            # 将有效行按空白分割并判断合法性
            parts = line.split()
            if(parts[0] == "stotal"):
                self.states = [State() for i in range(int(parts[1]))]
                continue
            if(len(parts) != 3 and len(parts) != 4):
                print("error in %s lines" % (row))
            # 处理转换的第一部分
            sstates = parts[0].split('-')
            dstate = int(parts[2])
            # 处理第四部分token
            if len(parts) == 4:
                unit = parts[3][1:-1].split(',')
                code = unit[0]
                if(len(unit) == 1):
                    self.states[dstate].settoken(code)
                elif(len(unit) == 2):
                    self.states[dstate].settoken(code, unit[1])
                else:
                    print("error")
            # 第一部分可能存在a-b
            for sstate in range(int(sstates[0]), int(sstates[-1]) + 1):
                # 处理第二部分该分支中没有做错误处理
                # a-b
                if len(parts[1]) == 3 and parts[1][1] == '-':
                    inputs = parts[1].split('-')
                    for i in range(ord(inputs[0]), ord(inputs[1]) + 1):
                        self.states[sstate].addtrans(chr(i), dstate)
                # 转义 \.
                elif len(parts[1]) == 2 and parts[1][0] == '\\':
                    self.states[sstate].addtrans(parts[1][1], dstate)
                # 空白
                elif parts[1] == "$blank":
                    for i in blank:
                        self.states[sstate].addtrans(i, dstate)
                # 普通字符或者一些特殊的字符或多个字符
                elif len(parts[1]):
                    for i in range(0, len(parts[1])):
                        if parts[1][i] == '.':
                            for j in range(0, 127):
                                # 跳过不可打印字符
                                if chr(j) in NPC:
                                    continue
                                self.states[sstate].addtrans(chr(j), dstate)
                            break
                        else:
                            self.states[sstate].addtrans(parts[1][i], dstate)
                else:
                    print(parts[1])
                    print("error in %s lines...." % (row))

        print("initialize DFA successfully")

    def testinitDFA(self):
        i = 0
        for state in self.states:
            print("状态%s的转换字典" %(i))
            i += 1
            print(state)