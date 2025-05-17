class LR0Parser:

    def __init__(self, Grammar, terminals, NoTerminals, cadenas, follow):
        self.Grammar = Grammar
        self.terminals = list(terminals) + ['$']
        self.NoTerminals = NoTerminals
        self.start_symbol = NoTerminals[0] + "'"
        self.follow = follow
        self.extenderGramatica()
        self.states = []
        self.transitions = {}
        self.action_table = {}
        self.goto_table = {}
        self.build_parsing_table()
        for cadena in cadenas:
            print(self.parse(cadena))

    def extenderGramatica(self):
        extend = self.NoTerminals[0] + "'"
        self.Grammar[extend] = [self.NoTerminals[0]]
        self.NoTerminals.insert(0, extend)

    def closure_lr0(self, items):
        closure = set(items)
        added = True
        while added:
            added = False
            new_items = set()
            for head, body, dot in closure:
                if dot < len(body):
                    symbol = body[dot]
                    if symbol in self.Grammar:
                        for prod in self.Grammar[symbol]:
                            item = (symbol, prod, 0)
                            if item not in closure:
                                new_items.add(item)
            if new_items:
                closure |= new_items
                added = True
        return frozenset(closure)

    def GOTO(self, items, symbol):
        goto_set = set()
        for head, body, dot in items:
            if dot < len(body) and body[dot] == symbol:
                goto_set.add((head, body, dot + 1))
        return self.closure_lr0(goto_set) if goto_set else None

    def build_parsing_table(self):
        initial = self.closure_lr0([(self.start_symbol, self.Grammar[self.start_symbol][0], 0)])
        self.states = [initial]
        self.transitions = {}

        i = 0
        while i < len(self.states):
            state = self.states[i]
            symbols = set()
            for head, body, dot in state:
                if dot < len(body):
                    symbols.add(body[dot])
            for symbol in symbols:
                goto = self.GOTO(state, symbol)
                if goto:
                    if goto not in self.states:
                        self.states.append(goto)
                    self.transitions[(i, symbol)] = self.states.index(goto)
            i += 1

        for idx, state in enumerate(self.states):
            self.action_table[idx] = {}
            self.goto_table[idx] = {}
            for item in state:
                head, body, dot = item
                if dot < len(body):
                    symbol = body[dot]
                    if symbol in self.terminals:
                        next_state = self.transitions.get((idx, symbol))
                        if next_state is not None:
                            self.action_table[idx][symbol] = ('shift', next_state)
                else:
                    if head == self.start_symbol:
                        self.action_table[idx]['$'] = ('accept',)
                    else:
                        for f in self.follow[head]:
                            self.action_table[idx][f] = ('reduce', head, body)
            for nt in self.NoTerminals:
                if (idx, nt) in self.transitions:
                    self.goto_table[idx][nt] = self.transitions[(idx, nt)]

    def parse(self, cadena):
        stack = [0]
        input_buffer = list(cadena) + ['$']
        idx = 0

        while True:
            state = stack[-1]
            symbol = input_buffer[idx]
            action = self.action_table.get(state, {}).get(symbol)

            if action is None:
                return 'no'

            if action[0] == 'shift':
                stack.append(symbol)
                stack.append(action[1])
                idx += 1
            elif action[0] == 'reduce':
                head, body = action[1], action[2]
                if body != 'e':
                    for _ in range(len(body) * 2):
                        stack.pop()
                state = stack[-1]
                stack.append(head)
                stack.append(self.goto_table[state][head])
            elif action[0] == 'accept':
                return 'yes'


   