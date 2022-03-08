#   Author: Jaroslav Kvasnička
#   Login:  xkvan14
#   IPP     Interpret

import os
import sys
import re
import xml.etree.ElementTree as ET
import getopt
import string

def xmlFunc(root):

    # Kontrola hlavičky programu
    try:
        if (root.tag != "program"):
            exit(32)
        # if(len(root.attrib) != 1):
        #    exit(32)
        if (root.attrib["language"] != "IPPcode21"):
            exit(32)
    except:
        exit(32)

    # Parsování Instrukcí
    for child in root:
        # Univerzální tabulka pro instrukce s argumenty
        table = [0, "", "", "", "", "", "", ""]
        arg1 = False
        arg2 = False
        arg3 = False
        try:
            if (len(child.attrib) != 2):
                exit(32)
            if (child.tag != "instruction"):
                exit(32)
            if (not child.attrib["opcode"]):
                exit(32)
            if (not child.attrib["order"]):
                exit(32)
        except:
            exit(32)

        # Kontrola jestli order je: číslo, je větší než 0, není záporné
        try:
            tmp = int(child.attrib["order"])
        except:
            exit(32)
        if(tmp < 1):
            exit(32)
        if (tmp in orderCheckTable):
            exit(32)
        else:
            orderCheckTable.append(tmp)

        # Přiřazování hodnot do celkové tabulky ve tvaru [[order, opcode, arg1.type, arg1.val. arg2.type, arg2.val, arg3.type, arg3.val], [atd...]...]
        try:
            table[0] = int(child.attrib["order"])
            table[1] = (child.attrib["opcode"]).upper()
        except:
            exit(32)

        # Parsování arg v Instrukcích
        for arg in child:
            # Kontrola jednoho atributu "type"
            if (len(arg.attrib) != 1):
                exit(32)
            # Kontrola typu int,string....
            if (arg.attrib["type"] != "int" and arg.attrib["type"] != "bool" and arg.attrib["type"] != "string" and
                    arg.attrib["type"] != "nil" and arg.attrib["type"] != "var" and arg.attrib["type"] != "type" and
                    arg.attrib["type"] != "label"):
                exit(32)

            # Přiřazování hodnot do celkové tabulky ve tvaru [[order, opcode, arg1.type, arg1.val. arg2.type, arg2.val, arg3.type, arg3.val], [atd...]...]
            if (arg.tag == "arg1"):
                # Kontrola více než 1 arg1
                if (arg1 != True):
                    arg1 = True
                else:
                    exit(32)
                table[2] = arg.attrib["type"]
                table[3] = arg.text
            if (arg.tag == "arg2"):
                # Kontrola více než 1 arg2
                if (arg2 != True):
                    arg2 = True
                else:
                    exit(32)
                table[4] = arg.attrib["type"]
                table[5] = arg.text
            if (arg.tag == "arg3"):
                # Kontrola více než 1 arg3
                if (arg3 != True):
                    arg3 = True
                else:
                    exit(32)
                table[6] = arg.attrib["type"]
                table[7] = arg.text

        # Zápis celé instrukce s argumenty do Univerzální tabulky
        UniTable.append(table)
    UniTable.sort(key=lambda x: x[0])

    # Přečíslování order na 1,2,3,4,5,6...
    order = 1
    for item in UniTable:
        item[0] = order
        order = order + 1

    return UniTable

def instrCheck(UniTable):
    for instruction in UniTable:
        # Kontrola Správnosti Instrukcí
        if (instruction[1] == "MOVE"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] != "" and instruction[5] != "" and instruction[6] == "" and instruction[7] == ""):
                exit(32)
        elif (instruction[1] == "INT2CHAR"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] != "" and instruction[5] != "" and instruction[6] == "" and instruction[7] == ""):
                exit(32)
        elif (instruction[1] == "NOT"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] != "" and instruction[5] != "" and instruction[6] == "" and instruction[7] == ""):
                exit(32)
        elif (instruction[1] == "STRLEN"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] != "" and instruction[5] != "" and instruction[6] == "" and instruction[7] == ""):
                exit(32)
        elif (instruction[1] == "TYPE"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] != "" and instruction[5] != "" and instruction[6] == "" and instruction[7] == ""):
                exit(32)
        elif (instruction[1] == "DEFVAR"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] == "" and instruction[5] == "" and instruction[6] == "" and instruction[7] == ""):
                exit(32)
        elif (instruction[1] == "POPS"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] == "" and instruction[5] == "" and instruction[6] == "" and instruction[7] == ""):
                exit(32)
        elif (instruction[1] == "CREATEFRAME"):
            if not (instruction[2] == "" and instruction[3] == "" and instruction[4] == "" and instruction[5] == "" and instruction[6] == "" and instruction[7] == ""):
                exit(32)
        elif (instruction[1] == "PUSHFRAME"):
            if not (instruction[2] == "" and instruction[3] == "" and instruction[4] == "" and instruction[5] == "" and instruction[6] == "" and instruction[7] == ""):
                exit(32)
        elif (instruction[1] == "POPFRAME"):
            if not (instruction[2] == "" and instruction[3] == "" and instruction[4] == "" and instruction[5] == "" and instruction[6] == "" and instruction[7] == ""):
                exit(32)
        elif (instruction[1] == "RETURN"):
            if not (instruction[2] == "" and instruction[3] == "" and instruction[4] == "" and instruction[5] == "" and instruction[6] == "" and instruction[7] == ""):
                exit(32)
        elif (instruction[1] == "BREAK"):
            if not (instruction[2] == "" and instruction[3] == "" and instruction[4] == "" and instruction[5] == "" and instruction[6] == "" and instruction[7] == ""):
                exit(32)
        elif (instruction[1] == "CALL"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] == "" and instruction[5] == "" and instruction[6] == "" and instruction[7] == ""):
                exit(32)
        elif (instruction[1] == "LABEL"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] == "" and instruction[5] == "" and instruction[6] == "" and instruction[7] == ""):
                exit(32)
        elif (instruction[1] == "JUMP"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] == "" and instruction[5] == "" and instruction[6] == "" and instruction[7] == ""):
                exit(32)
        elif (instruction[1] == "JUMPIFEQ"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] != "" and instruction[5] != "" and instruction[6] != "" and instruction[7] != ""):
                exit(32)
        elif (instruction[1] == "JUMPIFNEQ"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] != "" and instruction[5] != "" and instruction[6] != "" and instruction[7] != ""):
                exit(32)
        elif (instruction[1] == "ADD"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] != "" and instruction[5] != "" and instruction[6] != "" and instruction[7] != ""):
                exit(32)
        elif (instruction[1] == "SUB"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] != "" and instruction[5] != "" and instruction[6] != "" and instruction[7] != ""):
                exit(32)
        elif (instruction[1] == "MUL"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] != "" and instruction[5] != "" and instruction[6] != "" and instruction[7] != ""):
                exit(32)
        elif (instruction[1] == "IDIV"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] != "" and instruction[5] != "" and instruction[6] != "" and instruction[7] != ""):
                exit(32)
        elif (instruction[1] == "LT"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] != "" and instruction[5] != "" and instruction[6] != "" and instruction[7] != ""):
                exit(32)
        elif (instruction[1] == "GT"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] != "" and instruction[5] != "" and instruction[6] != "" and instruction[7] != ""):
                exit(32)
        elif (instruction[1] == "EQ"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] != "" and instruction[5] != "" and instruction[6] != "" and instruction[7] != ""):
                exit(32)
        elif (instruction[1] == "AND"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] != "" and instruction[5] != "" and instruction[6] != "" and instruction[7] != ""):
                exit(32)
        elif (instruction[1] == "OR"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] != "" and instruction[5] != "" and instruction[6] != "" and instruction[7] != ""):
                exit(32)
        elif (instruction[1] == "STRI2INT"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] != "" and instruction[5] != "" and instruction[6] != "" and instruction[7] != ""):
                exit(32)
        elif (instruction[1] == "CONCAT"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] != "" and instruction[5] != "" and instruction[6] != "" and instruction[7] != ""):
                exit(32)
        elif (instruction[1] == "GETCHAR"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] != "" and instruction[5] != "" and instruction[6] != "" and instruction[7] != ""):
                exit(32)
        elif (instruction[1] == "SETCHAR"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] != "" and instruction[5] != "" and instruction[6] != "" and instruction[7] != ""):
                exit(32)
        elif (instruction[1] == "PUSHS"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] == "" and instruction[5] == "" and instruction[6] == "" and instruction[7] == ""):
                exit(32)
        elif (instruction[1] == "WRITE"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] == "" and instruction[5] == "" and instruction[6] == "" and instruction[7] == ""):
                exit(32)
        elif (instruction[1] == "DPRINT"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] == "" and instruction[5] == "" and instruction[6] == "" and instruction[7] == ""):
                exit(32)
        elif (instruction[1] == "EXIT"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] == "" and instruction[5] == "" and instruction[6] == "" and instruction[7] == ""):
                exit(32)
        elif (instruction[1] == "READ"):
            if not (instruction[2] != "" and instruction[3] != "" and instruction[4] != "" and instruction[5] != "" and instruction[6] == "" and instruction[7] == ""):
                exit(32)
        else:
            exit(32)

def getVar(FRAME,VARNAME):
    VALUE = None
    if (FRAME == "GF"):
        if (VARNAME in GF_Frame):
            VALUE = GF_Frame[VARNAME]
        else:
            exit(54)
    elif (FRAME == "LF"):
        if (VARNAME in (LF_Frame[len(LF_Frame) - 1])):
            VALUE = LF_Frame[len(LF_Frame) - 1][VARNAME]
        else:
            exit(54)
    elif (FRAME == "TF"):
        if (TF_Existion == True):
            if (VARNAME in TF_Frame):
                VALUE = TF_Frame[VARNAME]
            else:
                exit(54)
        else:
            exit(55)
    return VALUE

def setVar(FRAME,VARNAME,VALUE):
    if (FRAME == "GF"):
        if (VARNAME in GF_Frame):
            GF_Frame[VARNAME] = VALUE
        else:
            exit(54)
    elif (FRAME == "LF"):
        if (VARNAME in (LF_Frame[len(LF_Frame) - 1])):
            LF_Frame[len(LF_Frame) - 1][VARNAME] = VALUE
        else:
            exit(54)
    elif (FRAME == "TF"):
        if (TF_Existion == True):
            if (VARNAME in TF_Frame):
                TF_Frame[VARNAME] = VALUE
            else:
                exit(54)
        else:
            exit(55)


def Interpretation(GF_Frame, LF_Frame, TF_Frame, TF_Existion, Stack, Label_Stack, Label_Call_Stack, Label_Jump):
    i = 0

    for Instruction in UniTable:
        if(i < Label_Jump):
            i = i + 1
            continue
        ##########################################################################
        # MOVE var var/val
        if (Instruction[1] == "MOVE"):
            VALUE = None
            FRAME = None
            VARNAME = None

            if (Instruction[2] != "var"):
                exit(32)

            if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "GF"
                VARNAME = re.sub(r'GF@', "", Instruction[3])
            elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "LF"
                VARNAME = re.sub(r'LF@', "", Instruction[3])
            elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "TF"
                VARNAME = re.sub(r'TF@', "", Instruction[3])
            else:
                exit(32)

            if (Instruction[4] != "int" and Instruction[4] != "bool" and Instruction[4] != "string" and Instruction[
                4] != "nil" and Instruction[4] != "var"):
                exit(32)
            if (Instruction[4] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'GF@', "", Instruction[5])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'LF@', "", Instruction[5])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'TF@', "", Instruction[5])
                    VALUE = getVar("TF", varName)
            elif (Instruction[4] == "string"):
                VALUE = ["string", Instruction[5]]
            elif (Instruction[4] == "int"):
                try:
                    VALUE = ["int", int(Instruction[5])]
                except:
                    exit(57)
            elif (Instruction[4] == "bool"):
                VALUE = ["bool", Instruction[5]]
                if (VALUE[1] != "true" and VALUE[1] != "false"):
                    exit(57)
            elif (Instruction[4] == "nil"):
                VALUE = ["nil", Instruction[5]]
                if (VALUE[1] != "nil"):
                    exit(57)

            setVar(FRAME, VARNAME, VALUE)
        ##########################################################################
        # INT2CHAR
        elif (Instruction[1] == "INT2CHAR"):
            VALUE = None
            FRAME = None
            VARNAME = None
            if (Instruction[2] != "var"):
                exit(32)

            if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "GF"
                VARNAME = re.sub(r'GF@', "", Instruction[3])
            elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "LF"
                VARNAME = re.sub(r'LF@', "", Instruction[3])
            elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "TF"
                VARNAME = re.sub(r'TF@', "", Instruction[3])
            else:
                exit(32)

            if (Instruction[4] != "int" and Instruction[4] != "bool" and Instruction[4] != "string" and Instruction[
                4] != "nil" and Instruction[4] != "var"):
                exit(32)
            if (Instruction[4] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'GF@', "", Instruction[5])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'LF@', "", Instruction[5])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'TF@', "", Instruction[5])
                    VALUE = getVar("TF", varName)
            elif (Instruction[4] == "int"):
                VALUE = ["int", Instruction[5]]
            else:
                exit(53)

            try:
                VALUE[1] = chr(int(VALUE[1]))
            except:

                exit(58)
            setVar(FRAME, VARNAME, VALUE)
        ##########################################################################
        # NOT
        elif (Instruction[1] == "NOT"):
            VALUE = None
            FRAME = None
            VARNAME = None
            if (Instruction[2] != "var"):
                exit(32)

            if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "GF"
                VARNAME = re.sub(r'GF@', "", Instruction[3])
            elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "LF"
                VARNAME = re.sub(r'LF@', "", Instruction[3])
            elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "TF"
                VARNAME = re.sub(r'TF@', "", Instruction[3])
            else:
                exit(32)

            if (Instruction[4] != "int" and Instruction[4] != "bool" and Instruction[4] != "string" and Instruction[
                4] != "nil" and Instruction[4] != "var"):
                exit(32)
            if (Instruction[4] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'GF@', "", Instruction[5])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'LF@', "", Instruction[5])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'TF@', "", Instruction[5])
                    VALUE = getVar("TF", varName)
            elif (Instruction[4] == "bool"):
                VALUE = ["bool", Instruction[5]]
            else:
                exit(53)

            if (VALUE[1] == "true"):
                VALUE[1] = "false"
            elif (VALUE[1] == "false"):
                VALUE[1] = "true"
            else:
                exit(57)
            setVar(FRAME, VARNAME, VALUE)
        ##########################################################################
        # STRLEN
        elif (Instruction[1] == "STRLEN"):
            VALUE = None
            FRAME = None
            VARNAME = None
            if (Instruction[2] != "var"):
                exit(32)

            if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "GF"
                VARNAME = re.sub(r'GF@', "", Instruction[3])
            elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "LF"
                VARNAME = re.sub(r'LF@', "", Instruction[3])
            elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "TF"
                VARNAME = re.sub(r'TF@', "", Instruction[3])
            else:
                exit(32)

            if (Instruction[4] != "int" and Instruction[4] != "bool" and Instruction[4] != "string" and Instruction[
                4] != "nil" and Instruction[4] != "var"):
                exit(32)
            if (Instruction[4] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'GF@', "", Instruction[5])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'LF@', "", Instruction[5])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'TF@', "", Instruction[5])
                    VALUE = getVar("TF", varName)
            elif (Instruction[4] == "string"):
                VALUE = ["string", Instruction[5]]
            else:
                exit(53)
            if (VALUE[0] != "string"):
                exit(53)

            setVar(FRAME, VARNAME, ["int", len(VALUE[1])])
        ##########################################################################
        # TYPE
        elif (Instruction[1] == "TYPE"):
            VALUE = None
            FRAME = None
            VARNAME = None
            if (Instruction[2] != "var"):
                exit(32)

            if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "GF"
                VARNAME = re.sub(r'GF@', "", Instruction[3])
            elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "LF"
                VARNAME = re.sub(r'LF@', "", Instruction[3])
            elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "TF"
                VARNAME = re.sub(r'TF@', "", Instruction[3])
            else:
                exit(32)

            if (Instruction[4] != "int" and Instruction[4] != "bool" and Instruction[4] != "string" and Instruction[
                4] != "nil" and Instruction[4] != "var"):
                exit(32)
            if (Instruction[4] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'GF@', "", Instruction[5])
                    if (varName in GF_Frame):
                        VALUE = GF_Frame[varName]
                    else:
                        VALUE = ["", ""]

                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'LF@', "", Instruction[5])
                    if (varName in (LF_Frame[len(LF_Frame) - 1])):
                        VALUE = LF_Frame[len(LF_Frame) - 1][varName]
                    else:
                        VALUE = ["", ""]

                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'TF@', "", Instruction[5])
                    if (TF_Existion == True):
                        if (varName in TF_Frame):
                            VALUE = TF_Frame[varName]
                        else:
                            VALUE = ["", ""]
                    else:
                        exit(55)

            elif (Instruction[4] == "string"):
                VALUE = ["string", Instruction[5]]
            elif (Instruction[4] == "int"):
                VALUE = ["int", Instruction[5]]
            elif (Instruction[4] == "bool"):
                VALUE = ["bool", Instruction[5]]
            elif (Instruction[4] == "nil"):
                VALUE = ["nil", Instruction[5]]

            setVar(FRAME, VARNAME, ["string", VALUE[0]])
        ##########################################################################
        # DEFVAR var
        elif (Instruction[1] == "DEFVAR"):
            varName = ""

            if (Instruction[2] != "var"):
                exit(32)

            if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                varName = re.sub(r'GF@', "", Instruction[3])
                if (varName in GF_Frame):
                    exit(52)
                GF_Frame[varName] = ["",""]

            elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                varName = re.sub(r'LF@', "", Instruction[3])
                if (len(LF_Frame) == 0):
                    exit(55)
                if (varName in (LF_Frame[len(LF_Frame) - 1])):
                    exit(52)
                LF_Frame[len(LF_Frame) - 1][varName] = ["",""]

            elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                varName = re.sub(r'TF@', "", Instruction[3])
                if (TF_Existion == False):
                    exit(55)
                TF_Frame[varName] = ["",""]
            else:
                exit(32)
        ##########################################################################
        # POPS
        elif (Instruction[1] == "POPS"):
            VALUE = None
            FRAME = None
            VARNAME = None
            if (Instruction[2] != "var"):
                exit(32)

            if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "GF"
                VARNAME = re.sub(r'GF@', "", Instruction[3])
            elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "LF"
                VARNAME = re.sub(r'LF@', "", Instruction[3])
            elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "TF"
                VARNAME = re.sub(r'TF@', "", Instruction[3])
            else:
                exit(32)

            setVar(FRAME, VARNAME, Stack.pop())
        ##########################################################################
        # PUSHS
        elif (Instruction[1] == "PUSHS"):
            VALUE = None
            if (Instruction[2] != "int" and Instruction[2] != "bool" and Instruction[2] != "string" and Instruction[
                2] != "nil" and Instruction[2] != "var"):
                exit(32)

            if (Instruction[2] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                    varName = re.sub(r'GF@', "", Instruction[3])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                    varName = re.sub(r'LF@', "", Instruction[3])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                    varName = re.sub(r'TF@', "", Instruction[3])
                    VALUE = getVar("TF", varName)
            elif (Instruction[2] == "string"):
                VALUE = ["string", Instruction[3]]
            elif (Instruction[2] == "int"):
                VALUE = ["int", Instruction[3]]
            elif (Instruction[2] == "bool"):
                VALUE = ["bool", Instruction[3]]
            elif (Instruction[2] == "nil"):
                VALUE = ["nil", Instruction[3]]
            Stack.append(VALUE)
        ##########################################################################
        # CREATEFRAME --
        elif (Instruction[1] == "CREATEFRAME"):
            TF_Existion = True
            TF_Frame = dict()
        ##########################################################################
        # PUSHFRAME --
        elif (Instruction[1] == "PUSHFRAME"):
            if (TF_Existion != True):
                exit(55)
            LF_Frame.append(TF_Frame.copy())
            TF_Existion = False
        ##########################################################################
        # POPFRAME --
        elif (Instruction[1] == "POPFRAME"):
            try:
                TF_Frame = LF_Frame.pop()
                TF_Existion = True
            except:
                exit(55)
        ##########################################################################
        # ADD
        elif (Instruction[1] == "ADD"):
            VALUE = None
            VALUE1 = None
            FRAME = None
            VARNAME = None
            if (Instruction[2] != "var"):
                exit(32)

            if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "GF"
                VARNAME = re.sub(r'GF@', "", Instruction[3])
            elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "LF"
                VARNAME = re.sub(r'LF@', "", Instruction[3])
            elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "TF"
                VARNAME = re.sub(r'TF@', "", Instruction[3])
            else:
                exit(32)

            if (Instruction[4] != "int" and Instruction[4] != "bool" and Instruction[4] != "string" and Instruction[
                4] != "nil" and Instruction[4] != "var"):
                exit(32)
            if (Instruction[4] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'GF@', "", Instruction[5])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'LF@', "", Instruction[5])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'TF@', "", Instruction[5])
                    VALUE = getVar("TF", varName)
            elif (Instruction[4] == "int"):
                VALUE = ["int", Instruction[5]]
            else:
                exit(53)

            if (Instruction[6] != "int" and Instruction[6] != "bool" and Instruction[6] != "string" and Instruction[
                6] != "nil" and Instruction[6] != "var"):
                exit(32)
            if (Instruction[6] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'GF@', "", Instruction[7])
                    VALUE1 = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'LF@', "", Instruction[7])
                    VALUE1 = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'TF@', "", Instruction[7])
                    VALUE1 = getVar("TF", varName)
            elif (Instruction[6] == "int"):
                VALUE1 = ["int", Instruction[7]]
            else:
                exit(53)

            if (VALUE[0] != "int" or VALUE1[0] != "int"):
                exit(53)
            try:
                VALUE[1] = int(VALUE[1]) + int(VALUE1[1])
            except:
                exit(57)
            setVar(FRAME, VARNAME, ["int", VALUE[1]])
        ##########################################################################
        # SUB
        elif (Instruction[1] == "SUB"):
            VALUE = None
            VALUE1 = None
            FRAME = None
            VARNAME = None
            if (Instruction[2] != "var"):
                exit(32)

            if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "GF"
                VARNAME = re.sub(r'GF@', "", Instruction[3])
            elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "LF"
                VARNAME = re.sub(r'LF@', "", Instruction[3])
            elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "TF"
                VARNAME = re.sub(r'TF@', "", Instruction[3])
            else:
                exit(32)

            if (Instruction[4] != "int" and Instruction[4] != "bool" and Instruction[4] != "string" and Instruction[
                4] != "nil" and Instruction[4] != "var"):
                exit(32)
            if (Instruction[4] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'GF@', "", Instruction[5])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'LF@', "", Instruction[5])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'TF@', "", Instruction[5])
                    VALUE = getVar("TF", varName)
            elif (Instruction[4] == "int"):
                VALUE = ["int", Instruction[5]]
            else:
                exit(53)

            if (Instruction[6] != "int" and Instruction[6] != "bool" and Instruction[6] != "string" and Instruction[
                6] != "nil" and Instruction[6] != "var"):
                exit(32)
            if (Instruction[6] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'GF@', "", Instruction[7])
                    VALUE1 = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'LF@', "", Instruction[7])
                    VALUE1 = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'TF@', "", Instruction[7])
                    VALUE1 = getVar("TF", varName)
            elif (Instruction[6] == "int"):
                VALUE1 = ["int", Instruction[7]]
            else:
                exit(53)

            if (VALUE[0] != "int" or VALUE1[0] != "int"):
                exit(53)
            try:
                VALUE[1] = int(VALUE[1]) - int(VALUE1[1])
            except:
                exit(57)
            setVar(FRAME, VARNAME, ["int", VALUE[1]])
        ##########################################################################
        # MUL
        elif (Instruction[1] == "MUL"):
            VALUE = None
            VALUE1 = None
            FRAME = None
            VARNAME = None
            if (Instruction[2] != "var"):
                exit(32)

            if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "GF"
                VARNAME = re.sub(r'GF@', "", Instruction[3])
            elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "LF"
                VARNAME = re.sub(r'LF@', "", Instruction[3])
            elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "TF"
                VARNAME = re.sub(r'TF@', "", Instruction[3])
            else:
                exit(32)

            if (Instruction[4] != "int" and Instruction[4] != "bool" and Instruction[4] != "string" and Instruction[
                4] != "nil" and Instruction[4] != "var"):
                exit(32)
            if (Instruction[4] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'GF@', "", Instruction[5])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'LF@', "", Instruction[5])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'TF@', "", Instruction[5])
                    VALUE = getVar("TF", varName)
            elif (Instruction[4] == "int"):
                VALUE = ["int", Instruction[5]]
            else:
                exit(53)

            if (Instruction[6] != "int" and Instruction[6] != "bool" and Instruction[6] != "string" and Instruction[
                6] != "nil" and Instruction[6] != "var"):
                exit(32)
            if (Instruction[6] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'GF@', "", Instruction[7])
                    VALUE1 = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'LF@', "", Instruction[7])
                    VALUE1 = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'TF@', "", Instruction[7])
                    VALUE1 = getVar("TF", varName)
            elif (Instruction[6] == "int"):
                VALUE1 = ["int", Instruction[7]]
            else:
                exit(53)

            if (VALUE[0] != "int" or VALUE1[0] != "int"):
                exit(53)
            try:
                VALUE[1] = int(VALUE[1]) * int(VALUE1[1])
            except:
                exit(57)
            setVar(FRAME, VARNAME, ["int", VALUE[1]])
        ##########################################################################
        # IDIV
        elif (Instruction[1] == "IDIV"):
            VALUE = None
            VALUE1 = None
            FRAME = None
            VARNAME = None
            if (Instruction[2] != "var"):
                exit(32)

            if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "GF"
                VARNAME = re.sub(r'GF@', "", Instruction[3])
            elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "LF"
                VARNAME = re.sub(r'LF@', "", Instruction[3])
            elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "TF"
                VARNAME = re.sub(r'TF@', "", Instruction[3])
            else:
                exit(32)

            if (Instruction[4] != "int" and Instruction[4] != "bool" and Instruction[4] != "string" and Instruction[
                4] != "nil" and Instruction[4] != "var"):
                exit(32)
            if (Instruction[4] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'GF@', "", Instruction[5])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'LF@', "", Instruction[5])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'TF@', "", Instruction[5])
                    VALUE = getVar("TF", varName)
            elif (Instruction[4] == "int"):
                VALUE = ["int", Instruction[5]]
            else:
                exit(53)

            if (Instruction[6] != "int" and Instruction[6] != "bool" and Instruction[6] != "string" and Instruction[
                6] != "nil" and Instruction[6] != "var"):
                exit(32)
            if (Instruction[6] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'GF@', "", Instruction[7])
                    VALUE1 = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'LF@', "", Instruction[7])
                    VALUE1 = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'TF@', "", Instruction[7])
                    VALUE1 = getVar("TF", varName)
            elif (Instruction[6] == "int"):
                VALUE1 = ["int", Instruction[7]]
            else:
                exit(53)

            if (VALUE[0] != "int" or VALUE1[0] != "int"):
                exit(53)
            try:
                VALUE[1] = int(VALUE[1]) // int(VALUE1[1])
            except:
                exit(57)
            setVar(FRAME, VARNAME, ["int", VALUE[1]])
        ##########################################################################
        # AND
        elif (Instruction[1] == "AND"):
            VALUE = None
            VALUE1 = None
            FRAME = None
            VARNAME = None
            if (Instruction[2] != "var"):
                exit(32)

            if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "GF"
                VARNAME = re.sub(r'GF@', "", Instruction[3])
            elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "LF"
                VARNAME = re.sub(r'LF@', "", Instruction[3])
            elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "TF"
                VARNAME = re.sub(r'TF@', "", Instruction[3])
            else:
                exit(32)

            if (Instruction[4] != "int" and Instruction[4] != "bool" and Instruction[4] != "string" and Instruction[
                4] != "nil" and Instruction[4] != "var"):
                exit(32)
            if (Instruction[4] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'GF@', "", Instruction[5])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'LF@', "", Instruction[5])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'TF@', "", Instruction[5])
                    VALUE = getVar("TF", varName)
            elif (Instruction[4] == "bool"):
                VALUE = ["bool", Instruction[5]]
            else:
                exit(53)

            if (Instruction[6] != "int" and Instruction[6] != "bool" and Instruction[6] != "string" and Instruction[
                6] != "nil" and Instruction[6] != "var"):
                exit(32)
            if (Instruction[6] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'GF@', "", Instruction[7])
                    VALUE1 = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'LF@', "", Instruction[7])
                    VALUE1 = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'TF@', "", Instruction[7])
                    VALUE1 = getVar("TF", varName)
            elif (Instruction[6] == "bool"):
                VALUE1 = ["bool", Instruction[7]]
            else:
                exit(53)

            if (VALUE[1] != "true" and VALUE[1] != "false" and VALUE1[1] != "true" and VALUE1[1] != "false"):
                exit(57)

            if (VALUE[1] == "true" and VALUE1[1] == "true"):
                VALUEVAR = "true"
            else:
                VALUEVAR = "false"

            setVar(FRAME, VARNAME, ["bool", VALUEVAR])
        ##########################################################################
        # OR
        elif (Instruction[1] == "OR"):
            VALUE = None
            VALUE1 = None
            FRAME = None
            VARNAME = None
            if (Instruction[2] != "var"):
                exit(32)

            if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "GF"
                VARNAME = re.sub(r'GF@', "", Instruction[3])
            elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "LF"
                VARNAME = re.sub(r'LF@', "", Instruction[3])
            elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "TF"
                VARNAME = re.sub(r'TF@', "", Instruction[3])
            else:
                exit(32)

            if (Instruction[4] != "int" and Instruction[4] != "bool" and Instruction[4] != "string" and Instruction[
                4] != "nil" and Instruction[4] != "var"):
                exit(32)
            if (Instruction[4] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'GF@', "", Instruction[5])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'LF@', "", Instruction[5])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'TF@', "", Instruction[5])
                    VALUE = getVar("TF", varName)
            elif (Instruction[4] == "bool"):
                VALUE = ["bool", Instruction[5]]
            else:
                exit(53)

            if (Instruction[6] != "int" and Instruction[6] != "bool" and Instruction[6] != "string" and Instruction[
                6] != "nil" and Instruction[6] != "var"):
                exit(32)
            if (Instruction[6] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'GF@', "", Instruction[7])
                    VALUE1 = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'LF@', "", Instruction[7])
                    VALUE1 = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'TF@', "", Instruction[7])
                    VALUE1 = getVar("TF", varName)
            elif (Instruction[6] == "bool"):
                VALUE1 = ["bool", Instruction[7]]
            else:
                exit(53)

            if (VALUE[1] != "true" and VALUE[1] != "false" and VALUE1[1] != "true" and VALUE1[1] != "false"):
                exit(57)

            if (VALUE[1] == "true" or VALUE1[1] == "true"):
                VALUEVAR = "true"
            else:
                VALUEVAR = "false"

            setVar(FRAME, VARNAME, ["bool", VALUEVAR])
        ##########################################################################
        # LT
        elif (Instruction[1] == "LT"):
            VALUE = None
            VALUE1 = None
            VALUEVAR = None
            FRAME = None
            VARNAME = None
            if (Instruction[2] != "var"):
                exit(32)

            if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "GF"
                VARNAME = re.sub(r'GF@', "", Instruction[3])
            elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "LF"
                VARNAME = re.sub(r'LF@', "", Instruction[3])
            elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "TF"
                VARNAME = re.sub(r'TF@', "", Instruction[3])
            else:
                exit(32)

            if (Instruction[4] != "int" and Instruction[4] != "bool" and Instruction[4] != "string" and Instruction[
                4] != "nil" and Instruction[4] != "var"):
                exit(32)
            if (Instruction[4] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'GF@', "", Instruction[5])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'LF@', "", Instruction[5])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'TF@', "", Instruction[5])
                    VALUE = getVar("TF", varName)
            elif (Instruction[4] == "string"):
                VALUE = ["string", Instruction[5]]
            elif (Instruction[4] == "int"):
                VALUE = ["int", Instruction[5]]
            elif (Instruction[4] == "bool"):
                VALUE = ["bool", Instruction[5]]
            else:
                exit(53)
            if (Instruction[6] != "int" and Instruction[6] != "bool" and Instruction[6] != "string" and Instruction[
                6] != "nil" and Instruction[6] != "var"):
                exit(32)
            if (Instruction[6] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'GF@', "", Instruction[7])
                    VALUE1 = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'LF@', "", Instruction[7])
                    VALUE1 = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'TF@', "", Instruction[7])
                    VALUE1 = getVar("TF", varName)
            elif (Instruction[6] == "string"):
                VALUE1 = ["string", Instruction[7]]
            elif (Instruction[6] == "int"):
                VALUE1 = ["int", Instruction[7]]
            elif (Instruction[6] == "bool"):
                VALUE1 = ["bool", Instruction[7]]
            else:
                exit(53)

            if (VALUE[0] != VALUE1[0]):
                exit(53)

            if (VALUE[0] == "int"):
                try:
                    if (int(VALUE[1]) < int(VALUE1[1])):
                        VALUEVAR = "true"
                    else:
                        VALUEVAR = "false"
                except:
                    exit(57)
            elif (VALUE[0] == "bool"):
                if (VALUE[1] == "false" and VALUE1[1] == "true"):
                    VALUEVAR = "true"
                else:
                    VALUEVAR = "false"
            elif (VALUE[0] == "string"):
                if (len(VALUE[1]) < len(VALUE1[1])):
                    VALUEVAR = "true"
                else:
                    VALUEVAR = "false"

            setVar(FRAME, VARNAME, ["bool", VALUEVAR])
        ##########################################################################
        # GT
        elif (Instruction[1] == "GT"):
            VALUE = None
            VALUE1 = None
            VALUEVAR = None
            FRAME = None
            VARNAME = None
            if (Instruction[2] != "var"):
                exit(32)

            if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "GF"
                VARNAME = re.sub(r'GF@', "", Instruction[3])
            elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "LF"
                VARNAME = re.sub(r'LF@', "", Instruction[3])
            elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "TF"
                VARNAME = re.sub(r'TF@', "", Instruction[3])
            else:
                exit(32)

            if (Instruction[4] != "int" and Instruction[4] != "bool" and Instruction[4] != "string" and Instruction[
                4] != "nil" and Instruction[4] != "var"):
                exit(32)
            if (Instruction[4] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'GF@', "", Instruction[5])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'LF@', "", Instruction[5])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'TF@', "", Instruction[5])
                    VALUE = getVar("TF", varName)
            elif (Instruction[4] == "string"):
                VALUE = ["string", Instruction[5]]
            elif (Instruction[4] == "int"):
                VALUE = ["int", Instruction[5]]
            elif (Instruction[4] == "bool"):
                VALUE = ["bool", Instruction[5]]
            else:
                exit(53)
            if (Instruction[6] != "int" and Instruction[6] != "bool" and Instruction[6] != "string" and Instruction[
                6] != "nil" and Instruction[6] != "var"):
                exit(32)
            if (Instruction[6] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'GF@', "", Instruction[7])
                    VALUE1 = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'LF@', "", Instruction[7])
                    VALUE1 = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'TF@', "", Instruction[7])
                    VALUE1 = getVar("TF", varName)
            elif (Instruction[6] == "string"):
                VALUE1 = ["string", Instruction[7]]
            elif (Instruction[6] == "int"):
                VALUE1 = ["int", Instruction[7]]
            elif (Instruction[6] == "bool"):
                VALUE1 = ["bool", Instruction[7]]
            else:
                exit(53)

            if (VALUE[0] != VALUE1[0]):
                exit(53)

            if (VALUE[0] == "int"):
                try:
                    if (int(VALUE[1]) > int(VALUE1[1])):
                        VALUEVAR = "true"
                    else:
                        VALUEVAR = "false"
                except:
                    exit(57)
            elif (VALUE[0] == "bool"):
                if (VALUE[1] == "true" and VALUE1[1] == "false"):
                    VALUEVAR = "true"
                else:
                    VALUEVAR = "false"
            elif (VALUE[0] == "string"):
                if (len(VALUE[1]) > len(VALUE1[1])):
                    VALUEVAR = "true"
                else:
                    VALUEVAR = "false"

            setVar(FRAME, VARNAME, ["bool", VALUEVAR])
        ##########################################################################
        # EQ
        elif (Instruction[1] == "EQ"):
            VALUE = None
            VALUE1 = None
            VALUEVAR = None
            FRAME = None
            VARNAME = None
            if (Instruction[2] != "var"):
                exit(32)

            if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "GF"
                VARNAME = re.sub(r'GF@', "", Instruction[3])
            elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "LF"
                VARNAME = re.sub(r'LF@', "", Instruction[3])
            elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "TF"
                VARNAME = re.sub(r'TF@', "", Instruction[3])
            else:
                exit(32)

            if (Instruction[4] != "int" and Instruction[4] != "bool" and Instruction[4] != "string" and Instruction[
                4] != "nil" and Instruction[4] != "var"):
                exit(32)
            if (Instruction[4] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'GF@', "", Instruction[5])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'LF@', "", Instruction[5])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'TF@', "", Instruction[5])
                    VALUE = getVar("TF", varName)
            elif (Instruction[4] == "string"):
                VALUE = ["string", Instruction[5]]
            elif (Instruction[4] == "int"):
                try:
                    VALUE = ["int", int(Instruction[5])]
                except:
                    exit(57)
            elif (Instruction[4] == "bool"):
                VALUE = ["bool", Instruction[5]]
            elif (Instruction[4] == "nil"):
                VALUE = ["nil", Instruction[5]]
            else:
                exit(53)
            if (Instruction[6] != "int" and Instruction[6] != "bool" and Instruction[6] != "string" and Instruction[
                6] != "nil" and Instruction[6] != "var"):
                exit(32)
            if (Instruction[6] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'GF@', "", Instruction[7])
                    VALUE1 = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'LF@', "", Instruction[7])
                    VALUE1 = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'TF@', "", Instruction[7])
                    VALUE1 = getVar("TF", varName)
            elif (Instruction[6] == "string"):
                VALUE1 = ["string", Instruction[7]]
            elif (Instruction[6] == "int"):
                try:
                    VALUE1 = ["int", int(Instruction[7])]
                except:
                    exit(57)
            elif (Instruction[6] == "bool"):
                VALUE1 = ["bool", Instruction[7]]
            elif (Instruction[6] == "nil"):
                VALUE1 = ["nil", Instruction[7]]
            else:
                exit(53)

            if (VALUE[0] == "int" and VALUE1[0] == "int"):
                try:
                    if (int(VALUE[1]) == int(VALUE1[1])):
                        VALUEVAR = "true"
                    else:
                        VALUEVAR = "false"
                except:
                    exit(57)
            elif (VALUE[0] == "bool" and VALUE1[0] == "bool"):
                if (VALUE[1] == "false" and VALUE1[1] == "true"):
                    VALUEVAR = "true"
                else:
                    VALUEVAR = "false"
            elif (VALUE[0] == "string" and VALUE1[0] == "string"):
                if (len(VALUE[1]) == len(VALUE1[1])):
                    VALUEVAR = "true"
                else:
                    VALUEVAR = "false"
            elif (VALUE[0] == "nil" or VALUE1[0] == "nil"):
                if (VALUE[1] == VALUE1[1]):
                    VALUEVAR = "true"
                else:
                    VALUEVAR = "false"
            else:
                exit(53)

            setVar(FRAME, VARNAME, ["bool", VALUEVAR])
        ##########################################################################
        # STRI2INT
        elif (Instruction[1] == "STRI2INT"):
            VALUE = None
            VALUE1 = None
            FRAME = None
            VARNAME = None
            if (Instruction[2] != "var"):
                exit(32)

            if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "GF"
                VARNAME = re.sub(r'GF@', "", Instruction[3])
            elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "LF"
                VARNAME = re.sub(r'LF@', "", Instruction[3])
            elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "TF"
                VARNAME = re.sub(r'TF@', "", Instruction[3])
            else:
                exit(32)

            if (Instruction[4] != "int" and Instruction[4] != "bool" and Instruction[4] != "string" and Instruction[
                4] != "nil" and Instruction[4] != "var"):
                exit(32)
            if (Instruction[4] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'GF@', "", Instruction[5])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'LF@', "", Instruction[5])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'TF@', "", Instruction[5])
                    VALUE = getVar("TF", varName)
            elif (Instruction[4] == "string"):
                VALUE = ["string", Instruction[5]]
            else:
                exit(53)

            if (Instruction[6] != "int" and Instruction[6] != "bool" and Instruction[6] != "string" and Instruction[
                6] != "nil" and Instruction[6] != "var"):
                exit(32)
            if (Instruction[6] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'GF@', "", Instruction[7])
                    VALUE1 = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'LF@', "", Instruction[7])
                    VALUE1 = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'TF@', "", Instruction[7])
                    VALUE1 = getVar("TF", varName)
            elif (Instruction[6] == "int"):
                VALUE1 = ["int", Instruction[7]]
            else:
                exit(53)

            if (VALUE[0] != "string" or VALUE1[0] != "int"):
                exit(53)
            try:
                setVar(FRAME, VARNAME, ["int", ord(VALUE[1][int(VALUE1[1])])])
            except:
                exit(58)
        ##########################################################################
        elif (Instruction[1] == "CONCAT"):
            VALUE = None
            VALUE1 = None
            FRAME = None
            VARNAME = None
            if (Instruction[2] != "var"):
                exit(32)

            if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "GF"
                VARNAME = re.sub(r'GF@', "", Instruction[3])
            elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "LF"
                VARNAME = re.sub(r'LF@', "", Instruction[3])
            elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "TF"
                VARNAME = re.sub(r'TF@', "", Instruction[3])
            else:
                exit(32)

            if (Instruction[4] != "int" and Instruction[4] != "bool" and Instruction[4] != "string" and Instruction[
                4] != "nil" and Instruction[4] != "var"):
                exit(32)
            if (Instruction[4] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'GF@', "", Instruction[5])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'LF@', "", Instruction[5])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'TF@', "", Instruction[5])
                    VALUE = getVar("TF", varName)
            elif (Instruction[4] == "string"):
                VALUE = ["string", Instruction[5]]
            else:
                exit(53)

            if (Instruction[6] != "int" and Instruction[6] != "bool" and Instruction[6] != "string" and Instruction[
                6] != "nil" and Instruction[6] != "var"):
                exit(32)
            if (Instruction[6] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'GF@', "", Instruction[7])
                    VALUE1 = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'LF@', "", Instruction[7])
                    VALUE1 = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'TF@', "", Instruction[7])
                    VALUE1 = getVar("TF", varName)
            elif (Instruction[6] == "string"):
                VALUE1 = ["string", Instruction[7]]
            else:
                exit(53)

            if (VALUE[0] != "string" or VALUE1[0] != "string"):
                exit(53)
            setVar(FRAME, VARNAME, ["string", VALUE[1] + VALUE1[1]])
        ##########################################################################
        # GETCHAR
        elif (Instruction[1] == "GETCHAR"):
            VALUE = None
            VALUE1 = None
            FRAME = None
            VARNAME = None
            if (Instruction[2] != "var"):
                exit(32)

            if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "GF"
                VARNAME = re.sub(r'GF@', "", Instruction[3])
            elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "LF"
                VARNAME = re.sub(r'LF@', "", Instruction[3])
            elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "TF"
                VARNAME = re.sub(r'TF@', "", Instruction[3])
            else:
                exit(32)

            if (Instruction[4] != "int" and Instruction[4] != "bool" and Instruction[4] != "string" and Instruction[
                4] != "nil" and Instruction[4] != "var"):
                exit(32)
            if (Instruction[4] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'GF@', "", Instruction[5])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'LF@', "", Instruction[5])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'TF@', "", Instruction[5])
                    VALUE = getVar("TF", varName)
            elif (Instruction[4] == "string"):
                VALUE = ["string", Instruction[5]]
            else:
                exit(53)

            if (Instruction[6] != "int" and Instruction[6] != "bool" and Instruction[6] != "string" and Instruction[
                6] != "nil" and Instruction[6] != "var"):
                exit(32)
            if (Instruction[6] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'GF@', "", Instruction[7])
                    VALUE1 = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'LF@', "", Instruction[7])
                    VALUE1 = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'TF@', "", Instruction[7])
                    VALUE1 = getVar("TF", varName)
            elif (Instruction[6] == "int"):
                VALUE1 = ["int", Instruction[7]]
            else:
                exit(53)

            if (VALUE[0] != "string" or VALUE1[0] != "int"):
                exit(53)
            try:
                setVar(FRAME, VARNAME, ["string", VALUE[1][int(VALUE1[1])]])
            except:
                exit(58)
        ##########################################################################
        # SETCHAR
        elif (Instruction[1] == "SETCHAR"):
            VALUE = None
            VALUE1 = None
            VALUEVAR = None
            FRAME = None
            VARNAME = None
            if (Instruction[2] != "var"):
                exit(32)

            if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "GF"
                VARNAME = re.sub(r'GF@', "", Instruction[3])
            elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "LF"
                VARNAME = re.sub(r'LF@', "", Instruction[3])
            elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "TF"
                VARNAME = re.sub(r'TF@', "", Instruction[3])
            else:
                exit(32)

            VALUEVAR = getVar(FRAME, VARNAME)

            if (Instruction[4] != "int" and Instruction[4] != "bool" and Instruction[4] != "string" and Instruction[
                4] != "nil" and Instruction[4] != "var"):
                exit(32)
            if (Instruction[4] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'GF@', "", Instruction[5])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'LF@', "", Instruction[5])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'TF@', "", Instruction[5])
                    VALUE = getVar("TF", varName)
            elif (Instruction[4] == "int"):
                VALUE = ["int", Instruction[5]]
            else:
                exit(53)

            if (Instruction[6] != "int" and Instruction[6] != "bool" and Instruction[6] != "string" and Instruction[
                6] != "nil" and Instruction[6] != "var"):
                exit(32)
            if (Instruction[6] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'GF@', "", Instruction[7])
                    VALUE1 = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'LF@', "", Instruction[7])
                    VALUE1 = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'TF@', "", Instruction[7])
                    VALUE1 = getVar("TF", varName)
            elif (Instruction[6] == "string"):
                VALUE1 = ["string", Instruction[7]]
            else:
                exit(53)

            try:
                if (VALUEVAR[0] != "string" or VALUE[0] != "int" or VALUE1[0] != "string"):
                    exit(53)

                tmp = list(VALUEVAR[1])
                try:
                    tmp1 = int(VALUE[1])
                except:
                    exit(57)
                tmp2 = list(VALUE1[1])
                tmp[tmp1] = tmp2[0]
                VALUEVAR[1] = ""
                for el in tmp:
                    VALUEVAR[1] += el
                setVar(FRAME, VARNAME, [VALUEVAR[0], VALUEVAR[1]])
            except:
                exit(58)
        ##########################################################################
        # DPRINT
        elif (Instruction[1] == "DPRINT"):
            VALUE = None
            if (Instruction[2] != "int" and Instruction[2] != "bool" and Instruction[2] != "string" and Instruction[
                2] != "nil" and Instruction[2] != "var"):
                exit(32)

            if (Instruction[2] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                    varName = re.sub(r'GF@', "", Instruction[3])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                    varName = re.sub(r'LF@', "", Instruction[3])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                    varName = re.sub(r'TF@', "", Instruction[3])
                    VALUE = getVar("TF", varName)
            elif (Instruction[2] == "string"):
                VALUE = ["string", Instruction[3]]
            elif (Instruction[2] == "int"):
                try:
                    VALUE = ["int", int(Instruction[3])]
                except:
                    exit(57)
            elif (Instruction[2] == "bool"):
                VALUE = ["bool", Instruction[3]]
            elif (Instruction[2] == "nil"):
                VALUE = ["nil", Instruction[3]]

            print(VALUE[1], file=sys.stderr)
        ##########################################################################
        # WRITE
        elif (Instruction[1] == "WRITE"):
            VALUE = None
            if (Instruction[2] != "int" and Instruction[2] != "bool" and Instruction[2] != "string" and Instruction[
                2] != "nil" and Instruction[2] != "var"):
                exit(32)

            if (Instruction[2] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                    varName = re.sub(r'GF@', "", Instruction[3])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                    varName = re.sub(r'LF@', "", Instruction[3])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                    varName = re.sub(r'TF@', "", Instruction[3])
                    VALUE = getVar("TF", varName)
            elif (Instruction[2] == "string"):
                VALUE = ["string", Instruction[3]]
            elif (Instruction[2] == "int"):
                try:
                    VALUE = ["int", int(Instruction[3])]
                except:
                    exit(57)
            elif (Instruction[2] == "bool"):
                VALUE = ["bool", Instruction[3]]
                if (VALUE[1] != "true" and VALUE[1] != "false"):
                    exit(57)
            elif (Instruction[2] == "nil"):
                VALUE = ["nil", Instruction[3]]
                if (VALUE[1] == "nil"):
                    VALUE[1] = ""
                else:
                    exit(57)

            print(VALUE[1], end='')
        ##########################################################################
        # READ
        elif (Instruction[1] == "READ"):
            VALUE = None
            FRAME = None
            VARNAME = None
            READ = None
            if (Instruction[2] != "var"):
                exit(32)

            if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "GF"
                VARNAME = re.sub(r'GF@', "", Instruction[3])
            elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "LF"
                VARNAME = re.sub(r'LF@', "", Instruction[3])
            elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                FRAME = "TF"
                VARNAME = re.sub(r'TF@', "", Instruction[3])
            else:
                exit(32)

            if (Instruction[4] != "int" and Instruction[4] != "bool" and Instruction[4] != "string" and Instruction[
                4] != "nil" and Instruction[4] != "var" and Instruction[4] != "type"):
                exit(32)

            if (Instruction[4] != "type"):
                exit(53)

            if (pathInput == "empty"):
                try:
                    READ = input()
                except:
                    READ = ""
            else:
                try:
                    READ = pathInput.readline()
                except:
                    READ = ""

            if (READ == ""):
                VALUE = ["nil", "nil"]
            elif (Instruction[5] == "string"):
                VALUE = ["string", READ]
            elif (Instruction[5] == "int"):
                try:
                    VALUE = ["int", int(READ)]
                except:
                    exit(57)
            elif (Instruction[5] == "bool"):
                if (READ == "true"):
                    VALUE = ["bool", "true"]
                else:
                    VALUE = ["bool", "false"]
            else:
                exit(57)

            setVar(FRAME, VARNAME, VALUE)
        ##########################################################################
        # EXIT
        elif (Instruction[1] == "EXIT"):
            VALUE = None
            if (Instruction[2] != "int" and Instruction[2] != "bool" and Instruction[2] != "string" and Instruction[
                2] != "nil" and Instruction[2] != "var"):
                exit(32)

            if (Instruction[2] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                    varName = re.sub(r'GF@', "", Instruction[3])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                    varName = re.sub(r'LF@', "", Instruction[3])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[3])):
                    varName = re.sub(r'TF@', "", Instruction[3])
                    VALUE = getVar("TF", varName)
            elif (Instruction[2] == "int"):
                try:
                    VALUE = ["int", int(Instruction[3])]
                except:
                    exit(57)

            try:
                VALUE[1] = int(VALUE[1])
                if not (VALUE[1] >= 0 and VALUE[1] <= 49):
                    exit(57)
            except:
                exit(57)
            exit(VALUE[1])
        ##########################################################################
        # LABEL
        elif (Instruction[1] == "LABEL"):
            if (Instruction[2] != "label"):
                exit(32)
            if (Instruction[3] in Label_Stack):
                exit(52)
            else:
                Label_Stack.append(Instruction[3])
        ##########################################################################
        # JUMP
        elif (Instruction[1] == "JUMP"):
            if (Instruction[2] != "label"):
                exit(52)

            for instruct in UniTable:
                if (instruct[1] == "LABEL"):
                    if (instruct[2] == "label"):
                        if (instruct[3] == Instruction[3]):
                            Label_Jump = int(instruct[0])
                            Interpretation(GF_Frame, LF_Frame, TF_Frame, TF_Existion, Stack, Label_Stack, Label_Call_Stack, Label_Jump)
            break
        ##########################################################################
        # JUMPIFEQ
        elif(Instruction[1] == "JUMPIFEQ"):
            VALUE = None
            VALUE1 = None
            VALUEVAR = None
            if(Instruction[2] != "label"):
                exit(32)

            if (Instruction[4] != "int" and Instruction[4] != "bool" and Instruction[4] != "string" and Instruction[
                4] != "nil" and Instruction[4] != "var"):
                exit(32)
            if (Instruction[4] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'GF@', "", Instruction[5])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'LF@', "", Instruction[5])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'TF@', "", Instruction[5])
                    VALUE = getVar("TF", varName)
            elif (Instruction[4] == "string"):
                VALUE = ["string", Instruction[5]]
            elif (Instruction[4] == "int"):
                try:
                    VALUE = ["int", int(Instruction[5])]
                except:
                    exit(57)
            elif (Instruction[4] == "bool"):
                VALUE = ["bool", Instruction[5]]
            elif (Instruction[4] == "nil"):
                VALUE = ["nil", Instruction[5]]
            else:
                exit(53)
            if (Instruction[6] != "int" and Instruction[6] != "bool" and Instruction[6] != "string" and Instruction[
                6] != "nil" and Instruction[6] != "var"):
                exit(32)
            if (Instruction[6] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'GF@', "", Instruction[7])
                    VALUE1 = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'LF@', "", Instruction[7])
                    VALUE1 = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'TF@', "", Instruction[7])
                    VALUE1 = getVar("TF", varName)
            elif (Instruction[6] == "string"):
                VALUE1 = ["string", Instruction[7]]
            elif (Instruction[6] == "int"):
                try:
                    VALUE1 = ["int", int(Instruction[7])]
                except:
                    exit(57)
            elif (Instruction[6] == "bool"):
                VALUE1 = ["bool", Instruction[7]]
            elif (Instruction[6] == "nil"):
                VALUE1 = ["nil", Instruction[7]]
            else:
                exit(53)

            if (VALUE[0] == "int" and VALUE1[0] == "int"):
                try:
                    if (int(VALUE[1]) == int(VALUE1[1])):
                        VALUEVAR = "true"
                    else:
                        VALUEVAR = "false"
                except:
                    exit(57)
            elif (VALUE[0] == "bool" and VALUE1[0] == "bool"):
                if (VALUE[1] == "true" and VALUE1[1] == "true" or VALUE[1] == "false" and VALUE1[1] == "false"):
                    VALUEVAR = "true"
                else:
                    VALUEVAR = "false"
            elif (VALUE[0] == "string" and VALUE1[0] == "string"):
                if (len(VALUE[1]) == len(VALUE1[1])):
                    VALUEVAR = "true"
                else:
                    VALUEVAR = "false"
            elif (VALUE[0] == "nil" or VALUE1[0] == "nil"):
                if (VALUE[1] == VALUE1[1]):
                    VALUEVAR = "true"
                else:
                    VALUEVAR = "false"
            else:
                exit(53)

            if(VALUEVAR == "true"):
                for instruct in UniTable:
                    if (instruct[1] == "LABEL"):
                        if (instruct[2] == "label"):
                            if (instruct[3] == Instruction[3]):
                                Label_Jump = int(instruct[0])
                                Interpretation(GF_Frame, LF_Frame, TF_Frame, TF_Existion, Stack, Label_Stack, Label_Call_Stack, Label_Jump)
                break
        ##########################################################################
        # JUMPIFNEQ
        elif (Instruction[1] == "JUMPIFNEQ"):
            VALUE = None
            VALUE1 = None
            VALUEVAR = None
            if (Instruction[2] != "label"):
                exit(32)

            if (Instruction[4] != "int" and Instruction[4] != "bool" and Instruction[4] != "string" and Instruction[
                4] != "nil" and Instruction[4] != "var"):
                exit(32)
            if (Instruction[4] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'GF@', "", Instruction[5])
                    VALUE = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'LF@', "", Instruction[5])
                    VALUE = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[5])):
                    varName = re.sub(r'TF@', "", Instruction[5])
                    VALUE = getVar("TF", varName)
            elif (Instruction[4] == "string"):
                VALUE = ["string", Instruction[5]]
            elif (Instruction[4] == "int"):
                try:
                    VALUE = ["int", int(Instruction[5])]
                except:
                    exit(57)
            elif (Instruction[4] == "bool"):
                VALUE = ["bool", Instruction[5]]
            elif (Instruction[4] == "nil"):
                VALUE = ["nil", Instruction[5]]
            else:
                exit(53)
            if (Instruction[6] != "int" and Instruction[6] != "bool" and Instruction[6] != "string" and Instruction[
                6] != "nil" and Instruction[6] != "var"):
                exit(32)
            if (Instruction[6] == "var"):
                if (re.match('^GF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'GF@', "", Instruction[7])
                    VALUE1 = getVar("GF", varName)
                elif (re.match('^LF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'LF@', "", Instruction[7])
                    VALUE1 = getVar("LF", varName)
                elif (re.match('^TF@[a-zA-z\_\$\&\%\*\!\?]', Instruction[7])):
                    varName = re.sub(r'TF@', "", Instruction[7])
                    VALUE1 = getVar("TF", varName)
            elif (Instruction[6] == "string"):
                VALUE1 = ["string", Instruction[7]]
            elif (Instruction[6] == "int"):
                try:
                    VALUE1 = ["int", int(Instruction[7])]
                except:
                    exit(57)
            elif (Instruction[6] == "bool"):
                VALUE1 = ["bool", Instruction[7]]
            elif (Instruction[6] == "nil"):
                VALUE1 = ["nil", Instruction[7]]
            else:
                exit(53)

            if (VALUE[0] == "int" and VALUE1[0] == "int"):
                try:
                    if (int(VALUE[1]) != int(VALUE1[1])):
                        VALUEVAR = "true"
                    else:
                        VALUEVAR = "false"
                except:
                    exit(57)
            elif (VALUE[0] == "bool" and VALUE1[0] == "bool"):
                if (VALUE[1] == "false" and VALUE1[1] == "true" or VALUE[1] == "true" and VALUE1[1] == "false"):
                    VALUEVAR = "true"
                else:
                    VALUEVAR = "false"
            elif (VALUE[0] == "string" and VALUE1[0] == "string"):
                if (len(VALUE[1]) != len(VALUE1[1])):
                    VALUEVAR = "true"
                else:
                    VALUEVAR = "false"
            elif (VALUE[0] == "nil" or VALUE1[0] == "nil"):
                if (VALUE[1] != VALUE1[1]):
                    VALUEVAR = "true"
                else:
                    VALUEVAR = "false"
            else:
                exit(53)

            if (VALUEVAR == "true"):
                for instruct in UniTable:
                    if (instruct[1] == "LABEL"):
                        if (instruct[2] == "label"):
                            if (instruct[3] == Instruction[3]):
                                Label_Jump = int(instruct[0])
                                Interpretation(GF_Frame, LF_Frame, TF_Frame, TF_Existion, Stack, Label_Stack, Label_Call_Stack, Label_Jump)
                break
        ##########################################################################
        elif(Instruction[1] == "CALL"):
            if(Instruction[2] != "label"):
                exit(32)

            for instruct in UniTable:
                if (instruct[1] == "LABEL"):
                    if (instruct[2] == "label"):
                        if (instruct[3] == Instruction[3]):
                            Label_Jump = int(instruct[0])
                            Label_Call_Stack.append(Instruction[0])
                            Interpretation(GF_Frame, LF_Frame, TF_Frame, TF_Existion, Stack, Label_Stack, Label_Call_Stack, Label_Jump)
            break
        ##########################################################################
        elif(Instruction[1] == "RETURN"):
            try:
                Interpretation(GF_Frame, LF_Frame, TF_Frame, TF_Existion, Stack, Label_Stack, Label_Call_Stack, Label_Call_Stack.pop())
            except:
                exit(56)
        ##########################################################################



PATHsource = "empty"
PATHinput = "empty"
pathSource = ""
pathInput = ""
orderCheckTable = []
UniTable = []
i = 0

# Načítání argumentů pomocí getopt
try:
    optlist, args = getopt.getopt(sys.argv[1:], '', ['help','source=','input='])
except getopt.GetoptError:
    exit(10)

# Kontrola prázného souboru
if(len(optlist) == 0):
    exit(10)

# Parsování argumentů
for index in optlist:
    if(index[0] == "--help"):
        # Kontrola 1 argumentu pro --help
        if(len(optlist) == 1):
            print("\t --help -vypíše nápovědu \n\t --input=file -cesta k souboru vstupních hodnot \n\t --source=file -cesta k souboru s XML kódem")
            exit(0)
        else:
            exit(10)

    # Kontrola cesty pro --input
    if ("--input" in index):
        if(os.path.isfile(index[1])):
            PATHinput = index[1]
        else:
            exit(11)

    # Kontrola cesty pro --source
    if ("--source" in index):
        if (os.path.isfile(index[1])):
            PATHsource = index[1]
        else:
            exit(11)

# Čtení ze souborů
if(PATHsource != "empty"):
    pathSource = open(PATHsource, 'r').read()
else:
    pathSource = sys.stdin.read()

if(PATHinput != "empty"):
    pathInput = open(PATHinput,'r')

# Sestavování XML pomocí xml.etree.ElementTree
try:
    root = ET.fromstring(pathSource)
except ET.ParseError:
    exit(31)

UniTable = xmlFunc(root)
instrCheck(UniTable)


GF_Frame = dict()
LF_Frame = []
TF_Frame = None
Stack = []
TF_Existion = False
Label_Stack = []
Label_Call_Stack = []
Label_Jump = 0

Interpretation(GF_Frame, LF_Frame, TF_Frame, TF_Existion, Stack, Label_Stack, Label_Call_Stack, Label_Jump)

