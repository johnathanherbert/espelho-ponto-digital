from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.core.validators import RegexValidator
from .widgets import ColorPickerWidget


class Colaborador(models.Model):
    # Dados Básicos
    matricula = models.CharField('Matrícula', max_length=20, unique=True)
    nome = models.CharField('Nome', max_length=200)
    
    # Documentos
    cpf = models.CharField('CPF', max_length=14, null=True, blank=True)
    pis = models.CharField('PIS', max_length=14, null=True, blank=True)
    
    # Dados Funcionais
    data_admissao = models.DateField('Data de Admissão', null=True, blank=True)
    data_demissao = models.DateField('Data de Demissão', null=True, blank=True)
    cargo = models.CharField('Cargo', max_length=200)  # Aumentei para 200 devido aos cargos longos
    
    # Informações Organizacionais
    TURNOS_CHOICES = [
        ('1T', 'MUSASHI - 1 TURNO - 07:00 as 15:05 - Segunda-Feira à Sábado'),
        ('2T', 'MUSASHI - 2 TURNO - 14:50 as 22:48 - Segunda-Feira à Sábado'),
        ('RD', 'REVEZAMENTO 1 (DIURNO) - 07:00 as 19:00 (1x1)'),
        ('RN', 'REVEZAMENTO 2 (NOTURNO) - 19:00 as 07:00 (1x1)'),
    ]
    
    turno = models.CharField(
        'Turno', 
        max_length=200,  # Aumentei devido aos turnos longos
        choices=TURNOS_CHOICES
    )
    
    equipe = models.CharField(
        'Equipe', 
        max_length=100, 
        default='MUSASHI'
    )
    
    centro_custo = models.CharField(
        'Centro de Custo', 
        max_length=100,
        default='MUSASHI - MANAUS'
    )

    def clean(self):
        # Remove espaços extras do nome
        if self.nome:
            self.nome = self.nome.strip().upper()
        
        # Formatação do CPF
        if self.cpf:
            cpf_limpo = ''.join(filter(str.isdigit, self.cpf))
            if len(cpf_limpo) == 11:
                self.cpf = f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
            else:
                raise ValidationError({'cpf': 'CPF deve conter 11 dígitos'})

        # Formatação do PIS
        if self.pis:
            pis_limpo = ''.join(filter(str.isdigit, self.pis))
            if len(pis_limpo) == 11:
                self.pis = f"{pis_limpo[:3]}.{pis_limpo[3:8]}.{pis_limpo[8:10]}-{pis_limpo[10]}"
            else:
                raise ValidationError({'pis': 'PIS deve conter 11 dígitos'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.matricula} - {self.nome}"

    class Meta:
        verbose_name = 'Colaborador'
        verbose_name_plural = 'Colaboradores'
        ordering = ['nome']


class EspelhoPonto(models.Model):
    arquivo = models.FileField(
        upload_to='espelho_ponto/',
        verbose_name='Arquivo PDF',
        help_text='Selecione o arquivo PDF do espelho de ponto'
    )
    data_envio = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Envio'
    )

    class Meta:
        verbose_name = 'Espelho de Ponto'
        verbose_name_plural = 'Espelhos de Ponto'

    def __str__(self):
        return f"Espelho de Ponto - {self.data_envio.strftime('%d/%m/%Y %H:%M')}"


class SiteConfiguration(models.Model):
    # Configurações Gerais
    site_name = models.CharField('Nome do Site', max_length=100, default='Espelho de Ponto')
    logo = models.ImageField('Logo', upload_to='site_config/', null=True, blank=True)
    favicon = models.ImageField('Favicon', upload_to='site_config/', null=True, blank=True)
    
    # Cores Principais
    color_validator = RegexValidator(
        regex=r'^#([A-Fa-f0-9]{6})$',
        message='Digite uma cor hexadecimal válida (ex: #FF0000)'
    )

    primary_color = models.CharField(
        max_length=7,
        default="#3B82F6",
        validators=[color_validator],
        verbose_name="Cor Primária"
    )
    secondary_color = models.CharField(
        max_length=7,
        default="#1D4ED8",
        validators=[color_validator],
        verbose_name="Cor Secundária"
    )
    
    # Cores do Tema
    background_color = models.CharField(
        max_length=7,
        default="#F3F4F6",
        validators=[color_validator],
        verbose_name="Cor de Fundo"
    )
    text_color = models.CharField(
        max_length=7,
        default="#111827",
        validators=[color_validator],
        verbose_name="Cor do Texto"
    )
    link_color = models.CharField(
        max_length=7,
        default="#2563EB",
        validators=[color_validator],
        verbose_name="Cor dos Links"
    )
    
    # Cores do Modo Escuro
    dark_background_color = models.CharField('Cor de Fundo (Modo Escuro)', 
                                           max_length=7, default='#1F2937')
    dark_text_color = models.CharField('Cor do Texto (Modo Escuro)', 
                                     max_length=7, default='#F9FAFB')
    dark_link_color = models.CharField('Cor dos Links (Modo Escuro)', 
                                     max_length=7, default='#60A5FA')
    
    # Textos Personalizáveis
    welcome_text = models.CharField('Texto de Boas-vindas', max_length=200,
                                  default='Espelho de Ponto Digital')
    welcome_subtitle = models.CharField('Subtítulo de Boas-vindas', max_length=200,
                                      default='Acesse seu espelho de ponto de forma rápida e segura')
    footer_text = models.TextField('Texto do Rodapé', 
                                 default='© {% now "Y" %} Espelho de Ponto Digital. Todos os direitos reservados.')
    
    # Contato
    contact_email = models.EmailField('Email de Contato', blank=True)
    contact_phone = models.CharField('Telefone de Contato', max_length=20, blank=True)
    
    # Redes Sociais
    facebook_url = models.URLField('URL do Facebook', blank=True)
    instagram_url = models.URLField('URL do Instagram', blank=True)
    linkedin_url = models.URLField('URL do LinkedIn', blank=True)

    class Meta:
        verbose_name = 'Configuração do Site'
        verbose_name_plural = 'Configurações do Site'

    def __str__(self):
        return 'Configurações do Site'

    def clean(self):
        # Validar formato das cores
        color_fields = [
            'primary_color', 'secondary_color', 'background_color',
            'text_color', 'link_color', 'dark_background_color',
            'dark_text_color', 'dark_link_color'
        ]
        
        for field in color_fields:
            color = getattr(self, field)
            if not color.startswith('#') or len(color) != 7:
                raise ValidationError({field: 'Cor inválida. Use formato hexadecimal (#RRGGBB)'})

        # Validar dimensões do logo
        if self.logo:
            width, height = get_image_dimensions(self.logo)
            if width > 500 or height > 200:
                raise ValidationError({
                    'logo': 'A logo deve ter no máximo 500x200 pixels'
                })

    def save(self, *args, **kwargs):
        if not SiteConfiguration.objects.exists() or self.pk:
            super().save(*args, **kwargs)


class PontoForm(models.Model):
    colaborador = models.ForeignKey(
        Colaborador, 
        on_delete=models.CASCADE,
        related_name='pontos'
    )
    arquivo = models.FileField(upload_to='pontos/')
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ponto de {self.colaborador.nome} - {self.data_envio.strftime('%d/%m/%Y')}"