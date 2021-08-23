import re
from lexer.token import Token, Real, Number, Boolean
from lexer.keywords import KEYWORDS


class Lexer:
    def __init__(self, source_file):
        self.tokens = []
        self.source = source_file
        self.curr_idx = 0
        self.next_idx = 1
        self.col = 1
        #self.errors = []

    #Returns 
    def next_Token(self):
        if self.tokens:
            return self.tokens.pop(0)

    #Increments the indexes
    def go_on(self, delta=1):
        self.curr_idx += delta
        self.next_idx += delta
        self.col += delta

    #Returns Current character
    def cchar(self):
        if self.curr_idx < len(self.source):
            return self.source[self.curr_idx]
        return ''

    #Returns Next character
    def nchar(self):
        if self.next_idx < len(self.source):
            return self.source[self.next_idx]
        return ''

    def scan(self):
        line = 1
        while self.cchar():
            if self.cchar() == ' ' or self.cchar() == '\t':   #Ignore blanks
                self.go_on()
                continue
            if self.cchar() == '\n':    #Count new line
                line += 1
                self.col = 1
            elif self.cchar() == '/' and self.nchar() == '/':   #Ignore single-line comments
                while self.cchar() and self.nchar() != '\n':
                    self.go_on()
            elif self.cchar() == '/' and self.nchar() == '*':   #Ignore multi-line comments
                while self.cchar() and (self.cchar() != '*' or self.nchar() != '/'):
                    if self.cchar() == '\n':
                        line += 1
                        self.col = 1
                    self.go_on()
                self.go_on()
            elif self.cchar().isalpha():    #Begins with a letter
                category, value = self.classify_alpha(self.curr_idx)
                if category == 'BOOL':
                    self.tokens.append(Boolean(value, line, self.col))
                else:
                    self.tokens.append(Token(category, value, line, self.col))
            elif self.cchar().isdigit():    #Begins with a number
                category, value = self.classify_number(self.curr_idx)
                if category == 'REAL':
                    self.tokens.append(Real(value, line, self.col))
                elif category == 'NUMBER':
                    self.tokens.append(Number(value, line, self.col))
            else:   #Begins with a symbol
                category, value = self.classify_symbol()
                self.tokens.append(Token(category, value, line, self.col))
            self.go_on()

    def classify_alpha(self, begin):
        while self.nchar().isalpha() or self.nchar().isdigit() or self.nchar() in '_$':
            self.go_on()
        word = self.source[begin:self.next_idx]
        if word in KEYWORDS:
            if word == 'false' or word == 'true':
                return 'BOOL', bool(word)
            return KEYWORDS[word], word
        else:
            return 'IDENTIFIER', word
    
    def classify_number(self, begin):
        value = 'Unknown'
        category = 'Unknown'
        if self.cchar() == '0':
            if self.nchar() == '.':
                self.go_on()
                while self.nchar().isdigit():
                    self.go_on()
                value = float(self.source[begin:self.next_idx])
                category = 'REAL'
            elif self.nchar() == 'x':
                self.go_on()
                while self.nchar().isdigit() or self.nchar() in 'abcdefABCDEF':
                    self.go_on()
                value = int(self.source[begin:self.next_idx], 16)
                category = 'NUMBER'
            elif self.nchar().isdigit():
                self.go_on()
                while self.nchar().isdigit():
                    self.go_on()
                value = int('0o' + self.source[begin:self.next_idx], 8)
                category = 'NUMBER'
            else:
                value = 0
                category = 'NUMBER'
        elif self.nchar() == '.':
            self.go_on()
            while self.nchar().isdigit():
                self.go_on()
            value = float(self.source[begin:self.next_idx])
            category = 'REAL'
        elif self.nchar().isdigit():
            while self.nchar().isdigit():
                self.go_on()
            value = int(self.source[begin:self.next_idx])
            category = 'NUMBER'
        else:
            value = int(self.cchar())
            category = 'NUMBER'

        return category, value
        

    def classify_symbol(self):
        value = 'Unknown'
        category = 'Unknown'
        key = self.cchar()
        while (key + self.nchar()) in KEYWORDS and self.cchar():
            self.go_on()
        if key in KEYWORDS:
            value = key
            category = KEYWORDS[key]

        return category, value