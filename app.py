# Importação
# Pode apresentar problema na importação do flask, então procura a versão do python digitando pip --version e corrige o PATH para a versão informada no terminal

from flask import Flask

# Instanciar o aplicativo do Flask

app = Flask(__name__)


# Definir uma rota raiz (página inicial) e a função que será executada ao requisitar

@app.route('/')
def hello_world():
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True)
    
