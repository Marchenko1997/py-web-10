from django import forms
from .models import Author, Quote, Tag


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]


class QuoteForm(forms.ModelForm):
    tags = forms.CharField(
        max_length=255, required=False, help_text="Введите теги через запятую"
    )

    class Meta:
        model = Quote
        fields = ["text", "author", "tags"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
        self.fields["author"].queryset = Author.objects.order_by("fullname")

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.user = user
        if commit:
            instance.save()

        tags_str = self.cleaned_data.get("tags", "")
        tags_list = [tag.strip() for tag in tags_str.split(",") if tag.strip()]
        for tag_name in tags_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            instance.tags.add(tag)

        return instance
