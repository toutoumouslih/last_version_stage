import pandas as pd
from decimal import Decimal
from django.core.management.base import BaseCommand
from myapp.models import Census, DemographicData, EducationLevel, Region, Department, Commune

class Command(BaseCommand):
    help = 'Import demographic data from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')
        parser.add_argument('--year', type=int, default=2023, help='Census year')

    def handle(self, *args, **options):
        excel_file = options['excel_file']
        year = options['year']

        try:
            # Lire le fichier Excel
            df = pd.read_excel(excel_file)
            
            # Afficher les informations sur le DataFrame
            self.stdout.write(f"Colonnes du fichier Excel : {df.columns.tolist()}")
            self.stdout.write(f"Nombre de lignes : {len(df)}")
            self.stdout.write(f"Premières lignes :\n{df.head()}")
            
            # Créer ou récupérer le recensement
            census, created = Census.objects.get_or_create(year=year)
            
            # Supprimer les anciennes données si elles existent
            DemographicData.objects.filter(census=census).delete()
            
            # Parcourir les lignes du DataFrame
            for index, row in df.iterrows():
                try:
                    if pd.isna(row['Code']):
                        continue
                        
                    code = str(row['Code']).strip()
                    self.stdout.write(f"Traitement de la ligne {index}, code : {code}")
                    
                    # Déterminer le niveau administratif
                    if len(code) == 2:  # Région
                        admin_object = Region.objects.get(adm1_pcode=code)
                        kwargs = {'region': admin_object}
                    elif len(code) == 4:  # Département
                        admin_object = Department.objects.get(adm2_pcode=code)
                        kwargs = {
                            'region': admin_object.region,
                            'department': admin_object
                        }
                    else:  # Commune
                        admin_object = Commune.objects.get(adm3_pcode=code)
                        kwargs = {
                            'region': admin_object.department.region,
                            'department': admin_object.department,
                            'commune': admin_object
                        }

                    # Créer les données démographiques
                    demo_data = DemographicData.objects.create(
                        census=census,
                        total_population=int(row['Population']),
                        male_percentage=Decimal(str(row['Masculin'])),
                        female_percentage=Decimal(str(row['Feminin'])),
                        population_10_plus=int(row['Population de 10 ans et plus']),
                        single_rate=Decimal(str(row['Célibataire'])),
                        married_rate=Decimal(str(row['Marié(e)'])),
                        divorced_rate=Decimal(str(row['Divorcé(e)'])),
                        widowed_rate=Decimal(str(row['Veuf(ve)'])),
                        school_enrollment_rate=Decimal(str(row['Taux de scolarisation des 6-11 ans en 2023/2024'])),
                        illiteracy_rate_10_plus=Decimal(str(row["Taux d'analphabétisme des 10 ans et plus"])),
                        population_15_plus=int(row['Population de 15 ans et plus']),
                        illiteracy_rate_15_plus=Decimal(str(row["Taux d'analphabétisme des 15 ans et plus"])),
                        **kwargs
                    )

                    # Créer les niveaux d'éducation
                    EducationLevel.objects.create(
                        demographic_data=demo_data,
                        no_education=Decimal(str(row['Aucun niveau'])),
                        preschool=Decimal(str(row['Préscolaire'])),
                        primary=Decimal(str(row['Primaire'])),
                        middle_school=Decimal(str(row['Collège'])),
                        high_school=Decimal(str(row['Lycée'])),
                        university=Decimal(str(row['Université']))
                    )

                    self.stdout.write(self.style.SUCCESS(
                        f'Successfully imported data for {admin_object}'
                    ))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f'Error importing row {index}: {str(e)}\nRow data: {row.to_dict()}'
                    ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading Excel file: {str(e)}')) 