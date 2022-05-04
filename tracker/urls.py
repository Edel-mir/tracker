from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = [
    path('', login_required(ExpenseListCreateView.as_view()), name='listPage'),
    path('edit/<int:pk>/', ExpenseEditPage, name='editPage'),
    path('delete/<int:pk>/', ExpenseDeleteView, name='deletePage'),
    path('statistic/', StatisticPage, name='statisticPage'),
    path('login/', Login.as_view()),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView),
]
