from lector import *

class Top_down:
    def __init__(self,First,Follow,Grammar,NoTerminals,cadenas):
        self.First=First
        self.Follow=Follow
        self.Grammar=Grammar
        self.NoTerminals=NoTerminals
        self.cadenas=cadenas
        self.Terminals=set()
        self.Resultados=[]
        self.terminals()
        self.Terminals=list(self.Terminals)
        self.eliminateLeftRecursion()
        lector=Lector(self.NoTerminals,self.Grammar,{},{})
        self.First=lector.First
        self.Follow=lector.followResultado
        self.NotLL1=self.verifyLL1()
        #print("grammar ",self.Grammar,
          #    " noTerminals ",self.Terminals,
          #    "Terminals ",self.NoTerminals)
        #print("FIRST: ",self.First)
        #print("FOLLOW: ",self.Follow) 
        #self.verifyLL1()
        #self.detect_and_eliminate_left_recursion()
        self.TableM = [["" for _ in range(len(self.Terminals))] for _ in range(len(self.NoTerminals))]
        self.dicRows={}
        self.dicColumns={}
        self.Error=False
        self.dicAsing()
        self.predictiveParsingTable()
        #print("Tabla :")
        #print(self.TableM)
        for cadena in self.cadenas:
            self.Resultados.append(self.predictiveParsing(cadena))
        for valores in self.Resultados:
            print(valores)
        
    def terminals(self):
        for nt,produccions in self.Grammar.items():
            for produccion in produccions:
                for item in produccion:
                    if item not in self.NoTerminals and item != "e":
                        self.Terminals.add(item)
        self.Terminals.add('$')
        

    def dicAsing(self):
        contRows=0
        contColumns=0
        for terminal in self.Terminals:
            self.dicColumns[terminal]=contColumns
            contColumns+=1
        for noTerminal in self.NoTerminals:
            self.dicRows[noTerminal]=contRows
            contRows+=1
    

    def predictiveParsingTable(self):
        for noTerminal in self.NoTerminals:
            for produccion in self.Grammar[noTerminal]:
                first=self.getFirst(produccion)
                for terminal in first:
                    if terminal != "e":
                        if self.TableM[self.dicRows[noTerminal]][self.dicColumns[terminal]]=="":
                            self.TableM[self.dicRows[noTerminal]][self.dicColumns[terminal]]=noTerminal+"->"+produccion
                        else:
                            self.Error=True
                    elif terminal == "e":
                        for terminalf in self.Follow[noTerminal]:
                            if self.TableM[self.dicRows[noTerminal]][self.dicColumns[terminalf]]=="":
                                self.TableM[self.dicRows[noTerminal]][self.dicColumns[terminalf]]=noTerminal+"->"+produccion
                                #print(noTerminal,terminalf," = ",noTerminal," -> ",produccion)
                
                                               
    def predictiveParsing(self,cadena):
        posicion=0
        TStack=['$','S'] #pila
        wString=cadena+'$'
        a=wString[posicion]
        xTop=TStack[-1]
        while(xTop!='$'):
            #print(wString,a,TStack)
            if xTop==a:
                TStack.pop()
                xTop=TStack[-1]
                posicion+=1
                a=wString[posicion]
            elif a not in self.Terminals and a!="e":
                self.Error=True
                #print("Error caracter desconocido")
                break
            elif a in self.Terminals and xTop in self.NoTerminals: 
                if self.TableM[self.dicRows[xTop]][self.dicColumns[a]] == "":
                    #print("Error tabla error")
                    #self.Error=True
                    break
                else:
                    TStack.pop()
                    regla=self.TableM[self.dicRows[xTop]][self.dicColumns[a]]
                    regla=regla.split("->")
                    producion=regla[1]
                    for valor in reversed(producion):
                        if valor!="e":
                            TStack.append(valor)
                    xTop=TStack[-1]
            else:
                self.Error=True
                break
            #input()
        #print(wString,a,TStack)
        if a == TStack[-1]:
            return "si"
        elif a != TStack[-1] or self.Error: 
            return "no"
                
            
    def getFirst(self,cadena):
        for i in range(len(cadena)):
            if cadena[i] not in self.NoTerminals:
                return cadena[i]
            else:
                return self.First[cadena[i]]
            

    #---------------------------VERIFICAR LL(1)---------------------------
    def verifyLL1(self):
        interseccion=False
        for noTerminal in self.NoTerminals:
            if len(self.Grammar[noTerminal])>1:
                for alpha in self.Grammar[noTerminal]:
                    for beta in self.Grammar[noTerminal]:
                        if alpha!=beta and alpha!="e" and beta!="e":
                            firstAlpha=self.getFirst(alpha)
                            firstBeta=self.getFirst(beta)
                            if len(firstAlpha) == 1 and firstAlpha[0]=="e":
                                for firstB in firstBeta:
                                    for followTerminal in self.Follow[noTerminal]:
                                        if firstB==followTerminal:
                                            interseccion=True
                                            return interseccion
                            elif len(firstBeta)==1 and firstBeta[0]=="e":
                                for fisrtA in firstAlpha:
                                    for followTerminalA in self.Follow[noTerminal]:
                                        if fisrtA==followTerminalA:
                                            interseccion=True
                                            return interseccion
                            else:
                                for firstA in firstAlpha:
                                    for firstB in firstBeta:
                                        if firstA==firstB:
                                            interseccion=True
                                            return interseccion
            else:
                for Alpha in self.Grammar[noTerminal]:
                    firstAlpha=self.getFirst(Alpha)
                    for follows in self.Follow[noTerminal]:
                        if firstAlpha==follows:
                            interseccion=True
                            return interseccion               
        return interseccion

 #---------------------------ELIMINAR RECURSIVIDAD POR IZQUIERDA---------------------------

    def eliminateLeftRecursion(self):
        posiblesNoTerminales = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        #print("eliminating left recursion")
        NewGrammar={}
        NewNoTerminals=[]
        needEliminate=False
        for noTerminal in self.NoTerminals:
            if noTerminal not in NewNoTerminals:
                NewNoTerminals.append(noTerminal)
            if noTerminal not in NewGrammar:
                NewGrammar[noTerminal]=[]
            for produccion in self.Grammar[noTerminal]:
                # Si tiene Recursividad Izquierda
                if produccion[0]==noTerminal:
                    needEliminate=True
                    break
            # Eliminar Recursividad directa
            if needEliminate:
                auxiliarTerminal=''
                for posibleNoTerminal in  posiblesNoTerminales:
                    if posibleNoTerminal not in self.NoTerminals and posibleNoTerminal not in NewNoTerminals:
                        auxiliarTerminal=posibleNoTerminal
                        NewNoTerminals.append(auxiliarTerminal)
                        NewGrammar[auxiliarTerminal]=[]
                        break
                for produccion in self.Grammar[noTerminal]:
                    if produccion[0]==noTerminal:
                        NewGrammar[auxiliarTerminal].append(produccion[1:]+auxiliarTerminal)
                    else:
                        NewGrammar[noTerminal].append(produccion+auxiliarTerminal)
            else:
                NewGrammar[noTerminal]=self.Grammar[noTerminal]
        self.Grammar=NewGrammar
        self.NoTerminals=NewNoTerminals                    
        #print("new grammar ",NewGrammar,"new noTerminals ",NewNoTerminals)        