from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .forms import StyledAuthenticationForm
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(template_name='habits/login.html', authentication_form=StyledAuthenticationForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('habits/create/', views.habit_create, name='habit_create'),
    path('habits/<int:pk>/edit/', views.habit_update, name='habit_update'),
    path('habits/<int:pk>/delete/', views.habit_delete, name='habit_delete'),
    path('habits/<int:pk>/', views.habit_detail, name='habit_detail'),
    path('habits/<int:pk>/toggle-today/', views.toggle_today, name='toggle_today'),
    path('habits/<int:pk>/log/', views.log_update_or_create, name='log_update_or_create'),
]
