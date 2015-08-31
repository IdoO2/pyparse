#! /usr/bin/env python3
#! -*- coding: utf8 -*-
# Author: Cyril RICHARD

import      re,    sys
from type_code import *
from time import timezone
from types import NoneType,TypeType

test1 = 1 + 2 + \
5

test2 = 1 + 2 + \
5 + \
78

a = (
    '1' + '2' + '3' + '4' +
    '12' + '7')


b = (
    '1' + '2' + '3' + '4' )
c=6

a = c ; E = "d" ;     D = 1 ;

M = m = cd = 10
print "M=T"
# ============ FONCTIONS ============ #

#nettoie une ligne en :
#   . supprimant les espaces aux extrémités
#   . supprimant l'indentation supperflux
def cleanLine(line) :
    line = re.sub(rdic['cl_indent'], ' ', line)
    line = re.sub(rdic['cl_arg'], ',', line)
    if len(line) and line[0] == ' ' : line = line[1:]
    if len(line) and line[-1] == ' ' : line = line[:-1]
    return line

def execReg(reg, line) :
    tmp = re.compile(reg)
    return tmp.match(line)

def       onliner() : print "online" ; return False
def onliner2() : print "online" ; return False

# ============ REGEX ============ #

rdic = {}
rdic['cl_indent'] = '[\t\s]+' #récupère toute l'indentation
rdic['cl_fct'] = '[{\s]+$' #on récupère les { ou ' ' de la fin
rdic['cl_end'] = '[;\s\t]+$' #on récupère  la fin de la ligne
rdic['cl_cmt'] = '(.+)(?=//|/\*)' #traite les commentaires sur une lignes
rdic['cl_mcmt'] = '[^/]+/\s*(.+)' # traite la fin des commentaires multiligne /* */
rdic['cl_var'] = '(.+(?=\=))' #récupère les informations avant l'affectation
rdic['cl_bracket'] = '\[[\w]*\]' #on enlève les crochets et ce qu'il y a entre
rdic['cl_syntax'] = '[)({}"\';!,\[\]+]' #récup_re certain élément de syntax pour les supprimer
rdic['cl_arg'] = '\s,|,\s' #traite les arguments dans une fonction
rdic['cl_mult'] = r'\\\n|\\' #traite les déclaration en multilie (#define \\n etc...)

rdic['include'] = '#include[<"\s]*([^>\s"]+)' #traite les include
rdic['define'] = '#define ([^)]+\)|[^\s]+) ([^/]+)' #découpe le define en deux partie, une avec un nom, l'autre avec les instructions
rdic['define_arg'] = '([^\s(]+)[\s(]*([^)]+)' #si il y a des arguments on les récupères.
rdic['typedef'] = 'typedef\s(.+)(?=NAME)' #definition dynamique, NAME est remplacé par le du typedef, on récupère donc la définition
rdic['fonction'] = '([^(]+)\(([^)]*)' #on récupère le début de la déclaration (type et nom) et les arguments
rdic['variable_scope'] = '(extern|static) (.+)' #détermine si il y a un scope


# ============ CLASSE ============ #

class Test1 : pass


class Test(str) :
    def __init__(self) :
        print "test"
    def    test() :
        print "test"
class CCode(object) :

    def __init__(self, txt) :
        self.varType = [
            'char', 'unsigned char', 'short int', 'unsigned short int', 'int',
            'unsigned int', 'long int', 'unsigned long int', 'float', 'double',
            'long double', 'void']
        self.include = []
        self.define = []
        self.typedef = []
        self.fonction = []
        self.vars = []
        self.txt = []
        self.symbol = {
            'include': self.include, 'define': self.define, 'typedef': self.typedef,
            'fonction': self.fonction, 'variable': self.vars
        }
        self.__preProcess(txt) #on prétraite le texte
        self.__getSymbol() #on traite le texte en récupérant les symboles
        self.__setUse() #on recherche où les symboles sont utilisés



    #Traite le texte afin de l'uniformisé et de simplifier les traitements ultérieurs.
    def __preProcess(self, txt) :
        i = x = 0
        cline = ""
        txt = txt.replace('\n{', '{\n') #on uniformise la syntaxe
        txt = txt.split('\n')

        while (i < len(txt)) : #on utilise un while pour gérer directement la position de l'index i
            txt[i] = cleanLine(txt[i])

            #si on a un symbole permettant une déclaration sur plusieurs ligne
            #on remet tout sur une ligne + des lignes vides pour conserver une numérotation correct
            if '\\\n' in txt[i] + '\n' :
                cline = cline + txt[i]
                i = i + 1 ; x = x + 1
                if '\\\n' in txt[i] + '\n' :
                    continue
                #cline = (cline + txt[i]).replace('\\\n', ' ').replace('\\', ' ')
                cline = re.sub(rdic['cl_mult'], ' ', cline + txt[i])
                cline = re.sub(rdic['cl_indent'], ' ', cline)
                self.txt.append(cline)
                for z in range(x) : self.txt.append('')
                cline = ""

            #on enlève les commentaires sur une ligne
            elif "//" in txt[i] or "/*" in txt[i] and "*/" in txt[i] :
                f = execReg(rdic['cl_cmt'], txt[i])
                if f : self.txt.append(f.group(1))
                else : self.txt.append('')

           #on traite les commentaires sur plusieurs lignes
           #on ajoute des lignes vides pour compenser
            elif "/*" in txt[i] :
                while "*/" not in txt[i] :
                    i = i + 1 ; x = x + 1
                for z in range(x) : self.txt.append('')
                f = execReg(rdic['cl_mcmt'], txt[i])
                if f : self.txt.append(f.group(1))
            else :
                self.txt.append(txt[i])
            x = 0 ; i = i + 1

    #récupère les includes
    def __addInclude(self, n, txt) :
        include = execReg(rdic["include"], txt)
        self.include.append(Include(n+1, include.group(1)))

    #récupère les define
    def __addDefine(self, n, txt) :
        define = execReg(rdic["define"], txt)
        name = define.group(1)
        desc = define.group(2)
        args = ''
        #si il y a des arguments, on les récupères
        if '(' in name :
            head = execReg(rdic['define_arg'], name)
            name = head.group(1)
            args = head.group(2)
        self.define.append(Define(n+1, name, desc, args))

    #récupère les typdef
    def __addTypedef(self, n, txt) :
        l = re.sub(rdic['cl_end'], '', txt) #on enlève la fin
        name = l.split()[-1] #on récupère le nom et on le remplace dans la regex
        typedef = execReg(rdic['typedef'].replace("NAME", name), l)
        desc = typedef.group(1) #on récupère tout ce qu'il y a entre typedef et le nom.
        self.typedef.append(Typedef(n+1, name, desc))
        self.varType.append(name) #on ajoute au type disponible dans le fichier

    #récupère les fonctions
    def __addFunction(self, n, txt) :
        l = re.sub(rdic['cl_fct'], '', txt)
        fct = execReg(rdic['fonction'], l)
        typ = ' '.join(fct.group(1).split()[:-1]) #on récupère le type
        name = fct.group(1).split()[-1] #dernière mot du premier groupe
        args = fct.group(2) #récupérer en intégralité par la regex
        self.fonction.append(Fonction(n+1, name, typ, args))

    #récupère les variables
    def __addVariable(self, n, l) :
        #si il y a plusieurs déclarations par ligne on les traites toutes
        for v in l.split(';') :
            cv = cleanLine(v)

            if '=' in cv : cv = execReg(rdic['cl_var'], cv).group(1)

            if len(cv.split()) < 2 : continue
            #est-elle static ou extern ?
            f = execReg(rdic['variable_scope'], cv)
            if f :
                scope = f.group(1)
                cv = f.group(2)
            else : scope = "" #sinon elle est rien de tout ça.

            names = cv.split()[-1] #le nom est systématiquement en dernier
            typ = ' '.join(cv.split()[:-1]) #on récupère le type
            for x in names.split(',') : # si il y a une multidéclaration, on la traite
                if '[' and ']' in x :
                    x = re.sub(rdic['cl_bracket'], '', x) #si besoin on traite les crochets
                self.vars.append(Variable(n+1, x, typ, scope))

    #la ligne commence t-elle par un type ?
    def __isTyped(self, line) :
        if len(line) and line.split()[0] in self.varType : return line.split()[0]
        return False

    #switch, détecte si une ligne peut abriter certaine définition de symbole
    def __getSymbol(self) :
        for i in range(len(self.txt)) :
            l = self.txt[i]
            typ = self.__isTyped(l)
            if "include" in l : self.__addInclude(i, l)
            if "define" in l : self.__addDefine(i, l)
            if "typedef" in l : self.__addTypedef(i, l)
            #une fonction possède un type, au moins 1 '(' et au moins 1 '{'
            if typ and '(' in l and '{' in l : self.__addFunction(i, l)
            #une variable est typée, sa déclaration termine par ';'
            #elle ne contient pas de '(' sauf si c'est une affectation (donc un '=') qui utilise une fonction
            #la portée est éventuellement désigné par les mots clés 'static' & 'extern'
            if (typ and ';' and ((not '(' in l) or ('(' in l and '=' in l))) or "static" in l or "extern" in l :
                self.__addVariable(i, l)

    #définit si un symbol est utilisé ou pas.
    def __setUse(self) :
        for i in range(len(self.txt)) :
            #on nettoie la syntaxe des lignes pour faire émerger des simboles
            l = re.sub(rdic['cl_syntax'], ' ', self.txt[i])
            for m in l.split() : # on traite mot par mot
                for k in self.symbol.keys() : #on récupère les listes de symboles
                    for s in self.symbol[k] : #on récupère les symboles
                        #si le nom d'un symbole correspond au nom d'un mot et que ce n'est pas sa ligne de déclaration
                        #on renseigne la ligne comme une ligne ou il est utilisé
                        if s.getName() == m and i+1 != s.getLine() : s.addUseLine(i+1)

    #imprime les symboles deux types d'impressions :
    #   . Init: imprime les infos sur l'initialisation.
    #   . Use: imprime les infos sur l'utilisation du symbol
    def showSymbol(self, type) :
        for k in self.symbol.keys() :
            print k.upper() #on imprime le type de symbol
            for s in self.symbol[k] : eval("s.show" + type + "()") #on appel la méthode qui commande l'affichage
            print

# ============ MAIN ============ #
if len(sys.argv) != 2 :
    msg = "trouve des symboles dans du code C"
    msg = msg + "'liste de fichiers à traiter'"
    exit('missing source-file name')

fd = open(sys.argv[1], "r")
c = CCode(fd.read())
c.showSymbol("Init")
c.showSymbol("Use")
fd.close()

exit(0)
