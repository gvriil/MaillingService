from django import forms
from .models import Comment, BlogPost


class StyleFormMixin:
    """Миксин для стилизации форм с помощью CSS классов."""

    def __init__(self, *args, **kwargs):
        """Инициализация миксина и добавление CSS классов к полям формы."""
        super(StyleFormMixin, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class CommentForm(forms.ModelForm):
    """Форма для создания комментария."""

    class Meta:
        model = Comment
        fields = ["text"]


class BlogPostForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания или редактирования блог-поста."""

    class Meta:
        model = BlogPost
        fields = ["title", "content", "preview", "is_published", "owner"]


class ContactForm(forms.Form):
    """Форма для отправки сообщения через контактную форму."""

    name = forms.CharField(label="Your Name", max_length=100)
    email = forms.EmailField(label="Your Email")
    message = forms.CharField(label="Your Message", widget=forms.Textarea)
