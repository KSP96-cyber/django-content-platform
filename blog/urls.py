from django.urls import path
from . views import BlogListView, BlogCreateView, BlogRegisterView, BlogLoginView, BlogLogoutView, BlogUpdateView, BlogDeleteView, BlogDetailView


app_name = 'blog'

urlpatterns = [
    path('list/', BlogListView.as_view(), name='blog_list'),  
    path('create/', BlogCreateView.as_view(), name='blog_create'),  
    path('register/', BlogRegisterView.as_view(), name='register'),  
    path('login/', BlogLoginView.as_view(), name='login'),  
    path('logout/', BlogLogoutView.as_view(), name='logout'),  
    path('blog/<int:pk>/edit/', BlogUpdateView.as_view(), name='blog_edit'),
    path('blog/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
    path('blog/<int:pk>/',  BlogDetailView.as_view(), name='blog_detail'),
]