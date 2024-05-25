import os
import django
from pymongo import MongoClient

# Налаштування Django
print("Setting up Django...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes_project.settings')
django.setup()
print("Django setup complete.")

from quotes.models import Author, Quote

# Підключення до MongoDB
print("Connecting to MongoDB...")
client = MongoClient("mongodb+srv://IrynaIra:LG152367@cluster0.ct1p0gg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
mongo_db = client['my_database']
print("MongoDB connection established.")
print("Available collections:", mongo_db.list_collection_names())

# Перевірка даних у колекціях
print("Checking if authors collection exists...")
if 'author' in mongo_db.list_collection_names():
    print("Authors collection exists.")
else:
    print("Authors collection does NOT exist.")

print("Checking if quotes collection exists...")
if 'quote' in mongo_db.list_collection_names():
    print("Quotes collection exists.")
else:
    print("Quotes collection does NOT exist.")

mongo_authors = mongo_db['author']
mongo_quotes = mongo_db['quote']

# Перевірка кількості записів
print(f"Number of authors in MongoDB: {mongo_authors.count_documents({})}")
print(f"Number of quotes in MongoDB: {mongo_quotes.count_documents({})}")

# Створюємо словник для відображення ідентифікаторів авторів MongoDB на Django
author_id_map = {}

# Міграція авторів
print("Starting authors migration...")
for mongo_author in mongo_authors.find():
    print(f"Processing author: {mongo_author}")
    author, created = Author.objects.get_or_create(
        fullname=mongo_author['fullname'],
        defaults={
            'born_date': mongo_author['born_date'],
            'born_location': mongo_author['born_location'],
            'description': mongo_author['description']
        }
    )
    author_id_map[str(mongo_author['_id'])] = author.id  # Зберігаємо відображення ідентифікаторів авторів

# Міграція цитат
print("Starting quotes migration...")
for mongo_quote in mongo_quotes.find():
    print(f"Processing quote: {mongo_quote}")
    author_id = author_id_map.get(str(mongo_quote['author']))  # Отримуємо відповідний ідентифікатор автора зі словника
    if author_id:
        quote_text = mongo_quote['quote']
        if author_id:
            author = Author.objects.get(id=author_id)
            quote_text = f'"{quote_text}" - {author.fullname}'
        else:
            quote_text = f'"{quote_text}" - Author unknown'
        
        quote, created = Quote.objects.get_or_create(
            quote=quote_text,
            author_id=author_id
        )
        if created:
            print(f"Quote created: {quote.quote}")
    else:
        print("Author not found. Quote not migrated.")

print("Migration completed.")