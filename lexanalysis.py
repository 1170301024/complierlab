from state import State


class LexAnalysis:
    def __init__(self):
        self.init()

    # 获得下一个token
    def getnexttoken(self):
        pass

    # 初始化词法分析类，从文件读入DFA以及程序实例
    def init(self):
        file_dfa = input("请输入DFA文件名：")

        self.initDFA(file_dfa)
        self.testinitDFA()
        file_program = input("请输入程序实例文件名：")

        #从文件读入程序放入缓存区

    def initDFA(self, path):
        row = 0
        file = open(path, "r")
        for line in file.readlines():
            row += 1
            line = line.strip()
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
                self.states[dstate].settoken(parts[3])
            # 第一部分可能存在a-b
            for sstate in range(int(sstates[0]), int(sstates[-1]) + 1):
                # 处理第二部分该分支中没有做错误处理
                if len(parts[1]) == 3 and parts[1][1] == '-':
                    inputs = parts[1].split('-')
                    for i in range(ord(inputs[0]), ord(inputs[1])):
                        self.states[sstate].addtrans(chr(i), dstate)
                elif len(parts[1]) == 1:
                    if parts[1][0] == '.':
                        for i in range(0, 129):
                            self.states[sstate].addtrans(chr(i), dstate)
                    else:
                        self.states[sstate].addtrans(parts[1][0], dstate)
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