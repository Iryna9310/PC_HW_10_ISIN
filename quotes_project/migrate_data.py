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
    if created:
        print(f"Author {author.fullname} created.")
    else:
        print(f"Author {author.fullname} already exists.")

# Міграція цитат
print("Starting quotes migration...")
for mongo_quote in mongo_quotes.find():
    print(f"Processing quote: {mongo_quote}")
    author_name = mongo_quote['author']
    try:
        author = Author.objects.get(fullname=author_name)
        quote, created = Quote.objects.get_or_create(
            quote=mongo_quote['quote'],
            author=author,
            defaults={'tags': mongo_quote['tags']}
        )
        if created:
            print(f"Quote created: {quote.quote}")
        else:
            print(f"Quote already exists: {quote.quote}")
    except Author.DoesNotExist:
        print(f"Author {author_name} does not exist. Quote not created: {mongo_quote['quote']}")
print("Migration completed.")