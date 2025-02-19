class Product: #Clase producto con nombre, precio y cantidad
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def toDB(self): #En formato JSON para la insercion a la bd
         return {'name':self.name,'price':self.price,'quantity':self.quantity}