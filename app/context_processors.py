from .models import SiteConfiguration

def site_configuration(request):
    default_config = {
        'primary_color': '#3B82F6',
        'secondary_color': '#1D4ED8',
        'background_color': '#F3F4F6',
        'text_color': '#111827',
        'link_color': '#2563EB',
    }
    
    try:
        config = SiteConfiguration.objects.first()
        if config:
            return {'site_config': config}
    except:
        pass
    
    return {'site_config': default_config} 