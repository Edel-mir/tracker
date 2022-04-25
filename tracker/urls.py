from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *

urlpatterns = [
    path('', listPage, name='listPage'),
    path('statistic/', statisticPage, name='statisticPage'),
    path('login/', Login.as_view()),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register),
]
