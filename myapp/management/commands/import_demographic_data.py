import json
from django.core.management.base import BaseCommand
from django.db import transaction
from myapp.models import Census, DemographicData, EducationLevel, Region, Department, Commune
from decimal import Decimal
from .demographic_data import DEMOGRAPHIC_DATA

class Command(BaseCommand):
    help = 'Import demographic data from the 2023 census'

    def add_arguments(self, parser):
        parser.add_argument('--year', type=int, default=2023)
        parser.add_argument('--force', action='store_true', help='Force reimport by deleting existing data')

    def handle(self, *args, **options):
        year = options['year']
        force = options['force']
        
        try:
            with transaction.atomic():
                # Supprimer les données existantes si --force est utilisé
                if force:
                    Census.objects.filter(year=year).delete()
                    self.stdout.write(self.style.SUCCESS(f'Deleted existing census data for year {year}'))

                # Create or get census
                census, created = Census.objects.get_or_create(year=year)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created new census for year {year}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Using existing census for year {year}'))

                # Importer les données pour chaque région
                for region_code, region_data in DEMOGRAPHIC_DATA.items():
                    try:
                        region = Region.objects.get(adm1_pcode=region_code)
                        
                        # Créer ou mettre à jour les données démographiques de la région
                        region_demo, created = DemographicData.objects.update_or_create(
                            census=census,
                            region=region,
                            defaults={
                                'total_population': region_data['population'],
                                'male_percentage': region_data['male'],
                                'female_percentage': region_data['female'],
                                'urban_percentage': region_data['urban'],
                                'rural_percentage': region_data['rural'],
                                'population_10_plus': int(region_data['population'] * 0.75),  # Estimation
                                'population_15_plus': int(region_data['population'] * 0.65),  # Estimation
                                'school_enrollment_rate': Decimal('65.0'),  # Valeur par défaut
                                'illiteracy_rate_10_plus': Decimal('35.0'),  # Valeur par défaut
                                'illiteracy_rate_15_plus': Decimal('38.0'),  # Valeur par défaut
                                'single_rate': Decimal('39.4'),  # Valeur par défaut
                                'married_rate': Decimal('52.3'),  # Valeur par défaut
                                'divorced_rate': Decimal('3.1'),  # Valeur par défaut
                                'widowed_rate': Decimal('5.2')  # Valeur par défaut
                            }
                        )
                        self.stdout.write(self.style.SUCCESS(f'{"Created" if created else "Updated"} data for region {region.adm1_en}'))

                        # Importer les données pour chaque département de la région
                        for dept_code, dept_data in region_data['departments'].items():
                            try:
                                dept = Department.objects.get(adm2_pcode=dept_code)
                                
                                # Créer ou mettre à jour les données démographiques du département
                                dept_demo, created = DemographicData.objects.update_or_create(
                                    census=census,
                                    region=region,
                                    department=dept,
                                    defaults={
                                        'total_population': dept_data['population'],
                                        'male_percentage': dept_data['male'],
                                        'female_percentage': dept_data['female'],
                                        'urban_percentage': dept_data['urban'],
                                        'rural_percentage': dept_data['rural'],
                                        'population_10_plus': int(dept_data['population'] * 0.75),  # Estimation
                                        'population_15_plus': int(dept_data['population'] * 0.65),  # Estimation
                                        'school_enrollment_rate': Decimal('65.0'),  # Valeur par défaut
                                        'illiteracy_rate_10_plus': Decimal('35.0'),  # Valeur par défaut
                                        'illiteracy_rate_15_plus': Decimal('38.0'),  # Valeur par défaut
                                        'single_rate': Decimal('39.4'),  # Valeur par défaut
                                        'married_rate': Decimal('52.3'),  # Valeur par défaut
                                        'divorced_rate': Decimal('3.1'),  # Valeur par défaut
                                        'widowed_rate': Decimal('5.2')  # Valeur par défaut
                                    }
                                )
                                self.stdout.write(self.style.SUCCESS(f'{"Created" if created else "Updated"} data for department {dept.adm2_en}'))
                            except Department.DoesNotExist:
                                self.stdout.write(self.style.WARNING(f'Department {dept_code} not found'))
                            except Exception as e:
                                self.stdout.write(self.style.ERROR(f'Error importing department {dept_code}: {str(e)}'))
                    
                    except Region.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'Region {region_code} not found'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error importing region {region_code}: {str(e)}'))

                self.stdout.write(self.style.SUCCESS('Successfully imported demographic data'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {str(e)}'))
            raise