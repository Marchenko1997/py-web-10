import requests
from bs4 import BeautifulSoup
from ..models import Quote, Author, Tag


def scrape_quotes():
    url = "http://quotes.toscrape.com/page/1/"
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        for quote_block in soup.select(".quote"):
            text = quote_block.find("span", class_="text").text.strip()
            author_name = quote_block.find("small", class_="author").text.strip()
            tags = [t.text for t in quote_block.select(".tags .tag")]

            author, _ = Author.objects.get_or_create(
                fullname=author_name,
                defaults={
                    "born_date": "неизвестно",
                    "born_location": "неизвестно",
                    "description": "автор с сайта quotes.toscrape.com",
                },
            )

            quote, created = Quote.objects.get_or_create(
                text=text,
                author=author,
                defaults={
                    "user_id": 1
                },  
            )

            if created:
                for tag_name in tags:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    quote.tags.add(tag)

        next_btn = soup.select_one(".next a")
        url = "http://quotes.toscrape.com" + next_btn["href"] if next_btn else None

    print("Скрапинг завершён")
