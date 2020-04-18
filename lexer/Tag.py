class Tag:


    AUTO = 256
    BREAK = 257
    CHAR = 258
    CONST = 259
    CONTINUE = 260
    DEFAULT = 261
    DO = 262
    DOUBLE = 263
    ELSE = 264
    ENUM = 265
    EXTERN = 266
    FLOAT = 267
    FOR = 268
    GOTO = 269
    INT = 270
    LONG = 271
    REGISTER = 272
    RETURN =273
    SHORT = 274
    SIGNED = 275
    SIZEOF = 276
    STRUCT = 277
    SWITCH = 278
    TYPEDEF = 279
    UNION = 280
    UNSIGNED = 281
    VOID = 282
    WHILE = 283
    IF = 284
    CASE = 285

    ID = 301
    ADD = 302
    SUB = 303
    MUILT = 304
    DIV = 305
    MOD = 306

    AND = 307
    OR  = 308
    NOT = 309
    REL = 310

    DECIMAL = 311
    HEX = 312
    OCTAL = 313
    FCONST = 314
    CCONST = 315
    STRING = 316

    SEMI = 317
    LRP = 318
    RRP = 319
    DOT = 320
    RP = 321
    LP = 322
    SLP = 323
    SRP = 324
    COM = 325
    COL = 326
    QM = 327
    ASSIGN = 328
    END = 329
    FINISH = 331
    COMMENT = 332
    DELIMITER = 333

    key_show_strs = {'256': 'AUTO', '257':'BREAK' ,  '258':'CHAR', '259':'CONST',  '260':'CONTINUE', '261':'DEFAULT', '262':'DO',
                 '263':'DOUBLE', '264':'ELSE', '265': 'ENUM', '266':'EXTERN', '267':'FLOAT', '268':'FOR', '269':'GOTO',
                 '270':'INT', '271':'LONG', '272':'REGISTER', '273':'RETURN', '274':'SHORT','275': 'SIGNED', '276':'SIZEOF',
                 '277':'STRUCT', '278':'SWITCH', '279':'TYPEDEF', '280':'UNION', '281':'UNSIGNED', '282':'VOID', '283':'WHILE','284':'IF','285':'CASE'}

    other_show_strs = {'302':'+', '303':'-', '304':'*', '305':'/', '306':'%', '307':'&&', '308':'||', '309':'!', '310':'REL',
                 '317':';', '318':'[', '319':']', '320':'.', '321':'}', '322':'{' , '323':'(' , '324':')', '325': ',' ,
                 '326': ':', '327':'?', '328':'=', '329':'$'}

    show_strs = dict(key_show_strs, **other_show_strs)

    show_value = [ID, DECIMAL, FCONST, HEX, OCTAL, CCONST, STRING, REL]

    # 关键字到整数的翻译
    keys_dirt = {'auto' : 256, 'break' : 257,  'char': 258, 'const': 259,  'continue' : 260, 'default': 261, 'do': 262, 'double': 263,
                 'else': 264, 'enum': 265, 'extern': 266, 'float': 267, 'for': 268, 'goto': 269, 'int': 270, 'long': 271, 'register': 272,
                 'return': 273, 'short': 274, 'signed': 275, 'sizeof': 176, 'struct': 277, 'switch': 278, 'typedef': 279, 'union': 280,
                 'unsigned': 281, 'void': 282, 'while': 283, 'if': 284,'case': 285}