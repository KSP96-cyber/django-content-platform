from django.urls import path
from . views import AdventListView, AdventCreateView, RegisterView, AdventLoginView, AdventLogoutView, AdventUpdateView, AdventDeleteView, AdventDetailView
from django.contrib.auth.views import LogoutView

app_name = 'eventmanager'

urlpatterns = [
    path('', AdventListView.as_view(), name='advent_list'),  # CBV для списка событий
    path('create/', AdventCreateView.as_view(), name='create_advent'),  # CBV для создания событий
    path('register/', RegisterView.as_view(), name='register'),  # Путь для регистрации
    path('login/', AdventLoginView.as_view(), name='login'),  # Путь для логина
    path('logout/', AdventLogoutView.as_view(), name='logout'),  # Путь для логаута
    path('advent/<int:pk>/edit/', AdventUpdateView.as_view(), name='edit_advent'),
    path('advent/<int:pk>/delete/', AdventDeleteView.as_view(), name='delete_advent'),
    path('advent/<int:pk>/',  AdventDetailView.as_view(), name='advent_detail'),

]




