from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import DemographicData, EducationLevel, Census, Country, Region, Department, Commune

class DemographicDataResource(resources.ModelResource):
    census = fields.Field(
        column_name='census',
        attribute='census',
        widget=ForeignKeyWidget(Census, 'pk')
    )
    
    country = fields.Field(
        column_name='country',
        attribute='country',
        widget=ForeignKeyWidget(Country, 'pk')
    )
    
    region = fields.Field(
        column_name='region',
        attribute='region',
        widget=ForeignKeyWidget(Region, 'pk')
    )
    
    department = fields.Field(
        column_name='department',
        attribute='department',
        widget=ForeignKeyWidget(Department, 'pk')
    )
    
    commune = fields.Field(
        column_name='commune',
        attribute='commune',
        widget=ForeignKeyWidget(Commune, 'pk')
    )

    class Meta:
        model = DemographicData
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('census', 'country', 'region', 'department', 'commune')
        exclude = ('id',)

    def before_import_row(self, row, **kwargs):
        print(f"DEBUG: Row in before_import_row (DemographicDataResource): {row}")
        # La conversion des PKs en instances sera gérée par ForeignKeyWidget
        # Cette partie du code n'est plus nécessaire pour la conversion
        for field in ['country_code', 'region_code', 'department_code', 'commune_code']:
            if field in row and not row[field]:
                row[field] = None

class EducationLevelResource(resources.ModelResource):
    demographic_data = fields.Field(
        column_name='demographic_data',
        attribute='demographic_data',
        widget=ForeignKeyWidget(DemographicData, 'pk')
    )

    class Meta:
        model = EducationLevel
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('demographic_data',)
        exclude = ('id',)

    def before_import_row(self, row, **kwargs):
        print(f"DEBUG: Row in before_import_row (EducationLevelResource): {row}")
        # La conversion de PK en instance sera gérée par ForeignKeyWidget
        # Cette partie du code n'est plus nécessaire pour la conversion