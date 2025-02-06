from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = "mailings"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path(
        "mailings/", cache_page(1)(views.MailingListView.as_view()), name="mailing_list"
    ),
    path("add/", views.MailingCreateView.as_view(), name="mailing_add"),
    path("<int:pk>/", views.MailingDetailView.as_view(), name="mailing_detail"),
    path("<int:pk>/update/", views.MailingUpdateView.as_view(), name="mailing_update"),
    path("<int:pk>/delete/", views.MailingDeleteView.as_view(), name="mailing_delete"),
    path("activate/<int:pk>/", views.activate, name="activate"),
    path("mailing/<int:pk>/deactivate/", views.deactivate, name="deactivate"),
    path("send_mail/<int:client_pk>/", views.send_single_mail, name="send_mail"),
    path("send_bulk_mail/<int:pk>/", views.send_bulk_mail, name="send_bulk_mail"),
    path("attempts/", views.AttemptListView.as_view(), name="attempt_list"),
]
