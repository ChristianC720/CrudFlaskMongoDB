from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import database as dbase #Se importa la conexion a la bd desde database.py
from product import Product #Se importa la clase desde product.py

db = dbase.dbConnect() #Conexión a la BD y objeto que contiene las colecciones etc.

app = Flask (__name__)

# Pagina principal del CRUD
@app.route("/")
def index():
    products = db['products'] #productos es igual a la colección products dentro de la bd
    productsReceived= products.find() #Recibe los productos para mostrar
    return render_template("index.html", products = productsReceived) #Una template de jinga donde se pueden ver, insertar, editar y eliminar productos


# METODO POST para Insertar
@app.route("/products", methods=['POST'])
def addProduct():
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']

    if name and price and quantity:
        product = Product(name, price, quantity)
        products.insert_one(product.toDB()) #Se realiza una insercion a la bd
        response = jsonify( #FORMATO DE LOS PRODUCTOS COMO JSON
            { 
            'name' : name,
            'price' : price,
            'quantity' : quantity
            }
        )
        return redirect(url_for('index')) #Te regresa al index
    else:
        return notFound()   #En caso de fallar, te manda a un 404


# METODO DELETE para Eliminar
@app.route("/delete/<string:product_name>")
def delProduct(product_name):
    products = db['products']
    products.delete_one({'name' : product_name}) #Se elimina el producto con el nombre correcto
    return redirect(url_for('index'))


# METODO PUT para Editar
@app.route("/edit/<string:product_name>", methods=['POST'])
def editProduct(product_name):
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']


    if name and price and quantity:
        products.update_one(
            {'name': product_name},  # Filtro para encontrar el documento
            {'$set': {'name': name, 'price': price, 'quantity': quantity}}  # Datos a actualizar
)
        response = jsonify({'message' :'producto ' + product_name + ' actualizado correctamente'})
        return redirect(url_for('index'))
    else:
        return notFound()


#ERROR 404 EN CASO DE FALLO
@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message' :'No encontrado, error: ' + request.url,
        'status' : '404 NOT FOUND'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

#Debug mode, para correrlo así, en vez de utilizar flask run, utiliza py -m app
if __name__ == "__main__":
    app.run(debug=True, port=8080)