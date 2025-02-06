import os

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from slugify import slugify
from blogpost.forms import BlogPostForm, CommentForm
from blogpost.models import BlogPost, Comment
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from mailings.views import OwnerRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.cache import cache

class BlogPostListView(PermissionRequiredMixin, ListView):
    permission_required = 'view_blogpost'
    model = BlogPost
    template_name = "blogpost/blogpost_list.html"
    context_object_name = "blogposts"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        cache_key = 'blogpost_list_{}'.format(self.request.user.is_authenticated)
        cached_queryset = cache.get(cache_key)
        if cached_queryset:
            return cached_queryset

        if self.request.user.is_authenticated:
            if "drafts" in self.request.GET:
                queryset = queryset.filter(owner=self.request.user, is_published=False)
            elif "published" in self.request.GET:
                queryset = queryset.filter(is_published=True)
            else:
                queryset = queryset.filter(is_published=True)
        else:
            queryset = queryset.filter(is_published=True)

        cache.set(cache_key, queryset, 60 * 15)  # Кэшировать на 15 минут
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["drafts"] = BlogPost.objects.filter(
                owner=self.request.user, is_published=False
            )
            context["published"] = BlogPost.objects.filter(is_published=True)
        return context



class BlogPostDetailView(DetailView):
    """
    Представление для отображения деталей поста.
    """

    model = BlogPost
    template_name = "blogpost/blogpost_detail.html"

    def get_object(self, queryset=None):
        """
        Возвращает объект поста и увеличивает счетчик просмотров.

        Args:
            queryset: Запрос для получения объекта.

        Returns:
            BlogPost: Объект поста.
        """
        obj = super().get_object(queryset)
        cache_key = 'blogpost_detail_{}'.format(obj.pk)
        cached_obj = cache.get(cache_key)
        if cached_obj:
            return cached_obj

        if self.request.user.is_authenticated:
            obj.views_count += 1
            obj.save()
            if obj.views_count == 100:
                send_mail(
                    "Поздравление с достижением!",
                    'Статья "{}" достигла 100 просмотров.'.format(obj.title),
                    settings.DEFAULT_FROM_EMAIL,
                    ["your_email@yandex.ru"],
                    fail_silently=False,
                )

        cache.set(cache_key, obj, 60 * 15)  # Кэшировать на 15 минут
        return obj

    def get_context_data(self, **kwargs):
        """
        Добавляет автора поста в контекст.

        Returns:
            dict: Контекст для шаблона.
        """
        context = super().get_context_data(**kwargs)
        context["author"] = self.object.owner
        return context


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания нового поста.
    """

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blogpost/blogpost_form.html"
    success_url = reverse_lazy("blogpost:blogpost_list")

    def form_valid(self, form):
        """
        Устанавливает владельца поста и генерирует slug перед сохранением.

        Args:
            form: Форма с данными поста.

        Returns:
            HttpResponse: Ответ после успешного сохранения формы.
        """
        form.instance.slug = slugify(form.instance.title)
        form.instance.owner = self.request.user
        return super().form_valid(form)

class BlogPostUpdateView(OwnerRequiredMixin, UpdateView):
    """
    Представление для обновления существующего поста.
    """

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blogpost/blogpost_form.html"

    def get_success_url(self):
        """
        Возвращает URL для перенаправления после успешного обновления поста.

        Returns:
            str: URL для перенаправления.
        """
        return reverse("blogpost:blogpost_detail", kwargs={"pk": self.object.pk})

class BlogPostDeleteView(OwnerRequiredMixin, DeleteView):
    """
    Представление для удаления поста.
    """

    model = BlogPost
    template_name = "blogpost/blogpost_confirm_delete.html"
    success_url = reverse_lazy("blogpost:blogpost_list")

    def delete(self, request, *args, **kwargs):
        """
        Удаляет пост и связанные с ним файлы.

        Args:
            request: HTTP запрос.

        Returns:
            HttpResponse: Ответ после успешного удаления поста.
        """
        self.object = self.get_object()
        # Удаление связанных файлов
        if self.object.image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(self.object.image))
            if os.path.exists(image_path):
                os.remove(image_path)
        # Удаление других связанных файлов, если есть
        # Например, если у вас есть поле для дополнительных файлов
        # if self.object.additional_files:
        #     for file in self.object.additional_files.all():
        #         file_path = os.path.join(settings.MEDIA_ROOT, str(file.file))
        #         if os.path.exists(file_path):
        #             os.remove(file_path)
        return super().delete(request, *args, **kwargs)

class AddCommentView(LoginRequiredMixin, CreateView):
    """
    Представление для добавления комментария к посту.
    """

    model = Comment
    form_class = CommentForm
    template_name = "blogpost/add_comment.html"

    def form_valid(self, form):
        """
        Устанавливает пост и автора комментария перед сохранением.

        Args:
            form: Форма с данными комментария.

        Returns:
            HttpResponse: Ответ после успешного сохранения формы.
        """
        form.instance.blogpost_id = self.kwargs["pk"]
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """
        Возвращает URL для перенаправления после успешного добавления комментария.

        Returns:
            str: URL для перенаправления.
        """
        return reverse_lazy(
            "blogpost:blogpost_detail", kwargs={"pk": self.kwargs["pk"]}
        )

class AddLikeView(LoginRequiredMixin, View):
    """
    Представление для добавления или удаления лайка к посту или комментарию.
    """

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает запрос на добавление или удаление лайка.

        Args:
            request: HTTP запрос.

        Returns:
            JsonResponse: Ответ с информацией о лайке и количестве лайков.
        """
        return handle_like(request, self.kwargs.get("model_type"), self.kwargs.get("pk"))


def handle_like(request, model_type, pk):
    """
    Обрабатывает добавление или удаление лайка к посту или комментарию.

    Args:
        request: HTTP запрос.
        model_type (str): Тип модели ('post' или 'comment').
        pk (str): Первичный ключ объекта.

    Returns:
        JsonResponse: Ответ с информацией о лайке и количестве лайков.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=403)

    if model_type == "post":
        obj = BlogPost.objects.get(pk=pk)
    elif model_type == "comment":
        obj = Comment.objects.get(pk=pk)
    else:
        return JsonResponse({"error": "Invalid model type"}, status=400)

    if request.user in obj.likes.all():
        obj.likes.remove(request.user)
        liked = False
    else:
        obj.likes.add(request.user)
        liked = True

    return JsonResponse({"liked": liked, "likes_count": obj.likes.count()})

@csrf_exempt
@require_POST
def like_post(request, model_type, pk):
    """
    Обрабатывает запрос на добавление или удаление лайка к посту или комментарию.

    Args:
        request: HTTP запрос.
        model_type (str): Тип модели ('post' или 'comment').
        pk (str): Первичный ключ объекта.

    Returns:
        JsonResponse: Ответ с информацией о лайке и количестве лайков.
    """
    return handle_like(request, model_type, pk)

class OwnerRequiredMixin(UserPassesTestMixin):
    """
    Миксин для проверки прав владельца объекта.
    """

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.is_staff