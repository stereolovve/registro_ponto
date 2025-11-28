from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import date, datetime
from decimal import Decimal
import json
import calendar
from .models import WorkCode, TimeRecord, Salary


@login_required
def dashboard_view(request):
    """Dashboard with statistics"""
    user = request.user
    hoje = date.today()

    # Registros do mês atual
    registros_mes = TimeRecord.objects.filter(
        user=user,
        data__month=hoje.month,
        data__year=hoje.year
    )

    # Calcular horas trabalhadas
    horas_mes = sum([r.calcular_horas_trabalhadas() for r in registros_mes])

    # Previsão de salário
    previsao_salario = Decimal(str(horas_mes)) * user.profile.valor_hora

    # Nome do mês em português
    meses = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }

    context = {
        'mes_atual': meses[hoje.month],
        'ano_atual': hoje.year,
        'horas_mes_atual': round(horas_mes, 2),
        'previsao_salario': previsao_salario,
        'total_registros_mes': registros_mes.count(),
    }

    return render(request, 'timetrack/dashboard.html', context)


@login_required
def registrar_ponto_view(request):
    """Time clock interface"""
    hoje = date.today()

    if request.method == 'POST':
        # Coletar dados dos 3 períodos
        entrada1 = request.POST.get('entrada1') or None
        saida1 = request.POST.get('saida1') or None
        entrada2 = request.POST.get('entrada2') or None
        saida2 = request.POST.get('saida2') or None
        entrada3 = request.POST.get('entrada3') or None
        saida3 = request.POST.get('saida3') or None
        work_code_id = request.POST.get('work_code')
        observacoes = request.POST.get('observacoes', '')

        try:
            work_code = WorkCode.objects.get(id=work_code_id, ativo=True)

            # Criar ou atualizar registro
            time_record, created = TimeRecord.objects.update_or_create(
                user=request.user,
                data=hoje,
                defaults={
                    'entrada1': entrada1,
                    'saida1': saida1,
                    'entrada2': entrada2,
                    'saida2': saida2,
                    'entrada3': entrada3,
                    'saida3': saida3,
                    'work_code': work_code,
                    'observacoes': observacoes,
                }
            )

            # clean() é chamado automaticamente e valida
            action = 'criado' if created else 'atualizado'
            messages.success(request, f'Ponto {action} com sucesso!')
            return redirect('historico')

        except WorkCode.DoesNotExist:
            messages.error(request, 'Código de trabalho inválido')
        except Exception as e:
            messages.error(request, f'Erro ao registrar ponto: {str(e)}')

    # GET: carregar registro existente do dia ou criar vazio
    try:
        registro = TimeRecord.objects.get(user=request.user, data=hoje)
    except TimeRecord.DoesNotExist:
        registro = None

    work_codes = WorkCode.objects.filter(ativo=True)

    context = {
        'registro': registro,
        'work_codes': work_codes,
        'data_hoje': hoje,
    }

    return render(request, 'timetrack/registrar_ponto.html', context)


@login_required
def historico_view(request):
    """View time records history"""
    hoje = date.today()

    # Filtros
    mes = int(request.GET.get('mes', hoje.month))
    ano = int(request.GET.get('ano', hoje.year))

    # Buscar registros
    registros = TimeRecord.objects.filter(
        user=request.user,
        data__month=mes,
        data__year=ano
    ).select_related('work_code').order_by('-data')

    # Calcular total de horas
    total_horas = sum([r.calcular_horas_trabalhadas() for r in registros])

    # Nome do mês
    meses = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }

    context = {
        'registros': registros,
        'mes_selecionado': mes,
        'ano_selecionado': ano,
        'mes_nome': meses.get(mes, ''),
        'total_horas': round(total_horas, 2),
        'meses': [(i, meses[i]) for i in range(1, 13)],
        'anos': range(2020, 2031),
    }

    return render(request, 'timetrack/historico.html', context)


@login_required
def historico_editar_view(request, record_id):
    """Edit time record"""
    registro = get_object_or_404(TimeRecord, id=record_id, user=request.user)

    if request.method == 'POST':
        # Coletar dados dos 3 períodos
        entrada1 = request.POST.get('entrada1') or None
        saida1 = request.POST.get('saida1') or None
        entrada2 = request.POST.get('entrada2') or None
        saida2 = request.POST.get('saida2') or None
        entrada3 = request.POST.get('entrada3') or None
        saida3 = request.POST.get('saida3') or None
        work_code_id = request.POST.get('work_code')
        observacoes = request.POST.get('observacoes', '')

        try:
            work_code = WorkCode.objects.get(id=work_code_id, ativo=True)

            # Atualizar registro
            registro.entrada1 = entrada1
            registro.saida1 = saida1
            registro.entrada2 = entrada2
            registro.saida2 = saida2
            registro.entrada3 = entrada3
            registro.saida3 = saida3
            registro.work_code = work_code
            registro.observacoes = observacoes
            registro.save()

            messages.success(request, 'Registro atualizado com sucesso!')
            # Redirecionar de volta ao histórico com os filtros
            return redirect(f'/historico/?mes={registro.data.month}&ano={registro.data.year}')

        except WorkCode.DoesNotExist:
            messages.error(request, 'Código de trabalho inválido')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar registro: {str(e)}')

    work_codes = WorkCode.objects.filter(ativo=True)

    context = {
        'registro': registro,
        'work_codes': work_codes,
    }

    return render(request, 'timetrack/historico_editar.html', context)


# ============ AJAX API ENDPOINTS ============

@login_required
@require_http_methods(["POST"])
def api_update_time_record(request, record_id):
    """Update a single field of existing TimeRecord via AJAX"""
    try:
        # Get record and validate ownership
        registro = get_object_or_404(TimeRecord, id=record_id, user=request.user)

        # Parse JSON body
        data = json.loads(request.body)
        field = data.get('field')
        value = data.get('value')

        # Convert empty strings to None
        if value == '' or value == '-':
            value = None

        # Update the specific field
        allowed_fields = [
            'entrada1', 'saida1', 'entrada2', 'saida2', 'entrada3', 'saida3',
            'work_code_id', 'observacoes'
        ]

        if field not in allowed_fields:
            return JsonResponse({
                'success': False,
                'errors': f'Campo inválido: {field}'
            }, status=400)

        # Handle work_code specially
        if field == 'work_code_id':
            try:
                work_code = WorkCode.objects.get(id=value, ativo=True)
                registro.work_code = work_code
            except WorkCode.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'errors': 'Código de trabalho inválido'
                }, status=400)
        else:
            setattr(registro, field, value)

        # Run validation
        try:
            registro.full_clean()
            registro.save()
        except Exception as e:
            return JsonResponse({
                'success': False,
                'errors': str(e)
            }, status=400)

        # Calculate and return updated hours
        total_hours = registro.calcular_horas_trabalhadas()

        return JsonResponse({
            'success': True,
            'total_hours': round(total_hours, 2),
            'record_id': registro.id
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'errors': 'JSON inválido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'errors': str(e)
        }, status=500)


@login_required
@require_http_methods(["POST"])
def api_create_time_record(request):
    """Create new TimeRecord for a specific date via AJAX"""
    try:
        # Parse JSON body
        data = json.loads(request.body)
        data_str = data.get('date')  # Expected format: 'YYYY-MM-DD'
        work_code_id = data.get('work_code_id')

        # Parse date
        data_obj = datetime.strptime(data_str, '%Y-%m-%d').date()

        # Check if record already exists
        if TimeRecord.objects.filter(user=request.user, data=data_obj).exists():
            return JsonResponse({
                'success': False,
                'errors': 'Registro já existe para esta data'
            }, status=400)

        # Get work code
        if work_code_id:
            try:
                work_code = WorkCode.objects.get(id=work_code_id, ativo=True)
            except WorkCode.DoesNotExist:
                work_code = WorkCode.objects.filter(ativo=True).first()
        else:
            work_code = WorkCode.objects.filter(ativo=True).first()

        # Create record with empty periods
        registro = TimeRecord.objects.create(
            user=request.user,
            data=data_obj,
            work_code=work_code
        )

        return JsonResponse({
            'success': True,
            'record_id': registro.id
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'errors': 'JSON inválido'
        }, status=400)
    except ValueError as e:
        return JsonResponse({
            'success': False,
            'errors': f'Data inválida: {str(e)}'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'errors': str(e)
        }, status=500)


# ============ UNIFIED TIMESHEET VIEW ============

def generate_calendar_grid(year, month, records):
    """
    Generate calendar data for the month with record status indicators
    Returns a list of weeks, where each week is a list of day dictionaries
    """
    # Create a dictionary mapping date -> record for quick lookup
    records_by_date = {r.data: r for r in records}

    # Get calendar for the month
    cal = calendar.monthcalendar(year, month)

    # Day names in Portuguese
    day_names = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']

    # Build calendar grid with metadata
    calendar_weeks = []
    today = date.today()

    for week in cal:
        calendar_week = []
        for day_num in week:
            if day_num == 0:
                # Empty day (padding from previous/next month)
                calendar_week.append({
                    'day': '',
                    'date': None,
                    'has_record': False,
                    'is_today': False,
                    'is_complete': False,
                    'is_partial': False,
                    'hours': 0
                })
            else:
                day_date = date(year, month, day_num)
                record = records_by_date.get(day_date)

                has_record = record is not None
                hours = record.calcular_horas_trabalhadas() if record else 0

                # Determine if record is complete (all 3 periods filled) or partial
                is_complete = False
                is_partial = False
                if record:
                    filled_periods = sum([
                        1 if (record.entrada1 and record.saida1) else 0,
                        1 if (record.entrada2 and record.saida2) else 0,
                        1 if (record.entrada3 and record.saida3) else 0
                    ])
                    is_complete = filled_periods == 3
                    is_partial = filled_periods > 0 and not is_complete

                calendar_week.append({
                    'day': day_num,
                    'date': day_date,
                    'date_str': day_date.strftime('%Y-%m-%d'),
                    'has_record': has_record,
                    'is_today': day_date == today,
                    'is_complete': is_complete,
                    'is_partial': is_partial,
                    'hours': round(hours, 1),
                    'record_id': record.id if record else None
                })
        calendar_weeks.append(calendar_week)

    return {
        'weeks': calendar_weeks,
        'day_names': day_names
    }


@login_required
def timesheet_view(request):
    """Unified timesheet interface with calendar + table"""
    hoje = date.today()

    # Get month/year from query params (default to current)
    mes = int(request.GET.get('mes', hoje.month))
    ano = int(request.GET.get('ano', hoje.year))

    # Get all records for user in that month
    registros = TimeRecord.objects.filter(
        user=request.user,
        data__month=mes,
        data__year=ano
    ).select_related('work_code').order_by('data')

    # Generate calendar data (all days in month with record status)
    calendar_data = generate_calendar_grid(ano, mes, registros)

    # Get all work codes for dropdown
    work_codes = WorkCode.objects.filter(ativo=True)

    # Calculate month summary
    total_hours = sum(r.calcular_horas_trabalhadas() for r in registros)

    # Month names in Portuguese
    meses = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }

    # Generate all days in month for table (including days without records)
    _, num_days = calendar.monthrange(ano, mes)
    all_days = []

    # Day names in Portuguese
    day_names_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']

    records_dict = {r.data: r for r in registros}

    for day in range(1, num_days + 1):
        day_date = date(ano, mes, day)
        record = records_dict.get(day_date)

        # Get day of week (0=Monday, 6=Sunday)
        weekday = day_date.weekday()
        day_name = day_names_pt[weekday]

        all_days.append({
            'date': day_date,
            'date_str': day_date.strftime('%d/%m'),
            'date_iso': day_date.strftime('%Y-%m-%d'),
            'day_name': day_name,
            'record': record,
            'is_today': day_date == hoje
        })

    context = {
        'registros': registros,
        'all_days': all_days,
        'calendar_data': calendar_data,
        'work_codes': work_codes,
        'mes_selecionado': mes,
        'ano_selecionado': ano,
        'mes_nome': meses.get(mes, ''),
        'total_horas': round(total_hours, 2),
        'total_registros': registros.count(),
        'meses': [(i, meses[i]) for i in range(1, 13)],
        'anos': range(2020, 2031),
    }

    return render(request, 'timetrack/timesheet.html', context)
