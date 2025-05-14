# Clase Lector para hacer el calculo de First and Follow
class Lector:
    def __init__(self, noTerminals, grammar,First,followResultado):
        self.noTerminals=noTerminals
        self.grammar=grammar
        self.First=First
        self.followResultado=followResultado
        # Primero calculamos First para cada no terminal
        for noTerminal in self.noTerminals:
            self.first(noTerminal,self.grammar)
        # Ahora Calculamos Follow para cada no terminal
        self.follow()
        
    # Funcion para hallar el First de los no terminales
    def first(self,noTerminal,grammar):
        # extraemos la gramatica
        reglas=grammar[noTerminal]
        #añadimos el terminal al diccionario del First
        if noTerminal not in self.First:
                    self.First[noTerminal]=[]
        # Recorremos las reglas
        for regla in reglas:
            #si el primer caracter es un Terminal, lo añadimos al first del no terminal
            if regla[0] not in self.noTerminals:
                # verificamos que no exista ya el terminal en el First del terminal
                if regla[0] not in self.First[noTerminal]:
                    self.First[noTerminal].append(regla[0])
                else: continue
            else: # si el primer caracter es un no terminal
                # verificamos que el caracter no sea el mismo no terminal 
                if regla[0] != noTerminal:
                    # hallamos el first del no terminal
                    self.first(regla[0],grammar)
                    # Recorremos el first del caracter no terminal
                    for a in self.First[regla[0]]:
                        # verificamos que no exista ya el terminal en el First del terminal
                        if a not in self.First[noTerminal]:
                            self.First[noTerminal].append(a)

    # Funcion para calcular el Follow
    def follow(self):
        # recorremos cada no terminal
        for nonTerminal in self.noTerminals:
            # añadimos el no terminal al diccionario
            if nonTerminal not in self.followResultado:
                self.followResultado[nonTerminal]=set()
            
            #primera Regla Follow(A)={$}
            if nonTerminal==self.noTerminals[0]:
                self.followResultado[nonTerminal].add('$')
        
        #segunda Regla A → αBβ First(β) ∈ Follow(B)
        #
        for noTerminal,ruleNonTerminal in self.grammar.items():
            for regla in ruleNonTerminal:
                for i in range(len(regla)-1):
                    if regla[i] in self.noTerminals:
                        if regla[i+1] in self.noTerminals:
                            for first in self.First[regla[i+1]]:
                                if first != "e":
                                    self.followResultado[regla[i]].add(first)
                        elif regla[i+1] != "e":
                            self.followResultado[regla[i]].add(regla[i+1])
        
        #tercera Regla A → αB Follow(B) = Follow(A)
        for noTerminal,ruleNonTerminal in self.grammar.items():
            for regla in ruleNonTerminal:
                if regla[len(regla)-1] in self.noTerminals:
                    for fo in self.followResultado[noTerminal]:
                        self.followResultado[regla[len(regla)-1]].add(fo)

