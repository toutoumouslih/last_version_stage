from django.core.management.base import BaseCommand
from django.db import transaction
from myapp.models import Region, Department, Commune, Census, DemographicData
from decimal import Decimal
import json
import os

class Command(BaseCommand):
    help = 'Import demographic data from JSON file'

    def handle(self, *args, **options):
        # Chemin vers le fichier JSON
        json_file = os.path.join(os.path.dirname(__file__), 'demographic_data_structured.json')
        
        # Créer ou récupérer le recensement 2023
        census, created = Census.objects.get_or_create(
            year=2023,
            is_projection=False
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Created census for year 2023'))
        else:
            self.stdout.write(self.style.SUCCESS('Using existing census for year 2023'))

        with transaction.atomic():
            # Supprimer les données existantes pour le recensement 2023
            DemographicData.objects.filter(census=census).delete()
            self.stdout.write(self.style.SUCCESS('Deleted existing demographic data'))

            # Lire le fichier JSON
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Parcourir les données
            for code, values in data.items():
                if code == "Code":  # Ignorer la clé "Code"
                    continue

                try:
                    # Déterminer le niveau administratif par la longueur du code
                    if len(code) == 2:  # Région
                        admin_object = Region.objects.get(adm1_pcode=f"MR{code}")
                        kwargs = {'region': admin_object}
                    elif len(code) == 3:  # Département
                        admin_object = Department.objects.get(adm2_pcode=f"MR{code}")
                        kwargs = {
                            'region': admin_object.region,
                            'department': admin_object
                        }
                    elif len(code) == 5:  # Commune
                        admin_object = Commune.objects.get(adm3_pcode=f"MR{code}")
                        kwargs = {
                            'region': admin_object.department.region,
                            'department': admin_object.department,
                            'commune': admin_object
                        }
                    else:
                        self.stdout.write(self.style.WARNING(f'Code invalide: {code}'))
                        continue

                    # Créer les données démographiques
                    DemographicData.objects.create(
                        census=census,
                        **kwargs,
                        total_population=int(float(values['population'])),
                        male_percentage=Decimal(str(float(values['male']) * 100)),
                        female_percentage=Decimal(str(float(values['female']) * 100)),
                        population_10_plus=int(float(values['population_10_plus'])),
                        single_rate=Decimal(str(float(values['single_rate']) * 100)),
                        married_rate=Decimal(str(float(values['married_rate']) * 100)),
                        divorced_rate=Decimal(str(float(values['divorced_rate']) * 100)),
                        widowed_rate=Decimal(str(float(values['widowed_rate']) * 100)),
                        school_enrollment_rate=Decimal(str(float(values['school_enrollment_rate']) * 100)),
                        illiteracy_rate_10_plus=Decimal(str(float(values['illiteracy_rate_10_plus']) * 100)),
                        population_15_plus=int(float(values['population_15_plus'])),
                        illiteracy_rate_15_plus=Decimal(str(float(values['illiteracy_rate_15_plus']) * 100))
                    )

                    self.stdout.write(self.style.SUCCESS(f'Successfully imported data for {values["name"]}'))

                except Region.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Region with code MR{code} not found'))
                except Department.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Department with code MR{code} not found'))
                except Commune.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Commune with code MR{code} not found'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error importing data for code {code}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Successfully imported all demographic data')) 