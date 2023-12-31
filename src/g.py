
import shell
import os

__version__ = "0.1"

# TOKEN CONSTANTS

TT_IF = ["IF", "if"]
TT_THEN = ["THEN", "then"]
TT_ENDIF = ["_ENDIF", "_endif", "_IF", "_if"]
TT_ELSE = ["ELSE", "else"]
TT_DEL = ["DEL", "DEL"]
TT_SUB = ["SUB", "sub"]
TT_ENDSUB = ["_SUB", "_sub"]
TT_GOTO = ["GOTO", "goto"]
TT_PRINT = ["PRINT", "print"]
TT_PRINTSTR = ["STR_PRINT", "str_print"]
TT_NLNPRINT = ["NLN_PRINT", "nln_print"]
TT_INPUT = ["INPUT", "input"]
TT_NEXT = ["NEXT", "next"]
TT_PREV = ["PREV", "prev"]
TT_EXE = ["EXE", "exe"]
TT_EVAL = ["EVAL", "eval"]
TT_NUMPUT = ["NUMPUT", "numput"]
TT_SLEEP = ["SLEEP", "sleep"]
TT_QUIT = ["QUIT", "quit", "EXIT", "exit", "END", "end"]
TT_CLEAR = ["CLEAR", "clear"]
TT_CMD = ["CMD", "cmd"]
TT_GETVARS = ["GETVARS", "getvars"]
TT_GETCWD = ["GETCWD", "getcwd"]
TT_VAR = ["$"]
TT_COMMENT = "~~"
DIGITS = list("0123456789.")
MATH_CHARS = list("+-/*()%")

symbols = {
    "$_VERSION" : __version__,
    "$_CWD": os.getcwd(),
    "$_LAST_IF": 0
}

subs = {

}

class Err:
    def __init__(self, name, details):
        self.details = details
        self.name = name
    
    def do(self):
        print(self.name, ":", self.details)
        quit()



from sys import argv

def open_file(filename):
    data = open(filename, "r").read()
    data += "\n"
    return data

def lex(filecontent):
    tok = ""
    var_started = 0
    in_comment = 0
    comment = ""
    varname = ""
    expr_started = 0 # 0 --> Not in a number | 1 --> In a number
    expr = ""
    isexpr = 0
    state = 0 # 0 -- > Not in a string | 1 --> In a string
    string = ""
    tokens = []
    filecontent = list(filecontent)
    for char in filecontent:
        tok += char
        if tok in " \t" and state == 0 and in_comment == 0: 
            tok = ""
            
        if tok == "\n" and state == 0: 
            if expr != "" and isexpr == 1:
                tokens.append("EXPR:" + expr)
                #print(expr + "EXPR")
                isexpr = 0
                expr = ""
            elif expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                #print(expr + "NUM")
                isexpr = 0
                expr = ""
            elif varname != "":
                tokens.append("VAR:" + varname)
                varname = ""
                var_started = 0
            elif in_comment == 1:
                tokens.append("COMMENT:" + comment)
                in_comment = 0
                comment = ""
            tok = ""
        elif tok == "=" and state == 0 and in_comment == 0:
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            if expr != "" and isexpr == 1:
                tokens.append("EXPR:" + expr)
                expr = ""
            if string != "":
                tokens.append("STRING:" + string)
                expr = ""
            if varname != "": #-
                tokens.append("VAR:" + varname) #-
                varname = "" #-
                var_started = 0
            if tokens[-1] == "EQUALS":
                tokens[-1] = "EQEQ"
            elif tokens[-1] == "BANG":
                tokens[-1] = "BAEQ"
            elif tokens[-1] == "HUNT_RIGHT":
                tokens[-1] = "HREQ"
            elif tokens[-1] == "HUNT_LEFT":
                tokens[-1] = "HLEQ"
            else:
                tokens.append("EQUALS")
            tok = ""
        elif tok == "!" and state == 0 and in_comment == 0:
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            if expr != "" and isexpr == 1:
                tokens.append("EXPR:" + expr)
                expr = ""
            if string != "":
                tokens.append("STRING:" + string)
                expr = ""
            if varname != "": #-
                tokens.append("VAR:" + varname) #-
                varname = "" #-
                var_started = 0
            tokens.append("BANG")
            tok = ""
        elif tok == ">" and state == 0 and in_comment == 0:
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            if expr != "" and isexpr == 1:
                tokens.append("EXPR:" + expr)
                expr = ""
            if string != "":
                tokens.append("STRING:" + string)
                expr = ""
            if varname != "": #-
                tokens.append("VAR:" + varname) #-
                varname = "" #-
                var_started = 0
            tokens.append("HUNT_RIGHT")
            tok = ""
        elif tok == "<" and state == 0 and in_comment == 0:
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            if expr != "" and isexpr == 1:
                tokens.append("EXPR:" + expr)
                expr = ""
            if string != "":
                tokens.append("STRING:" + string)
                expr = ""
            if varname != "": #-
                tokens.append("VAR:" + varname) #-
                varname = "" #-
                var_started = 0
            tokens.append("HUNT_LEFT")
            tok = ""
        elif tok in TT_VAR and state == 0 and in_comment == 0:
            var_started = 1
            varname += tok
            tok = ""
        elif var_started == 1:
            varname += tok
            tok = ""
        elif tok in TT_PRINTSTR:
            tokens.append("PRINT_STR")
            tok = ""
        elif tok in TT_PRINT:
            tokens.append("PRINT")
            tok = ""
        elif tok in TT_NLNPRINT:
            tokens.append("NLN_PRINT")
            tok = ""
        elif tok in TT_NEXT:
            tokens.append("NEXT")
            tok = ""
        elif tok in TT_PREV:
            tokens.append("PREV")
            tok = ""
        elif tok in TT_EXE:
            tokens.append("EXE")
            tok = ""
        elif tok in TT_EVAL:
            tokens.append("EVAL")
            tok = ""
        elif tok in TT_SUB:
            tokens.append("SUB")
            tok = ""
        elif tok in TT_ENDSUB:
            tokens.append("ENDSUB")
            tok = ""
        elif tok in TT_GOTO:
            tokens.append("GOTO")
            tok = ""
        elif tok in TT_SLEEP:
            tokens.append("SLEEP")
            tok = ""
        elif tok in TT_INPUT:
            tokens.append("INPUT")
            tok = ""
        elif tok in TT_NUMPUT:
            tokens.append("NUMPUT")
            tok = ""
        elif tok in TT_GETCWD:
            tokens.append("GETCWD")
            tok = ""
        elif tok in TT_QUIT:
            tokens.append("QUIT")
            tok = ""
        elif tok in TT_CLEAR:
            tokens.append("CLEAR")
            tok = ""
        elif tok in TT_GETVARS:
            tokens.append("GETVARS")
            tok = ""
        elif tok in TT_CMD:
            tokens.append("CMD")
            tok = ""
        elif tok in TT_IF:
            tokens.append("IF")
            tok = ""
        elif tok in TT_ELSE:
            tokens.append("ENDIF")
            tokens.append("IF")
            tokens.append("VAR:$_LAST_IF")
            tokens.append("EQEQ")
            tokens.append("NUM:0")
            tokens.append("THEN")
            tok = ""
        elif tok in TT_DEL:
            tokens.append("DEL")
            tok = ""
        elif tok in TT_THEN:
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            if expr != "" and isexpr == 1:
                tokens.append("EXPR:" + expr)
                expr = ""
            if string != "":
                tokens.append("STRING:" + string)
                string = ""
            if varname != "":
                tokens.append("VAR:" + varname)
                varname = ""
                var_started = 0
            #input("h")
            tokens.append("THEN")
            tok = ""
        elif tok in TT_ENDIF:
            tokens.append("ENDIF")
            tok = ""
        elif tok == TT_COMMENT and in_comment == 0 and state == 0:
            in_comment = 1
            comment = ""
            tok = ""
        elif in_comment == 1:
            comment += tok
            tok = ""
        elif tok in DIGITS and state == 0:  
            expr_started = 1
            expr += tok
            tok = ""
        elif tok in MATH_CHARS and state == 0:
            expr += tok
            isexpr = 1
            tok = ""
        elif tok == "\"":
            if state == 0:
                state = 1
            elif state == 1:
                tokens.append("STRING:" + string + "\"")
                string = ""
                state = 0
                tok = ""
        elif state == 1:
            string += tok
            tok = ""
    print(tokens)
    #return ""
    return tokens

def parse(toks):
    i = 0
    in_false_if = 0
    in_sub = 0
    csn = "" # Current Sub Name
    while (i < len(toks)):
        #print(i, ":", toks[i])
        if toks[i] == "ENDSUB":
            in_sub = 0
            csn = ""
            i+=1
        elif in_sub == 1:
            subs[csn].append(toks[i])
            i+=1
        elif toks[i] == "ENDIF":
            in_false_if = 0
            i+=1
        elif in_false_if == 1:
            i+=1
        elif toks[i] == "QUIT":
            quit()
            break
            
        
        elif toks[i] == "CLEAR":
            os.system('cls' if os.name == 'nt' else 'clear')
            i += 1
        
        elif toks[i].startswith("NUM") and toks[i] != "NUMPUT" or toks[i].startswith("EXPR"):
            i += 1
        
        elif toks[i].startswith("COMMENT"):
            i+=1
        
        elif toks[i] == "GETVARS":
            print(symbols)
            i+=1
        
        elif toks[i] == "GETCWD":
            symbols["$_CWD"] = os.getcwd()
            i+=1

        else:
        
            try:
                
                
                if toks[i] + " " + toks[i+1][0:6] == "PRINT STRING":
                    print(toks[i+1][8:len(toks[i+1])-1])
                    #print(toks[i+1][7:])
                    i+=2

                elif toks[i] + " " + toks[i+1][0:3] == "PRINT NUM":
                    print(eval(toks[i+1][4:]))
                    i+=2
                
                elif toks[i] + " " + toks[i+1][0:3] == "PRINT VAR":
                    try:
                        print(symbols[toks[i+1][4:]])
                        i+=2
                    except KeyError:
                        VarDoesNotExistError = Err("VarDoesNotExistError", "variable '"+ toks[i+1][4:]+ "' does not exist")
                        VarDoesNotExistError.do()
                    
                
                elif toks[i] + " " + toks[i+1][0:4] == "PRINT EXPR":
                    print(eval(toks[i+1][5:]))
                    i+=2
                
                elif toks[i] + " " + toks[i+1][0:6] == "NLN_PRINT STRING":
                    print(toks[i+1][8:len(toks[i+1])-1], end=" ")
                    #print(toks[i+1][7:])
                    i+=2

                elif toks[i] + " " + toks[i+1][0:3] == "NLN_PRINT NUM":
                    print(eval(toks[i+1][4:]), end=" ")
                    i+=2
                
                elif toks[i] + " " + toks[i+1][0:3] == "NLN_PRINT VAR":
                    try:
                        print(symbols[toks[i+1][4:]], end=" ")
                        i+=2
                    except KeyError:
                        VarDoesNotExistError = Err("VarDoesNotExistError", "variable '"+ toks[i+1][4:]+ "' does not exist")
                        VarDoesNotExistError.do()
                    
                
                elif toks[i] + " " + toks[i+1][0:4] == "NLN_PRINT EXPR":
                    print(eval(toks[i+1][5:]), end=" ")
                    i+=2
                
                elif toks[i] + " " + toks[i+1][0:3] == "PRINT_STR NUM":
                    print(toks[i+1][4:])
                    i+=2
                
                elif toks[i] + " " + toks[i+1][0:4] == "PRINT_STR EXPR":
                    print(toks[i+1][5:])
                    i+=2
                
                elif toks[i] + " " + toks[i+1][0:6] == "PRINT_STR STRING":
                    print(toks[i+1][8:len(toks[i+1])-1])
                    #print(toks[i+1][7:])
                    i+=2
                
                elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:6] == "VAR EQUALS STRING":
                    symbols[toks[i][4:]] = toks[i+2][8:len(toks[i+2])-1]
                    #print(symbols[toks[i][4:]])
                    i+=3
                
                elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS VAR":
                    symbols[toks[i][4:]] = symbols[toks[i+2][4:]]
                    #print(symbols[toks[i][4:]])
                    i+=3

                elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS NUM":
                    number = toks[i+2][4:]
                    if "." in number:
                        symbols[toks[i][4:]] = float(number)
                    else:
                        symbols[toks[i][4:]] = int(number)    
                    #print(symbols[toks[i][4:]])
                    i+=3
                
                elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:4] == "VAR EQUALS EXPR":
                    ex = eval(toks[i+2][5:])
                    if "." in str(ex):
                        symbols[toks[i][4:]] = float(ex)
                    else:
                        symbols[toks[i][4:]] = int(ex)    
                    #print(symbols[toks[i][4:]])
                    i+=3
                
                elif toks[i] + " " + toks[i+1][0:6] == "CMD STRING":
                    os.system(toks[i+1][8:len(toks[i+1])-1])
                    i+=2
                
                elif toks[i] + " " + toks[i+1][0:3] == "CMD VAR":
                    try:
                        os.system(symbols[toks[i+1][4:]])
                        i+=2
                    except KeyError:
                        VarDoesNotExistError = Err("VarDoesNotExistError", "variable '"+ toks[i+1][4:]+ "' does not exist")
                        VarDoesNotExistError.do()

                elif toks[i] + " " + toks[i+1][0:3] == "NEXT VAR":
                    try:
                        symbols[toks[i+1][4:]] += 1
                        print(symbols[toks[i+1][4:]])
                        i+=2
                    except KeyError:
                        VarDoesNotExistError = Err("VarDoesNotExistError", "variable '"+ toks[i+1][4:]+ "' does not exist")
                        VarDoesNotExistError.do()
                    except:
                        VarIsNotANumError = Err("VarIsNotANumberError", "variable '" + toks[i+1][4:] + "' is not a NUM")
                        VarIsNotANumError.do()
                    

                elif toks[i] + " " + toks[i+1][0:3] == "PREV VAR":
                    try:
                        symbols[toks[i+1][4:]] -= 1
                        print(symbols[toks[i+1][4:]])
                        i+=2
                    except KeyError:
                        VarDoesNotExistError = Err("VarDoesNotExistError", "variable '"+ toks[i+1][4:]+ "' does not exist")
                        VarDoesNotExistError.do()
                    except:
                        VarIsNotANumError = Err("VarIsNotANumberError", "variable '" + toks[i+1][4:] + "' is not a NUM")
                        VarIsNotANumError.do()

                elif toks[i] + " " + toks[i+1][0:6] == "EXE STRING":
                    fn = toks[i+1][8:len(toks[i+1])-1]
                    try:
                        fn_data = open_file(fn)
                        fn_toks = lex(fn_data)
                        parse(fn_toks)
                        i+=2
                    except FileNotFoundError:
                        FileDoesNotExistError = Err("FileDoesNotExistError", "file '"+fn+"' does not exist in " + os.getcwd())
                        FileDoesNotExistError.do()
                    except:
                        int("44")
                        fn_data = open_file(fn)
                        fn_toks = lex(fn_data)
                        parse(fn_toks)
                        i+=2
                
                elif toks[i] + " " + toks[i+1][0:3] == "EXE VAR":
                    try:
                        fn = symbols[toks[i+1][4:]]
                        fn_data = open_file(fn)
                        fn_toks = lex(fn_data)
                        parse(fn_toks)
                        i+=2
                    except KeyError:
                        VarDoesNotExistError = Err("VarDoesNotExistError", "variable '"+ toks[i+1][4:]+ "' does not exist")
                        VarDoesNotExistError.do()
                    except FileNotFoundError:
                        FileDoesNotExistError = Err("FileDoesNotExistError", "file '"+fn+"' does not exist in " + os.getcwd())
                        FileDoesNotExistError.do()
                    
                    except:
                        int("44")
                        fn_data = open_file(fn)
                        fn_toks = lex(fn_data)
                        parse(fn_toks)
                        i+=2

                elif toks[i] + " " + toks[i+1][0:6] == "EVAL STRING":
                    code = toks[i+1][8:len(toks[i+1])-1]
                    code = code + "\n"
                    code_toks = lex(code)
                    parse(code_toks)
                    i+=2
                
                elif toks[i] + " " + toks[i+1][0:3] == "EVAL VAR":
                    try:
                        code = symbols[toks[i+1][4:]]
                        code = code + "\n"
                        code_toks = lex(code)
                        parse(code_toks)
                        i+=2
                    except KeyError:
                        VarDoesNotExistError = Err("VarDoesNotExistError", "variable '"+ toks[i+1][4:]+ "' does not exist")
                        VarDoesNotExistError.do()
                    
                elif toks[i] + " " + toks[i+1][0:3] == "SLEEP NUM":
                    num = float(toks[i+1][4:])
                    import time
                    time.sleep(num)
                    i+=2
                elif toks[i] + " " + toks[i+1][0:3] == "SLEEP VAR":
                    try:
                        num = float(symbols[toks[i+1][4:]])
                        import time
                        time.sleep(num)
                        i+=2
                    except KeyError:
                        VarDoesNotExistError = Err("VarDoesNotExistError", "variable '"+ toks[i+1][4:]+ "' does not exist")
                        VarDoesNotExistError.do()
                
                elif toks[i] + " " + toks[i+1][0:3] == "INPUT VAR":
                    var  = toks[i+1][4:]
                    symbols[var] = input("")
                    i+=2
            
                elif toks[i] + " " + toks[i+1][0:3] == "NUMPUT VAR":
                    var  = toks[i+1][4:]
                    inp = input("")
                    if "." in inp:
                        symbols[var] = float(inp)
                    else:
                        symbols[var] = int(inp)
                    i+=2
                
                elif toks[i] + " " + toks[i+1][0:3] == "DEL VAR":
                    var = toks[i+1][4:]
                    del symbols[var]
                    i+=2
                
                elif toks[i] == "IF":
                    #input(toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3] + " " + toks[i+4])
                    min_cond = toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3] + " " + toks[i+4]
                    full_cond = toks[i] + " " + toks[i+1] + " " + toks[i+2] + " " + toks[i+3] + " " + toks[i+4]
                    op = toks[i+2]
                    #EQEQ == 
                    #BAEQ !=
                    #HLEQ <=
                    #HREQ >=
                    if op == "EQEQ":
                        if min_cond == "IF NUM EQEQ NUM THEN":
                            if float(toks[i+1][4:]) == float(toks[i+3][4:]):
                                #print("True")
                                symbols["$_LAST_IF"] = 1
                                in_false_if = 0
                                i+=5
                            else:
                                #print("False")
                                symbols["$_LAST_IF"] = 0
                                in_false_if = 1
                                i+=1
                        elif min_cond == "IF NUM EQEQ VAR THEN":
                            if float(toks[i+1][4:]) == symbols[toks[i+3][4:]]:
                                #print("True")
                                symbols["$_LAST_IF"] = 1
                                in_false_if = 0
                                i+=5
                            else:
                                #print("False")
                                symbols["$_LAST_IF"] = 0
                                in_false_if = 1
                                i+=1
                        elif min_cond == "IF VAR EQEQ NUM THEN":
                            if float(toks[i+3][4:]) == symbols[toks[i+1][4:]]:
                                #print("True")
                                symbols["$_LAST_IF"] = 1
                                in_false_if = 0
                                i+=5
                            else:
                                #print("False")
                                symbols["$_LAST_IF"] = 0
                                in_false_if = 1
                                i+=1
                        elif min_cond == "IF VAR EQEQ VAR THEN":
                            print("Urde'eeeeee")
                        elif min_cond == "IF NUM EQEQ EXP THEN":
                            input("TROLOLOL")
                            break
                        elif min_cond == "IF EXP EQEQ NUM THEN":
                            pass
                        elif min_cond == "IF EXP EQEQ EXP THEN":
                            pass
                
                
                elif toks[i] + " " + toks[i+1][0:6] == "SUB STRING":
                    in_sub = 1
                    csn = toks[i+1][8:len(toks[i+1])-1]
                    subs[csn] = []
                    i+=2
                
                elif toks[i] + " " + toks[i+1][0:6] == "GOTO STRING":
                    try:
                        parse(subs[toks[i+1][8:len(toks[i+1])-1]])
                        i+=2
                    except KeyError:
                        SubProcessDoesNotExistError = Err("SubProcessDoesNotExistError", "SubProcess '" + toks[i+1][8:len(toks[i+1])-1] + "' Does Not Exist.")
                        SubProcessDoesNotExistError.do()
                        break
                    



                else:
                    print("SYNTAX ERROR")
                    i+=1

            except IndexError:
                print("SYNTAX ERROR")
                i+=1
        
            
def run():

    try:
        data = open_file(argv[1])
    except IndexError:
        
        shell.sh()

    toks = lex(data)
    parse(toks)

run()