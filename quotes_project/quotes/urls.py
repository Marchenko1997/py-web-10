from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.quotes_view, name="quote_list"),
    path('authors/<int:author_id>', views.authors_view, name='author_detail'),
]
