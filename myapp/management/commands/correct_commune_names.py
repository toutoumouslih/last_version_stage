from django.core.management.base import BaseCommand
from django.db import transaction
from myapp.models import Commune

class Command(BaseCommand):
    help = 'Corriger les noms des communes'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Dictionnaire des corrections pour les communes
            commune_corrections = {
                # Corrections existantes
                'MR01401': 'Néma',
                'MR01402': 'Achmine',
                'MR01403': 'Jreif',
                'MR01404': 'Bangou',
                'MR01405': 'Hassi Etile',
                'MR01406': 'Oum Avnadech',
                'MR01407': 'El Mabrouk',
                'MR01408': 'Beribavat',
                'MR01409': 'Noual',
                'MR01410': 'Agoueinit',
                
                # Nouvelles corrections
                'MR01605': 'Hassi M\'Hadi',
                'MR01712': 'N\'Beiket Lehwach',
                'MR02401': 'Tintane',
                'MR03107': 'R\'Dheidhie',
                'MR06104': 'N\'Teichet',
                'MR09102': 'N\'Beike',
                'MR10101': 'Ould Yengé',
                'MR10202': 'Ould M\'Bonny',
                'MR13201': 'Tevragh Zeina',
                
                # Corrections pour Timbédra
                'MR01601': 'Timbédra',
                'MR01602': 'Touil',
                'MR01603': 'Koumbi Saleh',
                'MR01604': 'Bousteila',
                
                # Corrections pour les noms avec accents
                'MR05203': 'Aéré M\'Bar',
                'MR04102': 'Néré Walo',
                'MR04105': 'Tifondé Civé',
                'MR04203': 'Dolol Civé',
                'MR04207': 'Sagné',
                'MR04304': 'N\'Djadjbenni Gandéga',
                'MR04402': 'Bathet Moït',
                
                # Corrections pour les noms avec apostrophes
                'MR04301': 'M\'Bout',
                'MR05501': 'M\'Bagne',
                'MR06202': 'N\'Diago',
                'MR11201': 'F\'Deirick',
                'MR07103': 'N\'Teirguent',
                'MR06501': 'R\'Kiz',
                
                # Corrections pour les noms avec Aïn
                'MR07202': 'Aïn Ehel Taya',
                'MR07302': 'Aïn Savra',
                'MR02404': 'Aïn Varbe',
                
                # Corrections pour Keur Macène
                'MR06201': 'Keur Macène',
                'MR06202': 'N\'Diago',
                'MR06203': 'M\'Balal'
            }

            # Correction des noms des communes
            for commune in Commune.objects.all():
                if commune.adm3_pcode in commune_corrections:
                    old_name = commune.adm3_en
                    commune.adm3_en = commune_corrections[commune.adm3_pcode]
                    commune.save()
                    
                    self.stdout.write(self.style.SUCCESS(
                        f'Commune mise à jour: {old_name} -> {commune.adm3_en}'
                    ))

            self.stdout.write(self.style.SUCCESS('Correction des noms des communes terminée')) 