from django.urls import path
from blogpost import views
from blogpost.views import (
    BlogPostUpdateView,
    BlogPostDeleteView,
    AddCommentView,
    AddLikeView,
    like_post,
)

app_name = "blogpost"

urlpatterns = [
    path("", views.BlogPostListView.as_view(), name="blogpost_list"),  # Список постов
    path(
        "blogpost/add/", views.BlogPostCreateView.as_view(), name="blogpost_create"
    ),  # Создание поста
    path(
        "blogpost/<int:pk>/", views.BlogPostDetailView.as_view(), name="blogpost_detail"
    ),  # Просмотр поста
    path(
        "blogpost/<int:pk>/edit/", BlogPostUpdateView.as_view(), name="blogpost_edit"
    ),  # Редактирование поста
    path(
        "blogpost/<int:pk>/delete/",
        BlogPostDeleteView.as_view(),
        name="blogpost_delete",
    ),  # Удаление поста
    path(
        "add_comment/<int:pk>/", AddCommentView.as_view(), name="add_comment"
    ),  # Добавление комментария
    path(
        "like/<str:model_type>/<int:pk>/", AddLikeView.as_view(), name="add_like"
    ),  # Добавление лайка
    path("like/<str:model_type>/<int:pk>/", like_post, name="like_post"),
]
