from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import datetime, time

class WorkCode(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    descricao = models.CharField(max_length=200)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Código de Trabalho'
        verbose_name_plural = 'Códigos de Trabalho'
        ordering = ['codigo']
    
    def __str__(self):
        return f'{self.codigo} - {self.descricao}'

class TimeRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateField()
    
    entrada1 = models.TimeField(null=True, blank=True)
    saida1 = models.TimeField(null=True, blank=True)
    entrada2 = models.TimeField(null=True, blank=True)
    saida2 = models.TimeField(null=True, blank=True)
    entrada3 = models.TimeField(null=True, blank=True)
    saida3 = models.TimeField(null=True, blank=True)
    
    work_code = models.ForeignKey(WorkCode, on_delete=models.PROTECT, null=True, blank=True)
    observacoes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Registro de Ponto'
        verbose_name_plural = 'Registros de Ponto'
        unique_together = ['user', 'data']
        ordering = ['-data']
    
    def clean(self):
        if self.entrada1 and self.saida1:
            if self.entrada1 >= self.saida1:
                raise ValidationError('Horário de saída deve ser posterior ao de entrada')
        
        if self.entrada2 and self.saida2:
            if self.entrada2 >= self.saida2:
                raise ValidationError('Horário de saída 2 deve ser posterior ao de entrada 2')
            if self.saida1 and self.entrada2 <= self.saida1:
                raise ValidationError('Entrada 2 deve ser posterior à saída 1')
        
        if self.entrada3 and self.saida3:
            if self.entrada3 >= self.saida3:
                raise ValidationError('Horário de saída 3 deve ser posterior ao de entrada 3')
            if self.saida2 and self.entrada3 <= self.saida2:
                raise ValidationError('Entrada 3 deve ser posterior à saída 2')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def calcular_horas_trabalhadas(self):
        total_segundos = 0
        
        if self.entrada1 and self.saida1:
            delta1 = datetime.combine(datetime.today(), self.saida1) - datetime.combine(datetime.today(), self.entrada1)
            total_segundos += delta1.total_seconds()
        
        if self.entrada2 and self.saida2:
            delta2 = datetime.combine(datetime.today(), self.saida2) - datetime.combine(datetime.today(), self.entrada2)
            total_segundos += delta2.total_seconds()
        
        if self.entrada3 and self.saida3:
            delta3 = datetime.combine(datetime.today(), self.saida3) - datetime.combine(datetime.today(), self.entrada3)
            total_segundos += delta3.total_seconds()
        
        return round(total_segundos / 3600, 2)
    
    def __str__(self):
        return f'{self.user.get_full_name()} - {self.data} ({self.calcular_horas_trabalhadas()}h)'

class Salary(models.Model):
    STATUS_CHOICES = [
        ('calculando', 'Calculando'),
        ('pendente', 'Pendente Aprovação'),
        ('aprovado', 'Aprovado'),
        ('pago', 'Pago'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mes = models.PositiveIntegerField()
    ano = models.PositiveIntegerField()
    horas_trabalhadas = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    valor_hora = models.DecimalField(max_digits=8, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='calculando')
    observacoes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Salário'
        verbose_name_plural = 'Salários'
        unique_together = ['user', 'mes', 'ano']
        ordering = ['-ano', '-mes']
    
    def save(self, *args, **kwargs):
        self.valor_total = self.horas_trabalhadas * self.valor_hora
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.user.get_full_name()} - {self.mes:02d}/{self.ano} - R$ {self.valor_total}'
