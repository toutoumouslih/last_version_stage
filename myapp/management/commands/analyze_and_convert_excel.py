import pandas as pd
import json
from django.core.management.base import BaseCommand
from myapp.models import DemographicData

class Command(BaseCommand):
    help = 'Analyze Excel file and convert to JSON format'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')
        parser.add_argument('--output', type=str, default='demographic_data.json', help='Output JSON file path')

    def handle(self, *args, **options):
        excel_file = options['excel_file']
        output_file = options['output']

        try:
            # Lire le fichier Excel
            df = pd.read_excel(excel_file)
            
            # Afficher les informations sur le DataFrame
            self.stdout.write(f"Colonnes du fichier Excel : {df.columns.tolist()}")
            self.stdout.write(f"Nombre de lignes : {len(df)}")
            self.stdout.write(f"Premières lignes :\n{df.head()}")
            
            # Analyser les types de données
            self.stdout.write("\nTypes de données :")
            for column in df.columns:
                self.stdout.write(f"{column}: {df[column].dtype}")
            
            # Analyser les valeurs manquantes
            self.stdout.write("\nValeurs manquantes par colonne :")
            missing_values = df.isnull().sum()
            for column, count in missing_values.items():
                self.stdout.write(f"{column}: {count} valeurs manquantes")
            
            # Convertir en JSON
            json_data = []
            for index, row in df.iterrows():
                try:
                    # Créer un dictionnaire pour chaque ligne
                    row_data = {}
                    for column in df.columns:
                        value = row[column]
                        # Convertir les types de données appropriés
                        if pd.isna(value):
                            row_data[column] = None
                        elif isinstance(value, (int, float)):
                            row_data[column] = float(value)
                        else:
                            row_data[column] = str(value)
                    
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