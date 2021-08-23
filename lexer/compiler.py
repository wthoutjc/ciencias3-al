from lexer.lexer import Lexer

with open('Test','r') as f:
   lex = Lexer(f.read())
   lex.scan()
   for i in lex.tokens:
      print(i)