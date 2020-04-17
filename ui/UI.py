import tkinter
from tkinter import *
from tkinter import filedialog, ttk ,messagebox

from lexer.Tag import Tag
from lexer.lexer import Lexer
from myparser.parser import Parser

root = Tk()
root.title('编译原理实验')
root.geometry('1000x600')
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()


class UI:
    errorTreeview = None

    def __init__(self, lexer):
        self.parser = None
        self.lexer = lexer
        self.contentList = None
        self.content = None
        self.line = None
        self.errline = 0

        # 当前在content中的文件
        self.curfile = None

        #ProjectTree
        self.treeview = None
        self.projectDir = []
        self.filePath = {}
        # self.maxSize = 5000*3
        # root.maxsize(self.maxSize,self.maxSize)

        #ErrorTree

        self.errorTreeview = None

    def root(self):
        """
        主界面：定义菜单以及事件处理
        :return:void
        """

        #保存文件到相应文件
        def save_file():
            file_text = self.content.get('1.0', END)

            if(self.curfile in self.filePath.keys()):
                file_path = self.filePath[self.curfile]
                print(file_path)
            else:
                file_path = filedialog.asksaveasfilename(title=u'保存文件')
                print('保存文件：', file_path)

            if file_path is not None:
                with open(file=file_path, mode='w+', encoding='utf-8') as file:
                    file.write(file_text)
                print('保存完成')
            else:
                print('文件未保存')

        #辅助函数：读文件
        def read_file():
            '''
            读取系统文件，返回文件名
            :return:文件路径
            '''
            file_path = filedialog.askopenfilename(title='打开文件', filetype=[('all files', '')])
            print('打开文件', file_path)
            return file_path

        #前端显示文件
        def fileToContent(file):
            file_program = open(file, "r", encoding="utf-8")
            self.contentList = file_program.readlines()
            str_data = ''.join(self.contentList)
            self.content.delete('1.0',END)
            self.line.delete('1.0',END)
            self.content.insert(tkinter.END,str_data)
            for i in range(0,len(self.contentList)):
                if i == 0:
                    self.line.insert(tkinter.END, str(i + 1))
                    continue
                self.line.insert(tkinter.END,'\n'+str(i+1))

        #读取转换表：lexer
        def read_DFA_table():
            file = read_file()
            if file == '':
                return
            self.lexer.initDFA(path = file)
            # lb1 = Label(root, text='读取转换表成功', font=('黑体', 16, 'bold'))
            # lb1.place(relx=0.5, rely=0.5)
            # self.lexer.testinitDFA()
            fileName = file.split('/')[-1]
            item = self.projectDir[0][1]
            self.treeview.insert(item,0,fileName,text=fileName,value=(fileName))
            self.filePath[fileName] = file
            # fileToContent(file)

        #打开文件，读取源文件
        def open_file():
            file = read_file()
            if file == '':
                return
            file_program = open(file, "r", encoding="utf-8")
            self.lexer.program = file_program.read()
            fileName = file.split('/')[-1]
            item = self.projectDir[0][0]
            self.treeview.insert(item, 0, fileName, text=fileName, value=(fileName))
            self.filePath[fileName] = file
            self.curfile = fileName
            fileToContent(file)

        def lexicalRule():
            '''
            词法规则界面以及dfa转换表构建
            :return: void
            '''
            if self.lexer.states == None:
                tkinter.messagebox.showinfo('提示', '未读取转换表文件')
                return
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

            frame = Frame(window)
            # frame.place(x=630, y=90)
            frame.pack(anchor=W, ipadx=10, side=LEFT, expand=True, fill = X)
            # 词法规则
            content = Text(frame, width=70, height=30)
            content.pack(anchor=W, ipadx=10, side=LEFT, expand=False)
            fileName = '../lexer/lexicalRules'
            file = open(fileName, 'r', encoding="utf-8")
            strTemp = ''.join(file.readlines())
            content.insert(tkinter.END,strTemp)

            #状态转换表
            column = set() # 集合，元素不重复
            totalStates = self.lexer.states # (终结符，终止态)
            lines = len(totalStates)
            count = 0
            endState = [] #储存接收状态  加（end）
            for i in totalStates:
                if i.ifaccept(): #接收状态
                    endState.append(count)
                count+=1
                for j in i.transfunc.keys(): #dict_keys([]) 迭代形式
                     column.add(j)
            column = list(column) #终结符集合
            column.sort()
            column.insert(0,'state')

            treeview = ttk.Treeview(frame, height = 20, columns = column,show = 'headings')
            treeview.pack(anchor=E,ipadx=100, side=LEFT, expand=True, fill=BOTH)
            # treeview.place(x=630, y=90)
            # ----vertical scrollbar------------
            vbar = ttk.Scrollbar(treeview, orient=VERTICAL, command=treeview.yview)
            treeview.configure(yscrollcommand=vbar.set)
            vbar.pack(side=RIGHT, fill=Y)
            # ----horizontal scrollbar----------
            hbar = ttk.Scrollbar(treeview, orient=HORIZONTAL, command=treeview.xview)
            treeview.configure(xscrollcommand=hbar.set)
            hbar.pack(side = BOTTOM, fill = X)
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
            count = 0
            for i in totalStates:
                temp = treeview.insert('', index = count) # 新建行
                if count in endState: #若为接收状态
                    treeview.set(temp, column=column[0], value='*'+str(count))
                else:
                    treeview.set(temp, column=column[0], value=count)
                for j in i.transfunc.keys():  # dict_keys([]) 迭代形式
                    treeview.set(temp,column=j, value=i.transfunc[j])
                count += 1

        #词法分析
        def lexicalAnalysis():
            '''
            词法分分析情况：token序列，识别过程，错误情况
            :return:
            '''
            if self.lexer.program == None:
                tkinter.messagebox.showinfo('提示', '未读取分析文件')
                return
            if self.lexer.states == None:
                tkinter.messagebox.showinfo('提示', '未读取转换表文件')
                return
            self.lexer.program = self.content.get('0.0','end')
            self.contentList = self.content.get("0.0","end").split("\n")
            self.contentList.pop()#列表最后一个元素是空删除它

            window = Tk()
            window.title('词法分析')
            window.geometry('1200x600')
            window.resizable(0, 0)
            lb = Label(window, text='词法分析', font=('黑体', 16, 'bold'))
            lb.place(relx=0.5, rely=0.0)
            lb1 = Label(window, text='词法单元', font=('黑体', 16, 'bold'))
            lb1.place(relx=0.25, rely=0.1)
            lb1 = Label(window, text='DFA', font=('黑体', 16, 'bold'))
            lb1.place(relx=0.75, rely=0.1)

            frame = Frame(window)
            # frame.place(x=630, y=90)
            frame.pack(anchor=W, ipadx=10, side=LEFT, expand=True, fill = X)
            frame1 = Frame(window)
            frame1.pack(anchor=E, ipadx=10, side=LEFT, expand=True, fill = X)
            # tianchong
            content = Text(frame, width=0, height=30)
            content.pack(anchor=W, side=LEFT, expand=False)
            content.configure(background=window.cget('background'),highlightbackground=window.cget('background'))
            content1 = Text(frame1, width=0, height=30)
            content1.pack(anchor=E, side=LEFT, expand=False)
            content1.configure(background=window.cget('background'),highlightbackground=window.cget('background'))
            #词法单元
            type = ['input','token','line']
            treeview = ttk.Treeview(frame, height = 19, columns = type,show = 'headings')
            treeview.pack(anchor=W, ipadx=100, side=LEFT, expand=True, fill=BOTH)
            for head in type:
                treeview.column(head, width=200, anchor='center')
                treeview.heading(head, text=head)
            # ----vertical scrollbar------------
            vbar = ttk.Scrollbar(treeview, orient=VERTICAL, command=treeview.yview)
            treeview.configure(yscrollcommand=vbar.set)
            vbar.pack(side=RIGHT, fill=Y)
            # ----horizontal scrollbar----------
            hbar = ttk.Scrollbar(treeview, orient=HORIZONTAL, command=treeview.xview)
            treeview.configure(xscrollcommand=hbar.set)
            hbar.pack(side=BOTTOM, fill=X)
            #DFA

            menu = ['word','process']
            treeview1 = ttk.Treeview(frame1,  height = 19, columns = menu,show = 'headings')
            treeview1.pack(anchor=W, ipadx=100, side=LEFT, expand=True, fill=BOTH)
            treeview1.column(menu[0], width=100, anchor='center',stretch=False)
            treeview1.heading(menu[0], text=menu[0])
            treeview1.column(menu[1], width=1000, anchor='w',stretch=False)
            treeview1.heading(menu[1], text=menu[1], anchor='w')
            # ----vertical scrollbar------------
            vbar1 = ttk.Scrollbar(treeview1, orient=VERTICAL, command=treeview1.yview)
            treeview1.configure(yscrollcommand=vbar1.set)
            vbar1.pack(side=RIGHT, fill=Y)
            # ----horizontal scrollbar----------
            hbar1 = ttk.Scrollbar(treeview1, orient=HORIZONTAL, command=treeview1.xview)
            treeview1.configure(xscrollcommand=hbar1.set)
            hbar1.pack(side=BOTTOM, fill=X)
            window.rowconfigure(0, weight=1)
            window.columnconfigure(0, weight=1)

            content2 = Text(frame1, width=0, height=30)
            content2.pack(anchor=W, side=LEFT, expand=False)
            content2.configure(background=window.cget('background'), highlightbackground=window.cget('background'))

            currentLine = 0
            clear(self.errorTreeview)
            while True:
                recieve = self.lexer.getnexttoken()
                input = recieve[0]
                token = recieve[1]
                if (token.code == 'error'):
                    print(token.attr)
                    errorHandler(input, token)
                    continue
                while input not in self.contentList[currentLine]: #行号记录
                    currentLine += 1
                if (token.code == "end"):
                    break
                record = recieve[2]
                # print(input, ' ', token, ' ', currentLine, '\n')
                treeview.insert('', 'end', value=(input, token, currentLine + 1))
                treeview1.insert('','end', value=(input,record))
            self.lexical = True
            window.mainloop()

        def syntaxRule():
            '''
            用于前端打印LR分析表
            :return:
            '''
            if self.parser == None:
                self.lexer.program = "int m;z=0x12;m = 2+3*4;c= 'a';double b;int[2][4] h;int[3] a;a[0] = 2;while(m>2) if(m<8)m = m +1;else m = m*2;"
                self.lexer.initDFA("../lexer/dfa_table")

                self.parser = Parser(self.lexer)
                self.parser.program()
            gotos = self.parser.gotos
            actions = self.parser.actions


            # 初始化窗口
            window = Tk()
            window.title('LR分析表')
            window.geometry('1200x600')
            window.resizable(0, 0)
            lb = Label(window, text='LR分析表', font=('黑体', 16, 'bold'))
            lb.place(relx=0.5, rely=0.0)
            lb1 = Label(window, text='ACTION', font=('黑体', 16, 'bold'))
            lb1.place(relx=0.25, rely=0.1)
            lb2 = Label(window, text='GOTO', font=('黑体', 16, 'bold'))
            lb2.place(relx=0.75, rely=0.1)

            # 框架用于存放ACTION表
            frame = Frame(window)
            frame.pack(anchor=W, ipadx=10, side=LEFT, expand=True, fill=X)
            # 框架用于存放GOTO表
            frame1 = Frame(window)
            frame1.pack(anchor=E, ipadx=10, side=LEFT, expand=True, fill=X)
            # fill 以对齐->加滚轮
            content = Text(frame, width=0, height=30)
            content.pack(anchor=W, side=LEFT, expand=False)
            content.configure(background=window.cget('background'), highlightbackground=window.cget('background'))
            content1 = Text(frame1, width=0, height=30)
            content1.pack(anchor=E, side=LEFT, expand=False)
            content1.configure(background=window.cget('background'), highlightbackground=window.cget('background'))

            # ACTION: （终结符，转换，状态）
            column = set()  # 集合，元素不重复
            # 加终结符
            keys = ['ID', 'DECIMAL', 'FCONST', 'HEX', 'OCTAL', 'CCONST', 'STRING', 'REL']
            for key in Tag.show_strs.keys():
                column.add(Tag.show_strs[key])
            for key in keys:
                column.add(key)
            column = list(column)  # 终结符集合
            column.sort()
            column.insert(0, 'state')
            treeview = ttk.Treeview(frame, height=19, columns=column, show='headings')
            treeview.pack(anchor=W, ipadx=100, side=LEFT, expand=True, fill=BOTH)
            for head in column:
                treeview.column(head, width=100, anchor='center')
                treeview.heading(head, text=head)
            # ----vertical scrollbar------------
            vbar = ttk.Scrollbar(treeview, orient=VERTICAL, command=treeview.yview)
            treeview.configure(yscrollcommand=vbar.set)
            vbar.pack(side=RIGHT, fill=Y)
            # ----horizontal scrollbar----------
            hbar = ttk.Scrollbar(treeview, orient=HORIZONTAL, command=treeview.xview)
            treeview.configure(xscrollcommand=hbar.set)
            hbar.pack(side=BOTTOM, fill=X)

            count = 0
            for i in range(len(self.parser.item_family)):
                temp = treeview.insert('', index=count)  # 新建行
                treeview.set(temp, column=column[0], value=str(i))
                for goto in actions[i]:  # dict_keys([]) 迭代形式
                    index = column.index(str(goto[0]))
                    if goto[1] == 0:
                        value = 's'+str(goto[2])
                    else:
                        value = str(goto[2])
                    treeview.set(temp, column=index, value=(value))
                count += 1

            # GOTO
            column = set()
            column.add('DS')
            for production in self.parser.cfg.R:
                column.add(str(production.header))
            column = list(column)
            column.insert(0, 'state')
            print(column)
            treeview1 = ttk.Treeview(frame1, height=19, columns=column, show='headings')
            treeview1.pack(anchor=W, ipadx=100, side=LEFT, expand=True, fill=BOTH)
            for head in column:
                treeview1.column(head, width=100, anchor='center')
                treeview1.heading(head, text=head)
            # ----vertical scrollbar------------
            vbar1 = ttk.Scrollbar(treeview1, orient=VERTICAL, command=treeview1.yview)
            treeview1.configure(yscrollcommand=vbar1.set)
            vbar1.pack(side=RIGHT, fill=Y)
            # ----horizontal scrollbar----------
            hbar1 = ttk.Scrollbar(treeview1, orient=HORIZONTAL, command=treeview1.xview)
            treeview1.configure(xscrollcommand=hbar1.set)
            hbar1.pack(side=BOTTOM, fill=X)
            window.rowconfigure(0, weight=1)
            window.columnconfigure(0, weight=1)

            content2 = Text(frame1, width=0, height=30)
            content2.pack(anchor=W, side=LEFT, expand=False)
            content2.configure(background=window.cget('background'), highlightbackground=window.cget('background'))

            count = 0
            for i in range(len(self.parser.item_family)):
                temp = treeview1.insert('', index=count)  # 新建行
                treeview1.set(temp,column=column[0],value=str(i))
                if i not in gotos.keys():
                    continue
                for goto in gotos[i]:  #
                    index = column.index(str(goto[0]))
                    value = str(goto[1])
                    treeview1.set(temp, column=index, value=(value))
                count += 1


            window.mainloop()
        def syntaxAnalysis():
            '''
            用于输出文法分析结果
            :return:
            '''
            if self.lexer.program == None:
                tkinter.messagebox.showinfo('提示', '未读取分析文件')
                return
            if self.parser != None:
                # self.lexer.program = "int m;z=0x12;m = 2+3*4;c= 'a';double b;int[2][4] h;int[3] a;a[0] = 2;while(m>2) if(m<8)m = m +1;else m = m*2;"
                self.lexer.initDFA("../lexer/dfa_table")
                self.parser = Parser(self.lexer)
                self.parser.program()
            nodes = [self.parser.root_node]
            items = []

            # 初始化窗口
            window = Tk()
            window.title('语法分析')
            window.geometry('1200x600')
            window.resizable(0, 0)

            # 树形屏幕显示
            processTree = ttk.Treeview(window)
            processTree.pack(fill=BOTH, expand=YES)

            # insert(parent,index,iid=None,**kw)
            items.append(processTree.insert('',0,text=str(nodes[0].grammar_symbol)+' ('+str(nodes[0].lex_line)+')',open=True))
            for pNode in nodes:
                pNodeItem = items[nodes.index(pNode)]
                subNodes = pNode.get_subnodes()
                for subNode in subNodes:
                    screen_show = subNode.grammar_symbol.__str__()+' ('+str(subNode.lex_line)+')'
                    items.append(processTree.insert(pNodeItem,0,text=screen_show,value=(screen_show),open=True))
                nodes.extend(subNodes)

            window.mainloop()


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
                for item in self.treeview.selection():
                    item_text = self.treeview.item(item, 'values')
                    if item_text[0] not in ['project','source','lexer', 'parser', 'semantic']:
                        self.curfile = item_text[0]
                        fileToContent(self.filePath[item_text[0]])
                    else:
                        continue


            self.treeview = ttk.Treeview(projectframe)
            self.treeview.pack(expand=YES, fill=BOTH)
            firstClass = ['source','lexer', 'parser', 'semantic']

            firstClassDir = []

            rootDir = self.treeview.insert('', 0, 'project', text='project', value=('project'))
            count = 0
            for temp in firstClass: #一级目录
                tempDir = self.treeview.insert(rootDir, count, temp, text=temp, value=(temp))
                count += 1
                firstClassDir.append(tempDir)

            self.projectDir.append(firstClass)
            # count = 0

            # for temp in secondClass1:#lexer
            #     tempDir = treeview.insert(firstClassDir[0], count, temp, text=temp, value=(temp))
            #     count += 1
            #     if tempDir == 'ui':
            #         uiNode = treeview.insert(tempDir, count, 'UI.py', text='UI.py', value=('UI.py'))

            self.treeview.bind('<Button-1>',selectEvent)

        def errorHandler(input,errortoken):
            self.errorTreeview.insert('', self.errline, value=(input, errortoken.attr))
            self.errline += 1

        '''
        清空表
        input: type of treeview
        '''
        def clear(tree):
            x = tree.get_children()
            for item in x:
                tree.delete(item)

        def init_window():


            lineframe = Frame(contentframe, bg='white')
            test = Frame(contentframe)
            lineframe.pack(side=LEFT, anchor=N, fill=Y)
            test.pack(side=LEFT, anchor=N, expand=True, fill=BOTH)

            def multiple_yview(*args):
                self.line.yview(*args)
                self.content.yview(*args)

            # 代码区的滚动条
            scY = Scrollbar(test, command=multiple_yview)
            scX = Scrollbar(test, orient=HORIZONTAL)
            scY.pack(side=RIGHT, fill=Y)
            scX.pack(side=BOTTOM, fill=X)

            # 行数和代码显示
            self.line = Text(lineframe, width=3, yscrollcommand=scY.set)
            self.line.pack(side=LEFT, fill=Y, expand=True)
            self.line.configure(background='Gray')
            self.content = Text(test, width=80, yscrollcommand=scY.set, xscrollcommand=scX.set)
            self.content.pack(side=LEFT, expand=True, fill=BOTH)
            scY.config(command=multiple_yview)

            # 文件菜单
            file_list = ['打开文件', '保存']
            file_event_list = [open_file, save_file]
            file_menu = Menu(menubar)
            for menu, event in zip(file_list, file_event_list):
                file_menu.add_command(label=menu, command=event)
            menubar.add_cascade(label='文件', menu=file_menu)

            # 功能菜单
            # menuList = ['词法规则','词法分析','语法规则','语法分析','语义规则','语义分析']
            action_list = ['DFA转换表','词法分析','LR分析表', '语法分析', '语义分析']
            # eventList = [lexicalRule,lexicalAnalysis,syntaxRule,syntaxAnalysis,semanticsRule,semanticsAnalysis]
            action_event_list = [lexicalRule,lexicalAnalysis, syntaxRule, syntaxAnalysis, semanticsAnalysis]
            action_menu = Menu(menubar)
            for menu, event in zip(action_list, action_event_list):
                action_menu.add_command(label=menu, command=event)
            menubar.add_cascade(label='功能', menu=action_menu)

            # 配置菜单
            config_list = ['配置转换表']
            config_event_list = [read_DFA_table]
            config_menu = Menu(menubar)
            for menu, event in zip(config_list, config_event_list):
                config_menu.add_command(label=menu, command=event)
            menubar.add_cascade(label='配置', menu=config_menu)
            root.config(menu=menubar)

            #错误显示
            error = ['errorline', 'hint']
            self.errorTreeview = ttk.Treeview(messageframe, height=10, columns=error, show='headings')
            width = int(screenwidth/6)
            self.errorTreeview.column(error[0], width= width*2)
            self.errorTreeview.heading(error[0], text=error[0],anchor="w")
            self.errorTreeview.column(error[1], width=width*4)
            self.errorTreeview.heading(error[1], text=error[1],anchor="w")
            self.errorTreeview.pack(side=LEFT,fill=BOTH, expand=True,padx=1)

            '''
            需要错误信息返回值
            '''
            #项目文件
            projectDir()
        # 框架设计
        #frameText = Frame(root)
        untitleframe = Frame(bg='white')
        messageframe = Frame(bg='red')
        projectframe = Frame(untitleframe, bg='red')
        contentframe = Frame(untitleframe, bg='white')

        untitleframe.pack(side=TOP, anchor=W, expand=True, fill=BOTH)
        messageframe.pack(side=BOTTOM, anchor=W)
        contentframe.pack(side=LEFT, anchor=N, expand=True, fill=BOTH)
        projectframe.pack(side=TOP, anchor=E,expand=True, fill=BOTH)
        menubar = Menu(root)
        init_window()

        root.mainloop()


if __name__ == '__main__':
    lexer = Lexer()
    ui = UI(lexer)
    ui.root()