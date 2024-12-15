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
from datetime import timedelta

class CustomAdminSite(admin.AdminSite):
    site_header = 'Espelho de Ponto'
    site_title = 'Administração'
    index_title = 'Dashboard'

    def index(self, request, extra_context=None):
        """
        Customiza o dashboard do admin com métricas
        """
        # Obtém o mês atual
        hoje = timezone.now()
        primeiro_dia_mes = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Métricas dos Cards
        colaboradores_metrics = {
            "colaboradores_ativos": Colaborador.objects.filter(
                data_demissao__isnull=True
            ).count(),
            "admitidos_mes": Colaborador.objects.filter(
                data_admissao__year=hoje.year,
                data_admissao__month=hoje.month
            ).count(),
            "demitidos_mes": Colaborador.objects.filter(
                data_demissao__year=hoje.year,
                data_demissao__month=hoje.month
            ).count(),
            "total_colaboradores": Colaborador.objects.count(),
        }
        
        # Gráfico 1: Admissões por Mês (últimos 6 meses)
        admissoes_dados = (
            Colaborador.objects
            .filter(
                data_admissao__isnull=False,
                data_admissao__gte=hoje - timedelta(days=180)
            )
            .annotate(mes=TruncMonth('data_admissao'))
            .values('mes')
            .annotate(total=Count('id'))
            .order_by('mes')
        )
        
        # Gráfico 2: Colaboradores por Cargo
        cargos_dados = (
            Colaborador.objects
            .filter(data_demissao__isnull=True)
            .values('cargo')
            .annotate(total=Count('id'))
            .order_by('-total')[:8]  # Top 8 cargos
        )
        
        # Gráfico 3: Colaboradores por Centro de Custo
        setores_dados = (
            Colaborador.objects
            .filter(data_demissao__isnull=True)
            .values('centro_custo')
            .annotate(total=Count('id'))
            .order_by('-total')
        )
        
        # Gráfico 4: Status dos Colaboradores (Ativos vs Inativos)
        status_dados = {
            'Ativos': colaboradores_metrics['colaboradores_ativos'],
            'Inativos': Colaborador.objects.filter(data_demissao__isnull=False).count()
        }

        # Formatando dados para os gráficos
        context = {
            **colaboradores_metrics,
            'labels_admissoes': [d['mes'].strftime('%b/%Y') for d in admissoes_dados],
            'valores_admissoes': [d['total'] for d in admissoes_dados],
            
            'labels_cargos': [d['cargo'] for d in cargos_dados],
            'valores_cargos': [d['total'] for d in cargos_dados],
            
            'labels_setores': [d['centro_custo'] for d in setores_dados],
            'valores_setores': [d['total'] for d in setores_dados],
            
            'labels_status': list(status_dados.keys()),
            'valores_status': list(status_dados.values()),
        }
        
        return super().index(request, extra_context=context)

    def get_app_list(self, request):
        """
        Retorna uma lista personalizada de aplicativos ordenados
        """
        app_list = super().get_app_list(request)
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

# Classes de admin (sem decoradores)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'nome', 'cargo', 'centro_custo', 'data_admissao', 'status_colaborador')
    list_filter = ('centro_custo', 'cargo', 'data_admissao', 'data_demissao')
    search_fields = ('nome', 'matricula', 'cpf', 'pis')
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
        }),
    )

    def status_colaborador(self, obj):
        return "Ativo" if obj.data_demissao is None else "Inativo"
    status_colaborador.short_description = "Status"
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('nome')
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(matricula=search_term_as_int)
        except ValueError:
            pass
        return queryset, use_distinct

    class Media:
        css = {
            'all': ('admin/css/custom_jazzmin.css',)
        }

    # Personalização das ações em massa
    actions = ['marcar_como_demitido']

    def marcar_como_demitido(self, request, queryset):
        hoje = timezone.now().date()
        queryset.update(data_demissao=hoje)
        self.message_user(request, f"{queryset.count()} colaborador(es) marcado(s) como demitido(s).")
    marcar_como_demitido.short_description = "Marcar selecionados como demitidos"

    # Customização da exibição de campos
    def get_list_display(self, request):
        list_display = list(super().get_list_display(request))
        return list_display

    def get_list_filter(self, request):
        list_filter = list(super().get_list_filter(request))
        return list_filter

    # Formatação de campos específicos
    @admin.display(description='Data de Admissão')
    def data_admissao_formatada(self, obj):
        return obj.data_admissao.strftime('%d/%m/%Y') if obj.data_admissao else '-'

    @admin.display(description='Data de Demissão')
    def data_demissao_formatada(self, obj):
        return obj.data_demissao.strftime('%d/%m/%Y') if obj.data_demissao else '-'

    # Customização do formulário
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['matricula'].widget.attrs['class'] = 'vTextField'
        form.base_fields['nome'].widget.attrs['class'] = 'vTextField'
        return form

    # Adicione o método get_urls
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.admin_site.admin_view(self.import_excel_view),
                 name='app_colaborador_import_excel'),
        ]
        return custom_urls + urls

    def import_excel_view(self, request):
        print("Acessando view de importação")  # Debug
        if request.method == 'POST':
            if 'excel_file' in request.FILES:
                try:
                    importar_excel(self, request, request.FILES['excel_file'])
                    self.message_user(request, "Importação concluída com sucesso!")
                    return HttpResponseRedirect("../")
                except Exception as e:
                    print(f"Erro na importação: {str(e)}")  # Debug
                    self.message_user(request, f"Erro na importação: {str(e)}", level='ERROR')
        return render(
            request, 
            'admin/app/colaborador/import.html',  # Caminho corrigido
            context={'opts': self.model._meta}
        )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_import_button'] = True
        return super().changelist_view(request, extra_context)

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

# Registrar todos os modelos no final do arquivo
admin_site.register(Colaborador, ColaboradorAdmin)
admin_site.register(EspelhoPonto, EspelhoPontoAdmin)
admin_site.register(SiteConfiguration, SiteConfigurationAdmin)
