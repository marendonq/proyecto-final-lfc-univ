#Equipo compuesto por:
# Sara Isabel Ortiz Henao
# Nicolás Betancur Ochoa
# Juan Jose Cañon
# Julian Andres Romero Hinestroza

class RecursiveParser:
    def __init__(self, nonterminals, grammar):
        self.nonterminals = nonterminals
        self.grammar = grammar
        self.input_string = ""
        self.current_index = 0
    
    def recursive_parser(self, A):
        
        if self.current_index >= len(self.input_string):
            return False
        
        if A not in self.grammar:
            return False
        
        for production in self.grammar[A]:
            original_index = self.current_index
            success = True

            for symbol in production:
                if self.current_index >= len(self.input_string):
                    success = False
                    break

                a = self.input_string[self.current_index]
                if symbol in self.nonterminals:
                    if not self.recursive_parser(symbol):
                        success = False
                        break
                elif symbol == a:
                    self.current_index += 1
                else:
                    success = False
                    break

            if success:
                return True
                        
            # Reset the current index for backtracking
            self.current_index = original_index

        return False

    def parse(self, input_string):
        self.input_string = input_string
        self.current_index = 0
        if self.recursive_parser(self.nonterminals[0]) and self.current_index == len(input_string):
            return "yes"
        else:
            return "no"

if __name__ == "__main__":
    n, m, k = map(int, input().split())
    nonterminals = input().split()
    grammar = {}
    for _ in range(m):
        rule = input().split('-')  
        if len(rule) != 2:
            print(f"Error parsing rule: {rule}")
            continue
        if rule[0] not in grammar:
            grammar[rule[0]] = []
        grammar[rule[0]].append(rule[1])

    for noterminal in nonterminals:
        lista=grammar[noterminal]
        for  n in range(len(lista)):
                if lista[n][0]==noterminal:
                    aux=lista[n]
                    lista[n]=lista[len(lista)-1]
                    lista[len(lista)-1]=aux
                    grammar[noterminal]=lista
                #     print("Existe recursividad por la izquierda")
                # else:
                #     print("No existe recursividad por la izquierda")
        #print(noterminal,grammar[noterminal])


    parser = RecursiveParser(nonterminals, grammar)
    for _ in range(k):
        input_string = input()
        print(parser.parse(input_string))


"""
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

1 2 3
S
S-aSb
S-c
aacbb
acb
ab

1 2 3
S
S-Sa
S-c
caaa
ca
acaa                                                                                   

"""