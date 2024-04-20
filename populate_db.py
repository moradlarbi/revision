import random
from faker import Faker
from pymongo import MongoClient
from pydantic import BaseModel, Field, ValidationError

# Utilisation de faker pour générer des données fictives
fake = Faker()

# Modèle de produit avec validation du prix
class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(random.randint(10000, 99999)))  # Identifiant aléatoire
    name: str
    price: float = Field(ge=10, le=1000)  # Prix doit être entre 10 et 1000

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017")  # Assurez-vous que l'URL est correcte
db = client["product_db"]
collection = db["products"]

# Génération et insertion des données
def populate_products(n):
    for _ in range(n):
        product = {
            "name": fake.word(),  # Nom de produit fictif
            "price": random.uniform(10, 1000),  # Prix entre 10 et 1000
        }

        # Validation du produit
        try:
            validated_product = Product(**product)
            collection.insert_one(validated_product.dict())
            print(f"Product added: {validated_product}")
        except ValidationError as e:
            print(f"Validation error: {e}")

# Nombre de produits à ajouter
populate_products(10)  # Ajouter 10 produits
