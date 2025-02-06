# clients/urls.py
from django.urls import path
from .views import (
    ClientListView,
    ClientDetailView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
)

app_name = "clients"
urlpatterns = [
    path("", ClientListView.as_view(), name="client_list"),
    path("<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("create/", ClientCreateView.as_view(), name="client_create"),
    path("update/<int:pk>/", ClientUpdateView.as_view(), name="client_update"),
    path("delete/<int:pk>/", ClientDeleteView.as_view(), name="client_delete"),
]
