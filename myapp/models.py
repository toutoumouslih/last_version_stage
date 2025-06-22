from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import json
from django.contrib import admin

class Country(models.Model):
    """Modèle pour le pays (Mauritanie)"""
    name = models.CharField(max_length=100, default="Mauritania", verbose_name="Country Name")
    code = models.CharField(max_length=10, default="MR", verbose_name="Country Code")
    geo_json = models.JSONField(
        verbose_name="Geometry Data",
        default=dict,
        help_text="GeoJSON format for country boundaries"
    )
    
    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
    
    def __str__(self):
        return self.name

    def get_centroid(self):
        """Calcule le centroïde à partir du GeoJSON"""
        if not self.geo_json:
            return None
        coords = self.geo_json['coordinates'][0][0]
        lons = [c[0] for c in coords]
        lats = [c[1] for c in coords]
        return {
            'lat': sum(lats)/len(lats),
            'lon': sum(lons)/len(lons)
        }

class Region(models.Model):
    """Modèle pour les régions administratives de niveau 1 (ADM1)"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='regions')
    adm0_en = models.CharField(max_length=100, verbose_name="Country Name")
    adm0_pcode = models.CharField(max_length=10, verbose_name="Country Code")
    adm1_en = models.CharField(max_length=100, verbose_name="Region Name")
    adm1_pcode = models.CharField(max_length=10, verbose_name="Region Code")
    geo_json = models.JSONField(
        verbose_name="Geometry Data",
        help_text="GeoJSON MultiPolygon format"
    )
    date = models.DateField(verbose_name="Date of data")
    valid_on = models.DateField(verbose_name="Valid from")
    valid_to = models.DateField(null=True, blank=True, verbose_name="Valid to")
    area_sqkm = models.FloatField(verbose_name="Area in km²")
    
    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"
        ordering = ['adm1_en']
    
    def __str__(self):
        return f"{self.adm1_en} ({self.adm1_pcode})"

    def calculate_area(self):
        """Calcule la superficie à partir du GeoJSON"""
        from shapely.geometry import shape
        geom = shape(self.geo_json)
        self.area_sqkm = geom.area * 11132**2 / 1e6  # Conversion degrés carrés → km²
        self.save()

class Department(models.Model):
    """Modèle pour les départements administratifs de niveau 2 (ADM2)"""
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='departments')
    adm2_en = models.CharField(max_length=100, verbose_name="Department Name")
    adm2_pcode = models.CharField(max_length=10, verbose_name="Department Code")
    geo_json = models.JSONField(
        verbose_name="Geometry Data",
        help_text="GeoJSON MultiPolygon format"
    )
    date = models.DateField(verbose_name="Date of data")
    valid_on = models.DateField(verbose_name="Valid from")
    valid_to = models.DateField(null=True, blank=True, verbose_name="Valid to")
    area_sqkm = models.FloatField(verbose_name="Area in km²")
    
    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ['adm2_en']
    
    def __str__(self):
        return f"{self.adm2_en} ({self.adm2_pcode}) - {self.region.adm1_en}"

class Commune(models.Model):
    """Modèle pour les communes administratives de niveau 3 (ADM3)"""
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='communes')
    adm3_en = models.CharField(max_length=100, verbose_name="Commune Name")
    adm3_pcode = models.CharField(max_length=10, verbose_name="Commune Code")
    adm3_ref = models.CharField(max_length=100, null=True, blank=True, verbose_name="Commune Reference")
    real_name = models.CharField(max_length=100, verbose_name="Real Name")
    geo_json = models.JSONField(
        verbose_name="Geometry Data",
        help_text="GeoJSON MultiPolygon format"
    )
    date = models.DateField(verbose_name="Date of data")
    valid_on = models.DateField(verbose_name="Valid from")
    valid_to = models.DateField(null=True, blank=True, verbose_name="Valid to")
    area_sqkm = models.FloatField(verbose_name="Area in km²")
    
    class Meta:
        verbose_name = "Commune"
        verbose_name_plural = "Communes"
        ordering = ['adm3_en']
    
    def __str__(self):
        return f"{self.adm3_en} ({self.adm3_pcode}) - {self.department.adm2_en}"

class BoundaryPoint(models.Model):
    """Points de limite optionnels pour un contrôle plus fin"""
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='boundary_points')
    longitude = models.FloatField(
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
        verbose_name="Longitude"
    )
    latitude = models.FloatField(
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
        verbose_name="Latitude"
    )
    order = models.PositiveIntegerField(verbose_name="Point Order")
    
    class Meta:
        verbose_name = "Boundary Point"
        verbose_name_plural = "Boundary Points"
        ordering = ['commune', 'order']
    
    def __str__(self):
        return f"Point {self.order} for {self.commune.adm3_en}"

class Census(models.Model):
    """Données de recensement"""
    year = models.IntegerField(verbose_name="Année")
    is_projection = models.BooleanField(default=False, verbose_name="Est une projection")
    
    class Meta:
        verbose_name = "Recensement"
        verbose_name_plural = "Recensements"
        ordering = ['year']

    def __str__(self):
        return f"Recensement {self.year} {'(Projection)' if self.is_projection else ''}"

class DemographicData(models.Model):
    """Données démographiques par zone administrative"""
    census = models.ForeignKey(Census, on_delete=models.CASCADE, verbose_name="Recensement")
    # Liens vers les différents niveaux administratifs (un seul sera non-null)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Pays")
    region = models.ForeignKey(Region, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Région")
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Département")
    commune = models.ForeignKey(Commune, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Commune")
    
    # Données démographiques
    total_population = models.IntegerField(verbose_name="Population totale")
    male_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Pourcentage hommes")
    female_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Pourcentage femmes")
    urban_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Pourcentage urbain", default=0)
    rural_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Pourcentage rural", default=0)
    population_10_plus = models.IntegerField(verbose_name="Population de 10 ans et plus")
    
    # État matrimonial
    single_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Taux célibataires")
    married_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Taux mariés")
    divorced_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Taux divorcés")
    widowed_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Taux veufs")
    
    # Éducation
    school_enrollment_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Taux de scolarisation 6-11 ans")
    illiteracy_rate_10_plus = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Taux d'analphabétisme 10 ans et plus")
    population_15_plus = models.IntegerField(verbose_name="Population de 15 ans et plus")
    illiteracy_rate_15_plus = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Taux d'analphabétisme 15 ans et plus")

    class Meta:
        verbose_name = "Données démographiques"
        verbose_name_plural = "Données démographiques"
        unique_together = [
            ('census', 'country', 'region', 'department', 'commune')
        ]

    def __str__(self):
        if self.country:
            return f"Données {self.census.year} - {self.country}"
        elif self.region and not self.department:
            return f"Données {self.census.year} - {self.region}"
        elif self.department:
            return f"Données {self.census.year} - {self.department}"
        else:
            return f"Données {self.census.year} - {self.commune}"

class EducationLevel(models.Model):
    """Niveaux d'études"""
    demographic_data = models.OneToOneField(DemographicData, on_delete=models.CASCADE, verbose_name="Données démographiques")
    no_education = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Aucun niveau")
    preschool = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Crèche/maternelle")
    primary = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Primaire")
    middle_school = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Collège")
    high_school = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Lycée")
    university = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Université")

    class Meta:
        verbose_name = "Niveau d'éducation"
        verbose_name_plural = "Niveaux d'éducation"

    def __str__(self):
        return f"Niveaux d'éducation - {self.demographic_data}"