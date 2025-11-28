from django.contrib import admin
from django.utils import timezone
from .models import WorkCode, TimeRecord, Salary

@admin.register(WorkCode)
class WorkCodeAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descricao', 'ativo', 'created_at']
    list_filter = ['ativo']
    search_fields = ['codigo', 'descricao']
    ordering = ['codigo']

@admin.register(TimeRecord)
class TimeRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'data', 'entrada1', 'saida1', 'entrada2', 'saida2', 'entrada3', 'saida3', 'work_code', 'calcular_horas_trabalhadas']
    list_filter = ['data', 'work_code', 'user']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    date_hierarchy = 'data'
    ordering = ['-data']
    readonly_fields = ['calcular_horas_trabalhadas']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('user', 'data', 'work_code')
        }),
        ('Horários', {
            'fields': (
                ('entrada1', 'saida1'),
                ('entrada2', 'saida2'),
                ('entrada3', 'saida3'),
            )
        }),
        ('Observações', {
            'fields': ('observacoes',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if obj.aprovado and not obj.aprovado_em:
            obj.aprovado_por = request.user
            obj.aprovado_em = timezone.now()
        super().save_model(request, obj, form, change)

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ['user', 'mes', 'ano', 'horas_trabalhadas', 'valor_hora', 'valor_total', 'status']
    list_filter = ['status', 'ano', 'mes']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    ordering = ['-ano', '-mes']
    readonly_fields = ['valor_total']
