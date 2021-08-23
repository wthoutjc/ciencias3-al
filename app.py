# JAVA Analizador Léxico
# Construido por:
# - Juan Camilo Ramírez Rátiva - 20181020089
# -
# Universidad Distrital Francisco José de Caldas
# Ciencias de la Computación III - Bogotá D.C.

# Librerias
# Flask: Microframework encargado de enviar los JSON al front
from flask import Flask, request, render_template, jsonify, make_response
import json
# Libreria: autoria propia
from lexer.lexer import Lexer

app = Flask(__name__)

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

    output = []

    with open('lexer/Test.txt','w') as f:
        f.write(text)
        f.close()
    with open('lexer/Test.txt','r') as f:  
        lex = Lexer(f.read())
        lex.scan()
        for i in lex.tokens:
            output.append(str(i))
        f.close()
    res = make_response(jsonify({"results": output}), 200)
    return res

if __name__ == '__main__':
    app.run(debug = True)