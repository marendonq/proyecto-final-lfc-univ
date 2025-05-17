from lector import Lector
from Bottom_Up import LR0Parser

grammar = {
    'S': ['aSb', 'c']
}
noTerminals = ['S']
terminals = ['a', 'b', 'c']
cadenas = ['aacbb', 'acb', 'ab']

lector = Lector(noTerminals, grammar, {}, {})
parser = LR0Parser(grammar, terminals, noTerminals, cadenas, lector.followResultado)
