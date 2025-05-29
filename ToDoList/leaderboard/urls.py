from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_view
from .views import Homepage


# url - view - template
app_name = 'leaderboard'

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
]