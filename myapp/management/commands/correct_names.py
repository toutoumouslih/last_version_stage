from django.core.management.base import BaseCommand
from django.db import transaction
from myapp.models import Region, Department, Commune

class Command(BaseCommand):
    help = 'Corriger les noms des régions, départements et communes'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Corrections pour les régions
            region_corrections = {
                'MR01': 'Hodh Chargui',
                'MR02': 'Hodh El Gharbi',
                'MR03': 'Assaba',
                'MR04': 'Gorgol',
                'MR05': 'Brakna',
                'MR06': 'Trarza',
                'MR07': 'Adrar',
                'MR08': 'Dakhlet Nouadhibou',
                'MR09': 'Tagant',
                'MR10': 'Guidimakha',
                'MR11': 'Tiris Zemmour',
                'MR12': 'Inchiri',
                'MR13': 'Nouakchott Ouest',
                'MR14': 'Nouakchott Nord',
                'MR15': 'Nouakchott Sud',
            }

            # Corrections pour les départements
            department_corrections = {
                'MR011': 'Amourj',
                'MR012': 'Bassikounou',
                'MR013': 'Djiguenni',
                'MR014': 'Néma',
                'MR015': 'Oualata',
                'MR016': 'Timbédra',
                'MR017': "N'Beiket Lehwach",
                'MR018': 'Adel Bagrou',
                'MR021': 'Aioun',
                'MR022': 'Kobeni',
                'MR023': 'Tamchekett',
                'MR024': 'Tintane',
                'MR025': 'Touil',
                'MR031': 'Barkeol',
                'MR032': 'Boumdeid',
                'MR033': 'Guerou',
                'MR034': 'Kankossa',
                'MR035': 'Kiffa',
                'MR041': 'Kaédi',
                'MR042': 'Maghama',
                'MR043': "M'Bout",
                'MR044': 'Monguel',
                'MR045': 'Lexeibe 1',
                'MR051': 'Aleg',
                'MR052': 'Bababé',
                'MR053': 'Boghé',
                'MR054': 'Magta Lahjar',
                'MR055': "M'Bagne",
                'MR056': 'Maal',
                'MR061': 'Boutilimit',
                'MR062': 'Keur Macène',
                'MR063': 'Mederdra',
                'MR064': 'Ouad Naga',
                'MR065': "R'Kiz",
                'MR066': 'Rosso',
                'MR067': 'Tekane',
                'MR071': 'Aoujeft',
                'MR072': 'Atar',
                'MR073': 'Chinguetti',
                'MR074': 'Ouadane',
                'MR081': 'Nouadhibou',
                'MR082': 'Chami',
                'MR091': 'Moudjeria',
                'MR092': 'Tichit',
                'MR093': 'Tidjikja',
                'MR101': 'Ould Yengé',
                'MR102': 'Sélibaby',
                'MR103': 'Ghabou',
                'MR104': 'Wompou',
                'MR111': 'Bir Moghrein',
                'MR112': "F'Deirick",
                'MR113': 'Zouérate',
                
                # Inchiri (MR12)
                'MR121': 'Akjoujt',
                'MR122': 'Bennichab',
                
                # Nouakchott Ouest (MR13)
                'MR131': 'Tevragh-Zeina',
                'MR132': 'Ksar',
                'MR133': 'Sebkha',
                
                # Nouakchott Nord (MR14)
                'MR141': 'Dar Naim',
                'MR142': 'Teyarett',
                'MR143': 'Toujounine',
                
                # Nouakchott Sud (MR15)
                'MR151': 'El Mina',
                'MR152': 'Arafat',
                'MR153': 'Riyad'
            }

            # Correction des noms des régions
            for region in Region.objects.all():
                if region.adm1_pcode in region_corrections:
                    old_name = region.adm1_en
                    region.adm1_en = region_corrections[region.adm1_pcode]
                    region.save()
                    
                    self.stdout.write(self.style.SUCCESS(
                        f'Région mise à jour: {old_name} -> {region.adm1_en}'
                    ))

            # Correction des noms des départements
            for department in Department.objects.all():
                if department.adm2_pcode in department_corrections:
                    old_name = department.adm2_en
                    department.adm2_en = department_corrections[department.adm2_pcode]
                    department.save()
                    
                    self.stdout.write(self.style.SUCCESS(
                        f'Département mis à jour: {old_name} -> {department.adm2_en}'
                    ))
                else:
                    self.stdout.write(self.style.WARNING(
                        f'Code département non trouvé dans les corrections: {department.adm2_pcode}'
                    ))

            self.stdout.write(self.style.SUCCESS('Correction des noms des départements terminée'))

            self.stdout.write(self.style.SUCCESS('Correction des noms terminée')) 