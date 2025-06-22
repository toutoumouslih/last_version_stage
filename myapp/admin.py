from django.contrib import admin
from django.urls import path
from import_export.formats import base_formats
from .models import (
    DemographicData, Census, 
    Country, Region, Department, Commune, EducationLevel
)
from .resources import DemographicDataResource, EducationLevelResource
from .views import CentralizedImportView, download_template
from .admindossier.sites import custom_admin_site

class DemographicDataAdmin(admin.ModelAdmin):
    resource_class = DemographicDataResource
    
    # Configuration de l'affichage
    list_display = [
        'id', 'census', 'country', 'region',
        'department', 'commune', 'total_population'
    ]
    list_filter = ['census', 'country', 'region']
    search_fields = [
        'country__name', 
        'region__adm1_en',
        'department__adm2_en',
        'commune__adm3_en'
    ]
    list_per_page = 50

class CensusAdmin(admin.ModelAdmin):
    list_display = ['year', 'is_projection']
    search_fields = ['year']

class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name']

class RegionAdmin(admin.ModelAdmin):
    list_display = ['adm1_en', 'adm1_pcode', 'country']
    list_filter = ['country']
    raw_id_fields = ['country']

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['adm2_en', 'adm2_pcode', 'region']
    list_filter = ['region']
    raw_id_fields = ['region']

class CommuneAdmin(admin.ModelAdmin):
    list_display = ['adm3_en', 'adm3_pcode', 'department']
    list_filter = ['department']
    raw_id_fields = ['department']

# Nouvelle classe d'administration pour EducationLevel
class EducationLevelAdmin(admin.ModelAdmin):
    resource_class = EducationLevelResource
    list_display = [
        'demographic_data', 'no_education', 'preschool', 
        'primary', 'middle_school', 'high_school', 'university'
    ]
    list_filter = ['demographic_data__census', 'demographic_data__region']
    search_fields = [
        'demographic_data__commune__adm3_en',
        'demographic_data__department__adm2_en',
        'demographic_data__region__adm1_en',
    ]
    raw_id_fields = ['demographic_data']

# Enregistrement des modèles avec le site d'admin personnalisé
custom_admin_site.register(DemographicData, DemographicDataAdmin)
custom_admin_site.register(Census, CensusAdmin)
custom_admin_site.register(Country, CountryAdmin)
custom_admin_site.register(Region, RegionAdmin)
custom_admin_site.register(Department, DepartmentAdmin)
custom_admin_site.register(Commune, CommuneAdmin)
custom_admin_site.register(EducationLevel, EducationLevelAdmin)