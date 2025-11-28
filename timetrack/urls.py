from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # New unified timesheet interface
    path('timesheet/', views.timesheet_view, name='timesheet'),

    # AJAX API endpoints
    path('api/time-records/<int:record_id>/update/', views.api_update_time_record, name='api_update_time_record'),
    path('api/time-records/create/', views.api_create_time_record, name='api_create_time_record'),

    # Legacy routes (kept temporarily, redirect to timesheet)
    path('registrar-ponto/', RedirectView.as_view(url='/timesheet/', permanent=False), name='registrar_ponto'),
    path('historico/', RedirectView.as_view(url='/timesheet/', permanent=False), name='historico'),
    path('historico/editar/<int:record_id>/', RedirectView.as_view(url='/timesheet/', permanent=False), name='historico_editar'),
]
