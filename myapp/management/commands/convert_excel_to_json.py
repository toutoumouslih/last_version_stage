import pandas as pd
import json
from django.core.management.base import BaseCommand
from myapp.models import DemographicData, EducationLevel

class Command(BaseCommand):
    help = 'Convert Excel file to properly structured JSON format'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')
        parser.add_argument('--output', type=str, default='demographic_data_structured.json', help='Output JSON file path')

    def handle(self, *args, **options):
        excel_file = options['excel_file']
        output_file = options['output']

        try:
            # Lire le fichier Excel en spécifiant les noms de colonnes
            df = pd.read_excel(excel_file, header=3)  # Commencer à la ligne 4 pour les en-têtes
            
            # Afficher les informations sur le DataFrame
            self.stdout.write(f"Colonnes du fichier Excel : {df.columns.tolist()}")
            self.stdout.write(f"Nombre de lignes : {len(df)}")
            
            # Convertir en JSON avec la structure appropriée
            json_data = []
            for index, row in df.iterrows():
                try:
                    # Créer un dictionnaire pour les données démographiques
                    demographic_data = {
                        "total_population": int(row['Population']),
                        "male_percentage": float(row['Masculin']),
                        "female_percentage": float(row['Feminin']),
                        "population_10_plus": int(row['Population de 10 ans et plus']),
                        "single_rate": float(row['Célibataire']),
                        "married_rate": float(row['Marié(e)']),
                        "divorced_rate": float(row['Divorcé(e)']),
                        "widowed_rate": float(row['Veuf(ve)']),
                        "school_enrollment_rate": float(row['Taux de scolarisation des 6-11 ans en 2023/2024']),
                        "illiteracy_rate_10_plus": float(row["Taux d'analphabétisme des 10 ans et plus"]),
                        "population_15_plus": int(row['Population de 15 ans et plus']),
                        "illiteracy_rate_15_plus": float(row["Taux d'analphabétisme des 15 ans et plus"])
                    }
                    
                    # Créer un dictionnaire pour les niveaux d'éducation
                    education_data = {
                        "no_education": float(row['Aucun niveau']),
                        "preschool": float(row['Préscolaire']),
                        "primary": float(row['Primaire']),
                        "middle_school": float(row['Collège']),
                        "high_school": float(row['Lycée']),
                        "university": float(row['Université'])
                    }
                    
                    # Combiner les données
                    row_data = {
                        "code": str(row['Code']).strip(),
                        "demographic_data": demographic_data,
                        "education_data": education_data
                    }
                    
                    json_data.append(row_data)
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f'Error processing row {index}: {str(e)}\nRow data: {row.to_dict()}'
                    ))

            # Sauvegarder en JSON
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            
            self.stdout.write(self.style.SUCCESS(
                f'Successfully converted Excel data to JSON. Output saved to {output_file}'
            ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error processing Excel file: {str(e)}')) 