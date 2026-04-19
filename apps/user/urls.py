from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    MeView,
    UserListCreateView,
    UserDetailView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',    LoginView.as_view(),    name='login'),
    path('logout/',   LogoutView.as_view(),   name='logout'),
    path('me/',       MeView.as_view(),       name='me'),
    path('',          UserListCreateView.as_view(), name='user-list-create'),
    path('<int:id>/', UserDetailView.as_view(),     name='user-detail'),
]