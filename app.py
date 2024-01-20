# Version 01 - Working add delete and get

# Importação
# Pode apresentar problema na importação do flask, então procura a versão do python digitando pip --version e corrige o PATH para a versão informada no terminal
# BUG001 Houve um problema na importação do jsonify, pois ao digitar no código ficou errado, ou seja, com a vogal "a" jasonify, substituir todas as linhas resolve o problema
from flask import Flask, request, jsonify
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


@app.route('/api/products/add', methods=["POST"]) # Sinalização da rota do API, modelo e operação
def add_product():
    data = request.json 
    if 'name' in data and 'price' in data: # Condição prévia para saber se os dados obrigatórios estão presentes para poder ser realizado o cadastro, se um deles não estiver presente o produto não será cadastrado
        product = Product(name=data["name"], price=data["price"], description=data.get("description", "")) # Cadastra produto, na descrição foi utilizado o método get e pedimos ao py para procurar a chave description, caso não encontre, usará o valor entre as aspas, neste caso, vazio
        db.session.add(product) # Adicionar o produto ao banco de dados e comitar para confirmar o registro do produto
        db.session.commit()
        return jsonify({"message": "Product added sucessfully"})
    return jsonify({"message": "Invalid product data"}), 400 # Caso os dados sejam inválidos será apresentada essa mensagem e o número do erro precisa ser declarado, diferente se os dados forem válidos, em que o número 200 é apresentado sem precisar declarar

# Criar rota de delete utilizando <> para inserir o parâmetro, no caso inteiro e usar o método DELETE
@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
# Criar a função para deletar o produto
def delete_product(product_id):
    # Recuperar o produto da base de dados
    # Verificar se o produto existe
    # Se existe, apagar da base de dados
    # Se não existe, retornar com o código 404 "not found"
    # Usar a propriedade query e o método get
    product = Product.query.get(product_id)
    # Se utilizasse o if product_id != None: já seria suficiente, informando que se o produto escolhido fosse válido, ou seja, diferente de None poderia seguir, mas o py já entende colocando apenas if product:
    if product: 
        db.session.delete(product)
        db.session.commit()
        # Agora acrescentar as mensagens para as condições, se deletou ou se o produto não foi encontrado com o cod msg 404
        return jsonify({"message": "Product deleted sucessfully"})
    return jsonify({"message": "Product not found"}), 404

@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product: 
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
            })
    return jsonify({"message": "Product not found"}), 404
    
# Atualizar o produto
@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product: 
        return jsonify({"message": "Product not found"}), 404
    
    data = request.json
    if 'name' in data:
        product.name = data['name']

    if 'price' in data:
        product.price = data['price']

    if 'description' in data:
        product.description = data['description']
    db.session.commit()
    return jsonify({"message": "Product updated sucessfully"})

# Definir uma rota raiz (página inicial) e a função que será executada ao requisitar

@app.route('/')
def hello_world():
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True)

