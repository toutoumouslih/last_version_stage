from .sites import custom_admin_site
from django.contrib import admin

# Remplacez l'admin par défaut
admin.site = custom_admin_site

# from .sites import custom_admin_site

# __all__ = ['custom_admin_site']