from lector import Lector
from Bottom_Up import LR0Parser

# Representación de la gramática
grammar = {
    'S': ['S+T', 'T'],
    'T': ['T*F', 'F'],
    'F': ['(S)', 'i']
}

noTerminals = ['S', 'T', 'F']
terminals = ['+', '*', '(', ')', 'i']
cadenas = ['i+i', '(i)', '(i+i)*i)']

# Calcular FIRST y FOLLOW
lector = Lector(noTerminals, grammar, {}, {})
follow = lector.followResultado

# Ejecutar el parser SLR(1)
parser = LR0Parser(grammar, terminals, noTerminals, cadenas, follow)
