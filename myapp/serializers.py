from rest_framework import serializers
from .models import Country, Region, Department, Commune, DemographicData, EducationLevel

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

class EducationLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationLevel
        exclude = ('id', 'demographic_data')

class DemographicDataSerializer(serializers.ModelSerializer):
    education_level = EducationLevelSerializer(source='educationlevel', read_only=True)
    class Meta:
        model = DemographicData
        fields = '__all__'
        extra_kwargs = {'education_level': {'read_only': True}}
