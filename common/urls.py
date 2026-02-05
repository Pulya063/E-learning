from django.urls import path

from common import views
urlpatterns = [
    path('user/<int:user_id>', views.user_page, name='user_page'),
    path('login', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('main_page', views.main_page, name='main_page'),
]
