import os
import django
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId


load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes_site.settings")
django.setup()

from quotes.models import Author, Quote
from django.contrib.auth.models import User


mongo_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongo_uri)
db = client["quotes_db"]


def import_authors():
    authors = db.author.find()
    for author in authors:
        if not Author.objects.filter(fullname=author["fullname"]).exists():
            Author.objects.create(
                fullname=author["fullname"],
                born_date=author["born_date"],
                born_location=author["born_location"],
                description=author["description"],
            )
    print("✅ Авторы импортированы.")


def import_quotes():
    default_user, _ = User.objects.get_or_create(username="imported_user")
    quotes = db.quote.find()
    for q in quotes:
        author_id = q["author"]
        mongo_author = db.author.find_one({"_id": ObjectId(author_id)})

        if not mongo_author:
            print(f"⚠️ Автор не найден в MongoDB: {author_id}")
            continue

        try:
            author = Author.objects.get(fullname=mongo_author["fullname"])
        except Author.DoesNotExist:
            print(f"⚠️ Автор не найден в PostgreSQL: {mongo_author['fullname']}")
            continue

        if not Quote.objects.filter(text=q["quote"]).exists():
            Quote.objects.create(
                text=q["quote"],
                author=author,
                tags=",".join(q["tags"]),
                user=default_user,
            )
    print("✅ Цитаты импортированы.")


if __name__ == "__main__":
    import_authors()
    import_quotes()
