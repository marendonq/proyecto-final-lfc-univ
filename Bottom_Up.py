class LR0Parser:

    def __init__(self, Grammar, terminals, NoTerminals, cadenas):
        self.Grammar = Grammar
        self.terminals = terminals
        self.NoTerminals = NoTerminals
        self.start_symbol = cadenas[0]
        self.build_parsing_table()
        self.extenderGramatica()
        self.GOTO

    def build_parsing_table(self):
        self.closure = []
        self.goto = []
        self.items = []
        self.parsing_table = {}

    def extenderGramatica(self):
        extend =  self.NoTerminals[0]+"'"
        self.Grammar[extend]=[self.NoTerminals[0]]
        print(self.Grammar)


    def GOTO(self, item_set, symbol):
        goto_set = set()
        for item in item_set:
            if item[2] < len(item[1]) and item[1][item[2]] == symbol:
                new_item = (item[0], item[1], item[2] + 1)
                goto_set.add(new_item)
        return self.closure_lr0(goto_set) if goto_set else None


   