from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.index, name="index"),
    path("authors/<int:pk>", views.author_detail, name="author_detail"),
    path("add-author/", views.add_author, name="add_author"),
    path("add-quote/", views.add_quote, name="add_quote"),
    path("tag/<str:tag_name>", views.quotes_by_tag, name="quotes_by_tag"),
]
