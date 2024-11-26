from django.forms.widgets import Input

class ColorPickerWidget(Input):
    input_type = 'color'
    template_name = 'django/forms/widgets/input.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({'class': 'form-control'}) 