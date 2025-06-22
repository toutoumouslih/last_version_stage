import json
from django.core.management.base import BaseCommand
from django.db import transaction
from myapp.models import Country, Region, Department, Commune
from datetime import datetime

class Command(BaseCommand):
    help = 'Import administrative boundaries from GeoJSON file'

    def add_arguments(self, parser):
        parser.add_argument('geojson_file', type=str, help='mauritania_regions.geojson')

    def handle(self, *args, **options):
        with open(options['geojson_file'], 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Utilisation d'une transaction pour garantir l'intégrité des données
        with transaction.atomic():
            # Créer ou mettre à jour le pays (Mauritanie)
            country, _ = Country.objects.get_or_create(
                code="MR",
                defaults={
                    'name': "Mauritania",
                    'geo_json': {
                        'type': 'FeatureCollection',
                        'features': []
                    }
                }
            )

            for feature in data['features']:
                properties = feature['properties']
                geometry = feature['geometry']

                # Traiter la date (supposant le format "YYYY-MM-DD")
                date_obj = datetime.strptime(properties['date'], "%Y-%m-%d").date()
                valid_on_obj = datetime.strptime(properties['validOn'], "%Y-%m-%d").date()
                valid_to_obj = datetime.strptime(properties['validTo'], "%Y-%m-%d").date() if properties['validTo'] != "None" else None

                # Créer ou mettre à jour la région (ADM1)
                region, _ = Region.objects.get_or_create(
                    adm1_pcode=properties['ADM1_PCODE'],
                    defaults={
                        'country': country,
                        'adm0_en': properties['ADM0_EN'],
                        'adm0_pcode': properties['ADM0_PCODE'],
                        'adm1_en': properties['ADM1_EN'],
                        'geo_json': geometry,
                        'date': date_obj,
                        'valid_on': valid_on_obj,
                        'valid_to': valid_to_obj,
                        'area_sqkm': float(properties['AREA_SQKM'])
                    }
                )

                # Créer ou mettre à jour le département (ADM2)
                department, _ = Department.objects.get_or_create(
                    adm2_pcode=properties['ADM2_PCODE'],
                    defaults={
                        'region': region,
                        'adm2_en': properties['ADM2_EN'],
                        'geo_json': geometry,
                        'date': date_obj,
                        'valid_on': valid_on_obj,
                        'valid_to': valid_to_obj,
                        'area_sqkm': float(properties['AREA_SQKM'])
                    }
                )

                # Créer ou mettre à jour la commune (ADM3)
                Commune.objects.update_or_create(
                    adm3_pcode=properties['ADM3_PCODE'],
                    defaults={
                        'department': department,
                        'adm3_en': properties['ADM3_EN'],
                        'adm3_ref': properties['ADM3_REF'] if properties['ADM3_REF'] != "None" else None,
                        'real_name': properties['real_name'],
                        'geo_json': geometry,
                        'date': date_obj,
                        'valid_on': valid_on_obj,
                        'valid_to': valid_to_obj,
                        'area_sqkm': float(properties['AREA_SQKM'])
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported GeoJSON data'))