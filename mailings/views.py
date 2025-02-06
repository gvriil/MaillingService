from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from clients.models import Client
from .models import Mailing, Attempt
from .forms import MailingForm
from .services import send_mail
from django.core.cache import cache


def home(request):
    """
    Отображает главную страницу с общими статистиками по рассылкам и клиентам.
    """
    cache_key = 'home_stats'
    cached_data = cache.get(cache_key)
    if cached_data:
        return render(request, "mailings/home.html", cached_data)

    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status="running").count()
    unique_clients = Client.objects.values("email").distinct().count()
    context = {
        "total_mailings": total_mailings,
        "active_mailings": active_mailings,
        "unique_clients": unique_clients,
    }
    cache.set(cache_key, context, 60 * 15)  # Кэшировать на 15 минут
    return render(request, "mailings/home.html", context)


class HomeView(LoginRequiredMixin, ListView):
    """
    Отображает главную страницу с общими статистиками по рассылкам и клиентам.
    """
    model = Mailing
    template_name = "mailings/home.html"
    context_object_name = "mailings"
    paginate_by = 10
    login_url = '/users/login/'  # URL страницы логина
    redirect_field_name = 'next'  # Название поля, в которое будет сохранён URL текущей страницы

    def get_queryset(self):
        """
        Возвращает список рассылок в зависимости от роли пользователя.
        """
        cache_key = f'home_view_queryset_{self.request.user.id}'
        cached_queryset = cache.get(cache_key)
        if cached_queryset:
            return cached_queryset

        if self.request.user.is_staff:
            queryset = Mailing.objects.all()
        elif self.request.user.is_authenticated:
            queryset = Mailing.objects.filter(owner=self.request.user)
        else:
            queryset = Mailing.objects.none()

        cache.set(cache_key, queryset, 60 * 15)  # Кэшировать на 15 минут
        return queryset

    def get_context_data(self, **kwargs):
        """
        Добавляет контекстные данные для шаблона.
        """
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["drafts"] = Mailing.objects.filter(
                owner=self.request.user, status="created"
            )
        return context




class OwnerRequiredMixin(UserPassesTestMixin):
    """
    Миксин для проверки, что текущий пользователь является владельцем объекта или администратором.
    """

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.is_staff


class MailingListView(ListView):
    """
    Отображает список рассылок.
    """

    model = Mailing
    template_name = "mailings/mailing_list.html"
    context_object_name = "mailings"
    paginate_by = 10

    def get_queryset(self):
        """
        Возвращает список рассылок в зависимости от роли пользователя.
        """
        cache_key = f'mailing_list_view_queryset_{self.request.user.id}'
        cached_queryset = cache.get(cache_key)
        if cached_queryset:
            return cached_queryset

        if self.request.user.is_staff:
            queryset = Mailing.objects.all()
        elif self.request.user.is_authenticated:
            queryset = Mailing.objects.filter(owner=self.request.user)
        else:
            queryset = Mailing.objects.none()

        cache.set(cache_key, queryset, 60 * 15)  # Кэшировать на 15 минут
        return queryset

    def get_context_data(self, **kwargs):
        """
        Добавляет контекстные данные для шаблона.
        """
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["drafts"] = Mailing.objects.filter(
                owner=self.request.user, status="created"
            )
        return context



class MailingDetailView(DetailView):
    """
    Отображает детали конкретной рассылки.
    """

    model = Mailing
    template_name = "mailings/mailing_detail.html"
    context_object_name = "mailing"

    def get_object(self, queryset=None):
        """
        Возвращает объект рассылки.
        """
        cache_key = f'mailing_detail_view_object_{self.kwargs["pk"]}'
        cached_object = cache.get(cache_key)
        if cached_object:
            return cached_object

        obj = super().get_object(queryset)
        cache.set(cache_key, obj, 60 * 15)  # Кэшировать на 15 минут
        return obj



class MailingCreateView(LoginRequiredMixin, CreateView):
    """
    Создает новую рассылку.
    """

    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def form_valid(self, form):
        """
        Устанавливает текущего пользователя как владельца рассылки перед сохранением.
        """
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        """
        Добавляет текущего пользователя в аргументы формы.
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingUpdateView(OwnerRequiredMixin, UpdateView):
    """
    Обновляет существующую рассылку.
    """

    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_form_kwargs(self):
        """
        Добавляет текущего пользователя в аргументы формы.
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingDeleteView(OwnerRequiredMixin, DeleteView):
    """
    Удаляет рассылку.
    """

    model = Mailing
    template_name = "mailings/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailing_list")


def activate(request, pk):
    """
    Активирует рассылку.
    """
    mailing = get_object_or_404(Mailing, pk=pk)
    mailing.status = "running"
    mailing.save()
    messages.success(request, "Рассылка успешно активирована.")
    return redirect("mailings:mailing_list")


def deactivate(request, pk):
    """
    Деактивирует рассылку.
    """
    mailing = get_object_or_404(Mailing, pk=pk)
    mailing.status = "created"
    mailing.save()
    messages.success(request, "Рассылка успешно деактивирована.")
    return redirect("mailings:mailing_list")


def send_single_mail(request, client_pk):
    """
    Отправляет единичное письмо клиенту.
    """
    client = get_object_or_404(Client, pk=client_pk)
    success, response = send_mail(
        subject="Тестовое сообщение",
        body="Это тестовое письмо",
        recipient_list=[client.email],
        request_user=request.user,
    )

    if success:
        messages.success(request, response)
    else:
        messages.error(request, response)

    return redirect("clients:client_list")


def send_bulk_mail(request, pk):
    """
    Отправляет сообщение списку клиентов.
    """
    mailing = get_object_or_404(Mailing, pk=pk)
    recipient_list = [client.email for client in mailing.clients.all()]
    success, response = send_mail(
        subject=mailing.message.subject,
        body=mailing.message.body,
        recipient_list=recipient_list,
        request_user=request.user,
        mailing=mailing,
    )

    if success:
        messages.success(request, response)
    else:
        messages.error(request, response)

    return redirect("mailings:mailing_detail", pk=pk)


class AttemptListView(ListView):
    """
    Отображает список попыток отправки.
    """

    model = Attempt
    template_name = "mailings/attempt_list.html"
    context_object_name = "attempts"
    paginate_by = 10

    def get_queryset(self):
        """
        Возвращает список попыток отправки для текущего пользователя.
        """
        if self.request.user.is_authenticated:
            return Attempt.objects.filter(owner=self.request.user)
        return Attempt.objects.none()

    def get_context_data(self, **kwargs):
        """
        Добавляет контекстные данные для шаблона.
        """
        context = super().get_context_data(**kwargs)
        context["total_attempts"] = Attempt.objects.count()
        context["successful_attempts"] = Attempt.objects.filter(
            status="success"
        ).count()
        context["failed_attempts"] = Attempt.objects.filter(status="failed").count()
        return context
