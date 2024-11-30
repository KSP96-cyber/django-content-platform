from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView
from django.urls import reverse_lazy
from .models import Blog, Comment
from .forms import BlogForm, CommentForm
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.utils import timezone 


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'  # Template to be used for rendering
    context_object_name = 'blogs'  # variable name/Имя переменной в шаблоне
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # Получаем стандартный контекст/obtaining the default context
        context['user'] = self.request.user # Добавляем текущего пользователя/adding the current user
        return context   # Возвращаем обновленный контекст/returning the updated context
    
class BlogCreateView(LoginRequiredMixin,CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_create.html'
    login_url = 'blog:login' # Перенаправляет на страницу логина, если пользователь не залогиненredirect to the login if user is not logged in
    success_url = reverse_lazy('blog:blog_list')  # Перенаправление на список событий после успешного создания/redirect to the list of blogs after successful creation

    def form_valid(self, form):
        form.instance.user = self.request.user  # Устанавливаем текущего пользователя/ setting the current user
        form.instance.blog_view_count = 1  # Устанавливаем значение по умолчанию/ setting the default value
        return super().form_valid(form)
    

class BlogRegisterView(CreateView,):
    form_class = UserCreationForm
    template_name = 'blog/register.html'  # Твой шаблон для регистрации/ template for registration
    success_url = reverse_lazy('blog:blog_list')  # Куда перенаправить после успешной регистрации/ where to redirect after successful login
    
class BlogLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'blog/login.html'
    def get_success_url(self):
        return reverse_lazy('blog:blog_list')  
    
class BlogLogoutView(LogoutView):
    next_page = reverse_lazy('blog:blog_list')  

class BlogUpdateView(UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ['title', 'description', 'date', 'location', 'image']
    template_name = 'blog/blog_edit.html'
    success_url = reverse_lazy('blog:blog_list')

    # Проверяем, что текущий пользователь является создателем события/checking that the current user is the creator of the post
    def test_func(self):
        blog = self.get_object()
        return self.request.user == blog.user
    
class BlogDeleteView(UserPassesTestMixin, DeleteView):
    model = Blog
    template_name = 'blog/blog_delete.html'
    success_url = reverse_lazy('blog:blog_list')

    def test_func(self):
        blog = self.get_object()
        return self.request.user == blog.user
    
    
class BlogDetailView(LoginRequiredMixin, DetailView, FormView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'
    form_class = CommentForm
    login_url = 'blog:login'  

    def get_context_data(self, **kwargs):
        # Add comments to the context
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        return context

    def form_valid(self, form):
        # Process comment submission
        blog = self.get_object()  # Get current blog
        Comment.objects.create(
            blog=blog,
            user=self.request.user,
            text=form.cleaned_data['text']
        )
        return redirect('blog:blog_detail', pk=blog.pk)


