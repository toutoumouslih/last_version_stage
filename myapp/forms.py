from django import forms
from import_export.formats import base_formats
from .models import Census

class CentralizedImportForm(forms.Form):
    census_year = forms.ModelChoiceField(
        queryset=Census.objects.all().order_by('-year'),
        label="Recensement",
        empty_label="Sélectionnez un recensement"
    )
    import_file = forms.FileField(
        label="Fichier à importer",
        help_text="Format accepté : CSV, Excel (xlsx, xls), JSON"
    )
    file_format = forms.ChoiceField(
        label="Format du fichier",
        choices=[(f.CONTENT_TYPE, f.__name__) for f in base_formats.DEFAULT_FORMATS],
        help_text="Sélectionnez le format de votre fichier"
    )