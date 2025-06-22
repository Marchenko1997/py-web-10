from django.shortcuts import render
from .models import Quote, Author

def quotes_view(request):
    quotes = Quote.objects.select_related('author').all()
    return render(request, 'quotes/quotes.html', {'quotes': quotes})


def authors_view(request, author_id):
    author = Author.objects.get(pk=author_id)
    return render(request, "quotes/author_detail.html", {"author": author})
