from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Author, Quote
from .forms import AuthorForm, QuoteForm


def index(request):
    quotes = Quote.objects.all().order_by("author__fullname", "text")
    return render(request, "quotes/index.html", {"quotes": quotes})


@login_required
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("quotes:index")
    else:
        form = AuthorForm()
    return render(request, "quotes/add_author.html", {"form": form})


@login_required
def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect("quotes:index")
    else:
        form = QuoteForm()
    return render(request, "quotes/add_quote.html", {"form": form})


def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, "quotes/author_detail.html", {"author": author})


def quotes_by_tag(request, tag_name):
    quotes = Quote.objects.filter(tags__name__iexact=tag_name)
    return render(
        request, "quotes/quotes_by_tag.html", {"quotes": quotes, "tag": tag_name}
    )
