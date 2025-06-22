from rest_framework import serializers
from .models import Country, Region, Department, Commune, DemographicData

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class CommuneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commune
        fields = '__all__'

class DemographicDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemographicData
        fields = '__all__'
