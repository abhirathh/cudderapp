from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name = 'register'),
    path('login', views.login, name = 'login'),
    path('logout', views.logout, name = 'logout'),
    path('forgotPassword', views.forgotPassword, name = 'forgotPassword'),
    path('reset', views.resetPasswordRender, name = 'resetPasswordRender'),
    path('reset-password', views.resetPassword, name = 'resetPassword'),
]
