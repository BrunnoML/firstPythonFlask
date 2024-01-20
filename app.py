# Importação
# Pode apresentar problema na importação do flask, então procura a versão do python digitando pip --version e corrige o PATH para a versão informada no terminal

from flask import Flask, request, jasonify
from flask_sqlalchemy import SQLAlchemy
# Instanciar o aplicativo do Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecomemerce.dp'

# Começar a utilizar o nosso banco de dados

db = SQLAlchemy(app)


# Modelagem
# Produto (id, name, price, description)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

# Sinalização da rota do API, modelo e operação

@app.route('/api/products/add', methods=["POST"])
def add_product():
    if 'name' in data and 'price' in data: # Condição prévia para saber se os dados obrigatórios estão presentes para poder ser realizado o cadastro, se um deles não estiver presente o produto não será cadastrado
        data = request.json # armazena os dados fornecidos pelo cliente
        product = Product(name=data["name"], price=data["price"], description=data.get("description", "")) # cadastra produto, na descrição foi utilizado o método get e pedimos ao py para procurar a chave description, caso não encontre, usará o valor entre as aspas, neste caso, vazio

    # adicionar o produto ao banco de dados e comitar para confirmar o registro do produto
        db.session.add(product)
        db.session.commit()
        return jasonify({"message": "Product added sucessfully"})
    return jasonify({"message": "Invalid product data"}), 400 # Caso os dados sejam inválidos será apresentada essa mensagem e o número do erro precisa ser declarado, diferente se os dados forem válidos, em que o número 200 é apresentado sem precisar declarar
    

# Definir uma rota raiz (página inicial) e a função que será executada ao requisitar

@app.route('/')
def hello_world():
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True)

