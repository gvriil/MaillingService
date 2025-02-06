from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Client
from .forms import ClientForm


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "clients/client_list.html"
    context_object_name = "clients"
    paginate_by = 10

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "clients/client_detail.html"


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_create.html"

    def get_success_url(self):
        return reverse_lazy("clients:client_detail", kwargs={"pk": str(self.object.pk)})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/client_update.html"

    def get_success_url(self):
        return reverse_lazy("clients:client_detail", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise PermissionDenied("У вас нет прав для редактирования этого клиента.")
        return obj


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = "clients/client_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("clients:client_list")
