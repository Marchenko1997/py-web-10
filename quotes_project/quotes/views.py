from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Author, Quote, Tag
from .forms import AuthorForm, QuoteForm
from django.db.models import Count
from django.core.paginator import Paginator
from .utils.scraper import scrape_quotes


def index(request):
    quotes = Quote.objects.all().order_by("author__fullname", "text")

    paginator = Paginator(quotes, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    top_tags = Tag.objects.annotate(num_quotes= Count("quote")).order_by("-num_quotes")[:10]

    return render(request, "quotes/index.html", {"page_obj": page_obj, "top_tags": top_tags})


@login_required
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Автор успешно добавлен!")
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
            messages.success(request, "Цитата успешно добавлена!")
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


def run_scraper(request):
    if request.method == "POST":
        scrape_quotes()
        messages.success(request, "Скрапинг завершён и цитаты добавлены!")
    return redirect("quotes:index")
