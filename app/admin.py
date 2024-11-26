from django.contrib import admin
from django.contrib.admin import display
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Colaborador, EspelhoPonto, SiteConfiguration
from .admin_actions import importar_excel
from .widgets import ColorPickerWidget
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group

class CustomAdminSite(admin.AdminSite):
    site_header = 'Espelho de Ponto'
    site_title = 'Administração'
    index_title = 'Dashboard'

    def get_app_list(self, request):
        """
        Retorna uma lista personalizada de aplicativos ordenados
        """
        app_list = super().get_app_list(request)
        # Ordenar apps: app, auth, admin
        app_ordering = {
            'app': 1,
            'auth': 2,
            'admin': 3,
        }
        app_list.sort(key=lambda x: app_ordering.get(x['app_label'], 10))
        return app_list

# Criar instância do site admin customizado
admin_site = CustomAdminSite(name='admin')

# Registrar os modelos do auth no admin site customizado
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)

# Registrar os outros modelos
@admin.register(Colaborador, site=admin_site)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = [
        'display_colaborador_info',
        'display_status',
        'display_setor',
    ]
    
    @display(description="Informações")
    def display_colaborador_info(self, obj):
        """Exibe informações do colaborador em duas linhas com iniciais"""
        iniciais = ''.join(n[0].upper() for n in obj.nome.split()[:2])
        return [
            obj.nome,  # linha principal
            f"Matrícula: {obj.matricula}",  # linha secundária
            iniciais,  # iniciais no círculo
        ]
    
    @display(
        description=_("Status"),
        ordering="data_demissao",
        boolean=True
    )
    def display_status(self, obj):
        return obj.data_demissao is None
    
    @display(
        description=_("Setor"),
        ordering="centro_custo"
    )
    def display_setor(self, obj):
        return obj.centro_custo
    
    search_fields = ('matricula', 'nome', 'cpf', 'pis')
    list_filter = ('cargo', 'turno', 'centro_custo')
    ordering = ('nome',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('matricula', 'nome', 'cpf', 'pis')
        }),
        ('Informações Profissionais', {
            'fields': ('cargo', 'turno', 'centro_custo')
        }),
        ('Datas', {
            'fields': ('data_admissao', 'data_demissao')
        })
    )
    
    change_list_template = "admin/colaborador_changelist.html"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.import_excel_view, name='colaborador_import_excel'),
        ]
        return custom_urls + urls

    def import_excel_view(self, request):
        if request.method == "POST":
            if 'excel_file' not in request.FILES:
                messages.error(request, 'Nenhum arquivo foi enviado.')
                return render(request, 'admin/excel_import.html')
            
            excel_file = request.FILES['excel_file']
            
            # Verificar extensão do arquivo
            if not excel_file.name.endswith(('.xls', '.xlsx')):
                messages.error(request, 'Por favor, envie um arquivo Excel válido (.xls ou .xlsx)')
                return render(request, 'admin/excel_import.html')
            
            try:
                importar_excel(self, request, excel_file)
                return HttpResponseRedirect("../")
            except Exception as e:
                messages.error(request, f'Erro ao processar arquivo: {str(e)}')
                return render(request, 'admin/excel_import.html')
            
        return render(request, 'admin/excel_import.html')

    def get_metrics(self, request):
        return {
            "total_ativos": {
                "label": "Colaboradores Ativos",
                "value": Colaborador.objects.filter(data_demissao__isnull=True).count(),
            },
            "admitidos_mes": {
                "label": "Admitidos este mês",
                "value": Colaborador.objects.filter(
                    data_admissao__month=timezone.now().month,
                    data_admissao__year=timezone.now().year
                ).count(),
            },
        }

@admin.register(EspelhoPonto, site=admin_site)
class EspelhoPontoAdmin(admin.ModelAdmin):
    list_display = ('arquivo', 'data_envio')
    list_display_links = ('arquivo',)
    ordering = ('-data_envio',)

    def get_metrics(self, request):
        return {
            "total_espelhos": {
                "label": "Total de Espelhos",
                "value": EspelhoPonto.objects.count(),
            },
            "espelhos_mes": {
                "label": "Espelhos este mês",
                "value": EspelhoPonto.objects.filter(
                    data_envio__month=timezone.now().month,
                    data_envio__year=timezone.now().year
                ).count(),
            },
        }

@admin.register(SiteConfiguration, site=admin_site)
class SiteConfigurationAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        color_fields = ['primary_color', 'secondary_color', 'background_color', 'text_color', 'link_color']
        
        for field_name in color_fields:
            if field_name in form.base_fields:
                form.base_fields[field_name].widget = ColorPickerWidget()
        
        return form

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('site_name', 'logo', 'favicon')
        }),
        ('Cores do Tema', {
            'fields': (
                'primary_color', 'secondary_color', 'background_color',
                'text_color', 'link_color'
            ),
            'classes': ('wide',),
            'description': 'Selecione as cores do tema usando o color picker'
        }),
        ('Contato', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('Redes Sociais', {
            'fields': ('facebook_url', 'instagram_url', 'linkedin_url')
        }),
        ('Textos', {
            'fields': ('footer_text',)
        }),
    )

    class Media:
        css = {
            'all': ('admin/css/color-picker.css',)
        }

    def has_add_permission(self, request):
        return not SiteConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
