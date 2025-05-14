from lector import *
from TopDown import *
from Bottom_Up import *


if __name__=="__main__":
    #entrada numero de gramaticas
    gramarticas=int(input())
    numGramatica=0
    while(numGramatica<gramarticas):
        # Guarda valores de n m y k
        n,m,k = map(int,input().split())
        # Guarda los no terminales de la gramatica
        noTerminals=input().split(' ')
        # Guarda las reglas de la gramatica
        grammar={}
        # Asignar reglas a terminalesclear
        for i in range(m):
            rule=input().split('-')
            if len(rule)!=2:
                #print(f"Error in rule: {rule}")
                continue
            if rule[0] not in grammar:
                grammar[rule[0]]=[]
            grammar[rule[0]].append(rule[1])
        # Guardar cadenas
        cadenas=[]
        for i in range(k):
            cadena=str(input())
            cadenas.append(cadena)
        # Para implementar First y Follow
        lector=Lector(noTerminals,grammar,{},{})
        # Top-down parsing
        top_down=Top_down(lector.First,lector.followResultado,grammar,noTerminals,cadenas)
        #bottom_up = LR0Parser(lector.followResultado,grammar,noTerminals,cadenas)
        numGramatica+=1
        


        
'''
CASO DE PRUEBA INICIAL
1
1 2 3
S
S-aSb
S-c
aacbb
acb
ab

salida
si
si
no
'''

'''
Segundo caso de prueba.
1
2 4 4
S A
S-aSb
S-A
A-aA
A-a
aaabb
aabb
aaaaaaaaaabbbb
ab

salida
si
no
si
no
'''

'''
Tercer caso de prueba.
1
3 5 1
S T E
S-iEtST
S-a
T-cS
T-e
E-b
ibta

salida
error
'''

'''
3
1 2 3
S
S-aSb
S-c
aacbb
acb
ab
2 4 4
S A
S-aSb
S-A
A-aA
A-a
aaabb
aabb
aaaaaaaaaabbbb
ab
3 5 1
S T E
S-iEtST
S-a
T-cS
T-e
E-b
ibta
'''


'''
caso de prueba 4
1
1 2 10
S
S-aSb
S-c
aaaacbbbb
c
aaaaaacbbbbbb
acb
aaacbbb
aaaacbbb
cb
aaaaacbbbbbb
ac
d

Salida
yes
yes
yes
yes
yes
no
no
no
no
no
'''


'''
Caso recursividad izquierda
1
1 3 3
S
S-iSf
S-SSa
S-s
s
sssssssssssssssssssssssssssssf
isfisfif
'''

'''
segundo cado recursividad izquierda
1
1 2 10
S
S-Sa
S-a
aaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
b
c
aaaaaaaaaaaaaaaaaaaaac
aaaaaaacaaaaa
baaaaaaaaaaaa
'''