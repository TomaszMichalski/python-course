from django.urls import path
from django.urls import re_path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    re_path(r'^main[/]?$', views.main, name='main'),
    path('main/browse/', views.browse, name='browse'),
    path('main/manage/', views.manage, name='manage'),
    path('main/history/', views.history, name='history'),
    re_path(r'^main/chart[/]?$', views.browse),
    path('main/chart/<name>/', views.chart, name='chart'),
    re_path(r'', views.page_not_found, name='error')
]