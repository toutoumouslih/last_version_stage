from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import path
from myapp.views import CentralizedImportView, download_template

class CustomAdminSite(AdminSite):
    site_header = "Administration des Données Démographiques"
    site_title = "Tableau de Bord Admin"
    index_title = "Gestion des Données"
    site_url = "/"
    index_template = 'admin/index.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-all-data/',
                self.admin_view(CentralizedImportView.as_view()),
                name='import_all_data'),
            path('download-all-template/',
                self.admin_view(download_template),
                name='download_all_template'),
        ]
        return custom_urls + urls

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        return sorted(app_list, key=lambda x: x['name'])

custom_admin_site = CustomAdminSite(name='custom_admin')

# Enregistrement des modèles de base
custom_admin_site.register(Group)
custom_admin_site.register(Permission)
custom_admin_site.register(ContentType)