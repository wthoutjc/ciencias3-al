# PL/0 Analizador Léxico
# Construido por:
# - Juan Camilo Ramírez Rátiva - 20181020089
# -
# Universidad Distrital Francisco José de Caldas
# Ciencias de la Computación III - Bogotá D.C.
'''

 Este proyecto esta basado en diversas fuentes:

 - Esencia del PL/0: 
    1. https://www.youtube.com/watch?v=gWrmCOTrtrs
    2. https://www.youtube.com/watch?v=WkMOyY6QeWg&t=4s
    3. https://www.youtube.com/watch?v=9wm16XZc9dQ
    4. http://repositori.uji.es/xmlui/bitstream/handle/10234/5877/lexico.apun.pdf?sequence=1&isAllowed=y
 - Pl/0 resources: 
    1. https://github.com/zhuorantan/PL0
    2. https://www.dabeaz.com/ply/
    3. https://www.lawebdelprogramador.com/codigo/C-Visual-C/1513-Analizador-lexico-y-sintactico-para-el-lenguaje-pl0.html

 Informese más sobre la gramática Pl/0 en el documento PDF en el github o en el readme.md
'''
# Librerias
# Flask: Microframework encargado de enviar los JSON al front
from flask import Flask, request, render_template, jsonify, make_response
import json
# Lex
import ply.lex as lex

app = Flask(__name__)

# Palabras reservadas
reservadas = [
    'BEGIN','END','IF','THEN','WHILE','DO','CALL','CONST',
	'VAR','PROCEDURE','OUT','IN','ELSE'
]

# Tokens: 
tokens = reservadas + [
    'ID','NUMBER','PLUS','MINUS','TIMES','DIVIDE',
		'ODD','ASSIGN','NE','LT','LTE','GT','GTE',
		'LPARENT', 'RPARENT','COMMA','SEMMICOLOM',
		'DOT','UPDATE'
		]

t_ignore = '\t '
# Expresiones regulares para PL/0: https://en.wikipedia.org/wiki/PL/0
# SUMA RESTA
t_PLUS = r'\+'
t_MINUS = r'\-'
# Multiplicar, dividir
t_TIMES = r'\*'
t_DIVIDE = r'/'
# Asignar
t_ASSIGN = r'='
# Inecuaciones
t_ODD = r'ODD'
t_NE = r'<>'
t_LT = r'<'
t_LTE = r'<='
t_GT = r'>'
t_GTE = r'>='
# ( ) , ; . :=
t_LPARENT = r'\('
t_RPARENT = r'\)'
t_COMMA = r','
t_SEMMICOLOM = r';'
t_DOT = r'\.'
t_UPDATE = r':='

# Ocupamos una expresion regular mas avanzada:
'''
Función para el token ID
    Entrada: t TOKEN
'''
# Puede contener a-z A-Z ó _ y seguido de a-z A-Z 0-9 _
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.upper() in reservadas:
        t.value = t.value.upper()
        t.type = t.value
    return t

'''
Función para detectar los saltos de linea
    Entrada: t TOKEN
'''
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

'''
Función para el token COMMENT
    Entrada: t TOKEN
'''
# Comienza por # seguido de cualquier caracter excepto un salto de linea \n
def t_COMMENT(t):
    r'\#.*'
    pass

'''
Función para el token NUMBER
    Entrada: t TOKEN
'''
# Reconoce cualquier digito decimal 
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

'''
Función para imprimir errores si un TOKEN es invalido
    Entrada: t TOKEN
'''
# Función vital para PL/0
def t_error(t):
    return "Token ilegal en la línea {:4} valor: {:16} posición {:4}".format(str(t.lineno), str(t.value), str(t.lexpos))
    t.lexer.skip(1)

def analyze_lex(text):
    analize = lex.lex()
    analize.input(text)
    output = []
    while True:
        tok = analize.token()
        if not tok: break
        status = "Line {:4} Type: {:16} Value: {:16} Position: {:4}".format(str(tok.lineno), str(tok.type), str(tok.value), str(tok.lexpos))
        output.append(status)
    return output

@app.route("/")
def main():
    '''
    Cargamos el index.html que es donde se almacena
    los recursos visuales de la aplicación
    '''
    return render_template("index.html")

@app.route("/process-text", methods=["POST"])
def process_text():
    '''
    Ejecutamos el analizador léxico
    '''
    data = request.data
    s_data = data.decode("utf-8")
    json_data = json.loads(s_data)
    text = str(json_data['text'])

    output = analyze_lex(text)

    res = make_response(jsonify({"results": output}), 200)
    return res

if __name__ == '__main__':
    app.run(debug = True)