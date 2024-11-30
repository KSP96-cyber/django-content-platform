from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Advent
from .forms import AdventForm
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect


# Class-Based View для отображения списка событий (Advent)
class AdventListView(ListView):
    model = Advent
    template_name = 'eventmanager/advent_list.html'  # Шаблон, который будет использоваться для рендеринга
    context_object_name = 'advents'  # Имя переменной в шаблоне
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Получаем стандартный контекст
        context['user'] = self.request.user  # Добавляем текущего пользователя
        return context  # Возвращаем обновленный контекст


# Class-Based View для создания нового события (Advent)
class AdventCreateView(LoginRequiredMixin,CreateView):
    model = Advent
    form_class = AdventForm
    template_name = 'eventmanager/create_advent.html'
    login_url = 'login'  # Перенаправляет на страницу логина, если пользователь не залогинен
    success_url = reverse_lazy('eventmanager:advent_list')  # Перенаправление на список событий после успешного создания

    def form_valid(self, form):
        form.instance.user = self.request.user  # Устанавливаем текущего пользователя
        form.instance.advent_view_count = 1  # Устанавливаем значение по умолчанию
        return super().form_valid(form)
    

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'eventmanager/register.html'  # Твой шаблон для регистрации
    success_url = reverse_lazy('eventmanager:advent_list')  # Куда перенаправить после успешной регистрации
    
class AdventLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'eventmanager/login.html'  # Твой шаблон для log in
    def get_success_url(self):
        return reverse_lazy('eventmanager:advent_list')  # Куда перенаправить после успешной регистрации
    
class AdventLogoutView(LogoutView):
    next_page = reverse_lazy('eventmanager:advent_list')  # Куда перенаправить после успешной регистрации

class AdventUpdateView(UserPassesTestMixin, UpdateView):
    model = Advent
    fields = ['title', 'description', 'date', 'location', 'adventmanager_image']
    template_name = 'eventmanager/edite_advent.html'
    success_url = reverse_lazy('eventmanager:advent_list')

    # Проверяем, что текущий пользователь является создателем события
    def test_func(self):
        advent = self.get_object()
        return self.request.user == advent.user


class AdventDeleteView(UserPassesTestMixin, DeleteView):
    model = Advent
    template_name = 'eventmanager/delete_advent.html'
    success_url = reverse_lazy('eventmanager:advent_list')

    # Проверяем, что текущий пользователь является создателем события
    def test_func(self):
        advent = self.get_object()
        return self.request.user == advent.user
    
    
class AdventDetailView(DetailView):
    model = Advent
    template_name = 'eventmanager/advent_detail.html'
    context_object_name = 'advent'  # Указываем, что в шаблоне объект будет доступен как 'advent'

    def get_context_data(self, **kwargs):
        """
        Этот метод отвечает за отображение списка участников, которые уже подтвердили участие.
        """
        context = super().get_context_data(**kwargs)
        advent = self.get_object()  # Получаем объект Advent
        context['attendants'] = advent.rsvp_users.all()  # Список всех пользователей, которые нажали кнопку RSVP
        return context

    def post(self, request, *args, **kwargs):
        """
        Этот метод сохраняет информацию о том, что текущий пользователь подтвердил участие (нажал кнопку RSVP).
        """
        advent = self.get_object()  # Получаем объект Advent
        if request.user.is_authenticated:
            if request.user not in advent.rsvp_users.all():
                advent.rsvp_users.add(request.user)  # Добавляем пользователя в список участников
            return redirect('eventmanager:advent_detail', pk=advent.pk)
        else:
            return redirect('eventmanager:login')  # Перенаправляем на логин, если пользователь не залогинен

    

