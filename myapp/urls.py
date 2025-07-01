# from django.urls import path
# from . import views

# urlpatterns = [
#     path('regions/', views.get_regions, name='get_regions'),
#     path('departments/', views.get_departments, name='get_departments'),
#     path('departments/<int:region_id>/', views.get_departments, name='get_region_departments'),
#     path('communes/', views.get_communes, name='get_communes'),
#     path('communes/<int:department_id>/', views.get_communes, name='get_department_communes'),
#     path('statistics/', views.get_statistics, name='get_statistics'),
# ]



from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CountryViewSet, RegionViewSet, DepartmentViewSet, CommuneViewSet,
    DemographicDataListCreateView, DemographicDataDetailView,
    export_all_data, export_zone_data, CentralizedImportView, download_template,
    CensusYearsView
)

router = DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'regions', RegionViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'communes', CommuneViewSet)

urlpatterns = [
    # URLs de l'API REST
    path('api/', include(router.urls)),
    path('api/demographics/', DemographicDataListCreateView.as_view(), name='demographics-list-create'),
    path('api/demographics/<int:pk>/', DemographicDataDetailView.as_view(), name='demographics-detail'),
    path('api/census-years/', CensusYearsView.as_view(), name='census-years'),
    
    # URLs pour l'export
    path('export-all-data/', export_all_data, name='export_all_data'),
    path('export-zone-data/<int:zone_id>/<str:zone_type>/', export_zone_data, name='export_zone_data'),
]  
