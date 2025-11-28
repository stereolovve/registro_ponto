from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='timesheet/login.html'), name='login'),
    path('accounts/login/', RedirectView.as_view(url='/login/')), # Redirect legacy/default auth URL
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('timesheet/', views.monthly_view, name='monthly_view'),
    path('timesheet/<int:user_id>/', views.monthly_view, name='monthly_view_user'),
    path('save/', views.save_timesheet, name='save_timesheet'),
]