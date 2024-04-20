from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient
from bson import ObjectId  # Importation correcte
from typing import List
import uuid  # Pour générer des identifiants uniques si nécessaire

# Modèle pour les produits
class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))  # Correction de l'importation
    name: str
    price: float

    class Config:
        # Autorise l'utilisation de noms de champ personnalisés
        allow_population_by_field_name = True
        # Permet l'utilisation de types arbitraires comme ObjectId
        arbitrary_types_allowed = True
        # Définit comment encoder ObjectId pour JSON
        json_encoders = {ObjectId: str}

# Configuration de la connexion à MongoDB
client = MongoClient("mongodb://revtech-mongodb-1:27017")
db = client["product_db"]
collection = db["products"]

app = FastAPI()

# Obtenir tous les produits
@app.get("/products/", response_model=List[Product])
def get_products():
    products = list(collection.find())
    return products

# Obtenir un produit par ID
@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: str):
    product = collection.find_one({"_id": ObjectId(product_id)})  # Correction ici aussi
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Créer un produit
@app.post("/products/", response_model=Product)
def create_product(product: Product):
    product_dict = product.dict(by_alias=True)
    collection.insert_one(product_dict)
    return product

# Mettre à jour un produit
@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: str, product: Product):
    if not collection.find_one({"_id": ObjectId(product_id)}):
        raise HTTPException(status_code=404, detail="Product not found")

    collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": product.dict(by_alias=True, exclude={"id"})},
    )
    return collection.find_one({"_id": ObjectId(product_id)})

# Supprimer un produit
@app.delete("/products/{product_id}")
def delete_product(product_id: str):
    if not collection.find_one({"_id": ObjectId(product_id)}):
        raise HTTPException(status_code=404, detail="Product not found")

    collection.delete_one({"_id": ObjectId(product_id)})
    return {"message": "Product deleted successfully"}
