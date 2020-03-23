import os
import tkinter
from tkinter import *
from tkinter import filedialog, ttk

from lexanalysis import LexAnalysis

root = Tk()
root.title('编译原理实验')
root.geometry('800x800')

class UI:
    def __init__(self, lexer):
        self.lexer = lexer
        self.contentList = None
        self.lexical = False
        # self.maxSize = 5000*3
        # root.maxsize(self.maxSize,self.maxSize)

    def root(self):
        """
        主界面：定义菜单以及事件处理
        :return:void
        """
        #相应列表
        def save():
            file_path = filedialog.asksaveasfilename(title=u'保存文件')
            print('保存文件：', file_path)
            file_text = content.get('1.0',END)
            if file_path is not None:
                with open(file=file_path, mode='a+', encoding='utf-8') as file:
                    file.write(file_text)
                print('保存完成')
            else:
                print('文件未保存')


        def openfile():
            '''
            读取系统文件，返回文件名
            :return:文件路径
            '''
            file_path = filedialog.askopenfilename(title='打开文件', filetype=[('all files', '')])
            print('打开文件', file_path)
            return file_path

        def table():
            '''
            读取转换表
            :return: void
            '''
            file = openfile()
            if file == '':
                return
            self.lexer.initDFA(path = file)
            # lb1 = Label(root, text='读取转换表成功', font=('黑体', 16, 'bold'))
            # lb1.place(relx=0.5, rely=0.5)
            # self.lexer.testinitDFA()

        def fileToContent(file):
            '''
            读取文件到前端
            :param file:
            :return:
            '''
            file_program = open(file, "r", encoding="utf-8")
            self.contentList = file_program.readlines()
            str_data = ''.join(self.contentList)
            content.delete('1.0',END)
            content.insert(tkinter.END,str_data)
            for i in range(0,len(self.contentList)):
                if i == 0:
                    line.insert(tkinter.END, str(i + 1))
                    continue
                line.insert(tkinter.END,'\n'+str(i+1))

        def source():
            '''
            读取源文件
            :return: void
            '''
            file = openfile()
            if file == '':
                return
            file_program = open(file, "r", encoding="utf-8")
            self.lexer.program = file_program.read()

            fileToContent(file)

        def lexicalRule():
            '''
            词法规则界面以及dfa转换表构建
            :return: void
            '''
            window = Tk()
            window.title('词法规则')
            window.geometry('1200x600')
            window.resizable(0, 0)
            lb = Label(window, text='词法规则', font=('黑体', 16, 'bold'))
            lb.place(relx = 0.5,rely = 0.0)
            lb1 = Label(window,text='词法规则', font=('黑体', 16, 'bold'))
            lb1.place(relx = 0.25,rely = 0.1)
            lb2 = Label(window, text='状态转换表', font=('黑体', 16, 'bold'))
            lb2.place(relx=0.75, rely=0.1)

            # 词法规则
            content = Text(window, width=70, height=30)
            content.place(x=30, y=90)
            fileName = '../lexicalRules'
            file = open(fileName, 'r', encoding="utf-8")
            strTemp = ''.join(file.readlines())
            content.insert(tkinter.END,strTemp)

            #状态转换表
            column = set() # 集合，元素不重复
            totalStates = self.lexer.states # (终结符，终止态)
            lines = len(totalStates)
            count = 1
            endState = []
            for i in totalStates:
                if i.ifaccept():
                    endState.append(count)
                count+=1
                for j in i.transfunc.keys(): #dict_keys([]) 迭代形式
                     column.add(j)
            column = list(column) #终结符集合
            column.sort()
            column.insert(0,'state')
            # print('column: ',column)

            for x in range(lines):
                for y in range(len(column)):
                    pass
            frame = Frame(window,width=30)
            frame.place(x=630, y=90)
            treeview = ttk.Treeview(frame, height = 19, columns = column,show = 'headings')
            # treeview.place(x=630, y=90)
            # ----vertical scrollbar------------
            vbar = ttk.Scrollbar(frame, orient=VERTICAL, command=treeview.yview)
            treeview.configure(yscrollcommand=vbar.set)
            # vbar.place(x=1170,y=90)
            treeview.grid(row=0, column=0, sticky=NSEW)
            vbar.grid(row=0, column=1, sticky=NS)
            # ----horizontal scrollbar----------
            hbar = ttk.Scrollbar(frame, orient=HORIZONTAL, command=treeview.xview)
            treeview.configure(xscrollcommand=hbar.set)
            # hbar.place(x=630,y=390)
            # hbar.pack(side = BOTTOM, fill = X)
            hbar.grid(row=1, column=0, sticky=EW)
            window.rowconfigure(0,weight = 1)
            window.columnconfigure(0,weight=1)
            for head in column:
                treeview.column(head, width=50, anchor='center')
                test = head
                if head == '\t':
                    test = '\\t'
                elif head == ' ':
                    test = 'space'
                elif head == '\n':
                    test = '\\n'
                elif head == '\r':
                    test = '\\r'
                treeview.heading(head,text=test)


            # 表格
            count = 1
            for i in totalStates:
                temp = treeview.insert('', index = count) # 新建行
                if count in endState:
                    treeview.set(temp, column=column[0], value=str(count)+'(end)')
                else:
                    treeview.set(temp, column=column[0], value=count)
                for j in i.transfunc.keys():  # dict_keys([]) 迭代形式
                    treeview.set(temp,column=j, value=i.transfunc[j])
                count += 1

        def lexicalAnalysis():
            '''
            词法分分析情况：token序列，识别过程，错误情况
            :return:
            '''
            window = Tk()
            window.title('词法分析')
            window.geometry('1200x600')
            window.resizable(0, 0)
            lb = Label(window, text='词法分析', font=('黑体', 16, 'bold'))
            lb.place(relx=0.5, rely=0.0)
            lb1 = Label(window, text='词法单元', font=('黑体', 16, 'bold'))
            lb1.place(relx=0.10, rely=0.1)
            lb1 = Label(window, text='DFA', font=('黑体', 16, 'bold'))
            lb1.place(relx=0.50, rely=0.1)
            lb2 = Label(window, text='错误项', font=('黑体', 16, 'bold'))
            lb2.place(relx=0.80, rely=0.1)


            #词法单元
            type = ['input','token','line']
            treeview = ttk.Treeview(window, height = 19, columns = type,show = 'headings')
            treeview.place(x=30, y=90)
            for head in type:
                treeview.column(head, width=100, anchor='center')
                treeview.heading(head, text=head)
            # # ----vertical scrollbar------------
            # vbar = ttk.Scrollbar(window, orient=VERTICAL, command=treeview.yview)
            # treeview.configure(yscrollcommand=vbar.set)
            # vbar.pack(, fill = Y)

            #DFA
            menu = ['word','process']
            treeview1 = ttk.Treeview(window, height = 19, columns = menu,show = 'headings')
            treeview1.place(x=430, y=90)
            treeview1.column(menu[0], width=50, anchor='center')
            treeview1.heading(menu[0], text=menu[0])
            treeview1.column(menu[1], width=300, anchor='center')
            treeview1.heading(menu[1], text=menu[1])
            # # ----vertical scrollbar------------
            # vbar = ttk.Scrollbar(window, orient=VERTICAL, command=treeview1.yview)
            # treeview1.configure(yscrollcommand=vbar.set)
            # vbar.pack(side = RIGHT, fill = Y)

            #错误
            error = ['error','reason']
            treeview2 = ttk.Treeview(window, height = 19, columns = error,show = 'headings')
            treeview2.place(x=830, y=90)
            treeview2.column(error[0], width=50, anchor='center')
            treeview2.heading(error[0], text=error[0])
            treeview2.column(error[1], width=300, anchor='center')
            treeview2.heading(error[1], text=error[1])
            # # ----vertical scrollbar------------
            # vbar = ttk.Scrollbar(window, orient=VERTICAL, command=treeview2.yview)
            # treeview2.configure(yscrollcommand=vbar.set)
            # vbar.pack(side = RIGHT, fill = Y)
            #handle
            currentLine = 0
            i = 0
            while True and not self.lexical:
                recieve = self.lexer.getnexttoken()
                # if 'error' in recieve[1]:
                #     treeview2.insert('',i,value=recieve[1])
                input = recieve[0]
                while input not in self.contentList[currentLine]:
                    currentLine += 1
                token = recieve[1]
                if (token.code == "end"):
                    break
                record = recieve[2]
                # print(input, ' ', token, ' ', currentLine, '\n')
                treeview.insert('', i, value=(input, token, currentLine + 1))
                treeview1.insert('',i, value=(input,record))
                i += 1
            self.lexical = True
            window.mainloop()

        def syntaxRule():
            pass

        def syntaxAnalysis():
            pass

        def semanticsRule():
            pass

        def semanticsAnalysis():
            pass

        def projectDir():
            '''
            配置项目目录结构
            :return:
            '''
            def selectEvent(event):
                for item in treeview.selection():
                    item_text = item
                    # item_text = treeview.item(item,'values')
                    # print(item)
                    if item_text == 'token':
                        tokenhandler()
                    elif item_text == 'token.py':
                        tokenpyhandler()
                    elif item_text == 'test.py':
                        testpyhandler()
                    elif item_text == 'UI.py':
                        UIhandler()
                    elif item_text == 'lexicalRules':
                        lexicalRuleshandler()
                    elif item_text == 'lexanalysis.py':
                        lexanalysishandler()
                    elif item_text == 'hello':
                        hellohandler()
                    elif item_text == 'dfa_table':
                        dfa_tablehandler()
                    elif item_text == 'test.py':
                        testpyhandler()

            #Handler
            def tokenhandler():
                fileToContent('../token')

            def tokenpyhandler():
                fileToContent('../token.py')

            def lexanalysishandler():
                fileToContent('../lexanalysis.py')

            def statehandler():
                fileToContent('../state.py')

            def dfa_tablehandler():
                fileToContent('../dfa_table')

            def UIhandler():
                fileToContent('UI.py')

            def hellohandler():
                fileToContent('../hello')

            def lexicalRuleshandler():
                fileToContent('../lexicalRules')

            def testpyhandler():
                fileToContent('../test.py')

            treeview = ttk.Treeview(root)
            treeview.place(relx=0.75, rely=0.2)
            firstClass = ['source', 'lexer', 'parser', 'semantic']
            firstClassDir = []
            secondClass1 = ['ui', 'dfa_table', 'hello', 'lexanalysis.py', 'lexicalRules', 'state.py'
                , 'test.py', 'token', 'token.py']

            secondClass2 = []
            secondClass3 = []

            rootDir = treeview.insert('', 0, 'project', text='project', value=('project'))
            count = 0
            for temp in firstClass: #一级目录
                tempDir = treeview.insert(rootDir, count, temp, text=temp, value=(temp))
                count += 1
                firstClassDir.append(tempDir)
            count = 0

            # for temp in secondClass1:#lexer
            #     tempDir = treeview.insert(firstClassDir[0], count, temp, text=temp, value=(temp))
            #     count += 1
            #     if tempDir == 'ui':
            #         uiNode = treeview.insert(tempDir, count, 'UI.py', text='UI.py', value=('UI.py'))
            # treeview.bind('<Button-1>',selectEvent)

        def config():
            '''
            配置主界面
            :return:
            '''
            #错误信息
            error = ['error', 'reason']
            treeview2 = ttk.Treeview(root, height=10, columns=error, show='headings')
            treeview2.place(x=0, y=600)
            treeview2.column(error[0], width=50, anchor='center')
            treeview2.heading(error[0], text=error[0])
            treeview2.column(error[1], width=1000,anchor='center')
            treeview2.heading(error[1], text=error[1])
            '''
            需要错误信息返回值
            '''

            #项目文件
            projectDir()

        #菜单初始化
        menubar = Menu(root)

        # 屏幕显示
        scY = Scrollbar(root)
        scX = Scrollbar(root, orient=HORIZONTAL)
        scY.pack(side=RIGHT, fill=Y)
        scX.pack(side=BOTTOM, fill=X)
        content = Text(root, width=70, height=30, yscrollcommand=scY.set, xscrollcommand=scX.set)
        content.place(x=30, y=50)

        # 行数显示
        line = Text(root, width=3, height=30, yscrollcommand=scY.set)
        line.place(x=0, y=50)
        line.configure(background='Gray')

        menuList = ['词法规则','词法分析','语法规则','语法分析','语义规则','语义分析']
        eventList = [lexicalRule,lexicalAnalysis,syntaxRule,syntaxAnalysis,semanticsRule,semanticsAnalysis]
        fileOpen = Menu(menubar)
        fileOpen.add_command(label='打开转换表文件',command=table)
        fileOpen.add_command(label='打开源文件', command=source)
        fileOpen.add_command(label='保存', command=save)
        menubar.add_cascade(label='文件', menu=fileOpen)
        totalMenu = Menu(menubar)
        for menu,event in zip(menuList,eventList):
            totalMenu.add_command(label = menu, command = event)
        menubar.add_cascade(label='功能', menu=totalMenu)
        root.config(menu=menubar)

        #配置主界面
        config()

        root.mainloop()


if __name__ == '__main__':
    lexer = LexAnalysis()
    ui = UI(lexer)
    ui.root()