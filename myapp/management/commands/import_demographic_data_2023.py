from django.core.management.base import BaseCommand
from django.db import transaction
from myapp.models import Region, Department, Commune, Census, DemographicData, EducationLevel, Country
from decimal import Decimal

class Command(BaseCommand):
    help = 'Import demographic data from the 2023 census'

    def handle(self, *args, **options):
        # Créer ou récupérer le recensement 2023
        census, created = Census.objects.get_or_create(
            year=2023,
            is_projection=False
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created census for year 2023'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Using existing census for year 2023'))

        with transaction.atomic():
            # Supprimer les données existantes pour le recensement 2023
            DemographicData.objects.filter(census=census).delete()
            self.stdout.write(self.style.SUCCESS('Deleted existing demographic data'))

            # Définir les données démographiques nationales
            national_data = {
                'total_population': 4000000,
                'male_percentage': 48.5,
                'female_percentage': 51.5,
                'urban_percentage': 50.0,
                'rural_percentage': 50.0,
                'population_10_plus': 3000000,
                'single_rate': 45.0,
                'married_rate': 48.0,
                'divorced_rate': 4.0,
                'widowed_rate': 3.0,
                'school_enrollment_rate': 95.0,
                'illiteracy_rate_10_plus': 30.0,
                'population_15_plus': 2500000,
                'illiteracy_rate_15_plus': 32.0,
                'education_levels': {
                    'no_education': 15.0,
                    'preschool': 1.0,
                    'primary': 68.0,
                    'middle_school': 18.0,
                    'high_school': 6.0,
                    'university': 2.0
                }
            }

            # Créer les données démographiques nationales
            demographic_data = DemographicData.objects.create(
                census=census,
                country=Country.objects.first(),
                total_population=national_data['total_population'],
                male_percentage=national_data['male_percentage'],
                female_percentage=national_data['female_percentage'],
                urban_percentage=national_data['urban_percentage'],
                rural_percentage=national_data['rural_percentage'],
                population_10_plus=national_data['population_10_plus'],
                single_rate=national_data['single_rate'],
                married_rate=national_data['married_rate'],
                divorced_rate=national_data['divorced_rate'],
                widowed_rate=national_data['widowed_rate'],
                school_enrollment_rate=national_data['school_enrollment_rate'],
                illiteracy_rate_10_plus=national_data['illiteracy_rate_10_plus'],
                population_15_plus=national_data['population_15_plus'],
                illiteracy_rate_15_plus=national_data['illiteracy_rate_15_plus']
            )

            # Créer les niveaux d'éducation pour les données nationales
            EducationLevel.objects.create(
                demographic_data=demographic_data,
                no_education=national_data['education_levels']['no_education'],
                preschool=national_data['education_levels']['preschool'],
                primary=national_data['education_levels']['primary'],
                middle_school=national_data['education_levels']['middle_school'],
                high_school=national_data['education_levels']['high_school'],
                university=national_data['education_levels']['university']
            )

            # Parcourir les régions
            for region in Region.objects.all():
                try:
                    # Récupérer les données de la région
                    region_data = self.get_region_data(region.adm1_pcode)
                    if not region_data:
                        self.stdout.write(
                            self.style.WARNING(
                                f'No data found for region {region.adm1_pcode}'
                            )
                        )
                        continue

                    # Créer les données démographiques pour la région
                    demographic_data = DemographicData.objects.create(
                        census=census,
                        region=region,
                        total_population=region_data['total_population'],
                        male_percentage=region_data['male_percentage'],
                        female_percentage=region_data['female_percentage'],
                        urban_percentage=region_data['urban_percentage'],
                        rural_percentage=region_data['rural_percentage'],
                        population_10_plus=region_data['population_10_plus'],
                        single_rate=region_data['single_rate'],
                        married_rate=region_data['married_rate'],
                        divorced_rate=region_data['divorced_rate'],
                        widowed_rate=region_data['widowed_rate'],
                        school_enrollment_rate=region_data['school_enrollment_rate'],
                        illiteracy_rate_10_plus=region_data['illiteracy_rate_10_plus'],
                        population_15_plus=region_data['population_15_plus'],
                        illiteracy_rate_15_plus=region_data['illiteracy_rate_15_plus']
                    )

                    # Créer les niveaux d'éducation pour la région
                    EducationLevel.objects.create(
                        demographic_data=demographic_data,
                        no_education=region_data['education_levels']['no_education'],
                        preschool=region_data['education_levels']['preschool'],
                        primary=region_data['education_levels']['primary'],
                        middle_school=region_data['education_levels']['middle_school'],
                        high_school=region_data['education_levels']['high_school'],
                        university=region_data['education_levels']['university']
                    )

                    self.stdout.write(self.style.SUCCESS(f'Created data for region {region.adm1_en}'))

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Error processing region {region.adm1_pcode}: {str(e)}'
                        )
                    )

            # Parcourir les départements
            for department in Department.objects.all():
                department_data = self.get_department_data(department.adm2_pcode)
                if department_data:
                    try:
                        # Créer les données démographiques pour le département
                        demographic_data = DemographicData.objects.create(
                            census=census,
                            region=department.region,
                            department=department,
                            total_population=department_data['total_population'],
                            male_percentage=department_data['male_percentage'],
                            female_percentage=department_data['female_percentage'],
                            urban_percentage=department_data['urban_percentage'],
                            rural_percentage=department_data['rural_percentage'],
                            population_10_plus=department_data['population_10_plus'],
                            single_rate=department_data['single_rate'],
                            married_rate=department_data['married_rate'],
                            divorced_rate=department_data['divorced_rate'],
                            widowed_rate=department_data['widowed_rate'],
                            school_enrollment_rate=department_data['school_enrollment_rate'],
                            illiteracy_rate_10_plus=department_data['illiteracy_rate_10_plus'],
                            population_15_plus=department_data['population_15_plus'],
                            illiteracy_rate_15_plus=department_data['illiteracy_rate_15_plus']
                        )

                        # Créer les niveaux d'éducation pour le département
                        EducationLevel.objects.create(
                            demographic_data=demographic_data,
                            no_education=department_data['education_levels']['no_education'],
                            preschool=department_data['education_levels']['preschool'],
                            primary=department_data['education_levels']['primary'],
                            middle_school=department_data['education_levels']['middle_school'],
                            high_school=department_data['education_levels']['high_school'],
                            university=department_data['education_levels']['university']
                        )

                        self.stdout.write(self.style.SUCCESS(f'Created data for department {department.adm2_en}'))

                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f'Error processing department {department.adm2_pcode}: {str(e)}'
                            )
                        )
                else:
                    self.stdout.write(self.style.WARNING(f'No data found for department {department.adm2_pcode}'))

            # Parcourir les communes
            for commune in Commune.objects.all():
                commune_data = self.get_commune_data(commune.real_name)
                if commune_data:
                    try:
                        # Créer les données démographiques pour la commune
                        demographic_data = DemographicData.objects.create(
                            census=census,
                            region=commune.department.region,
                            department=commune.department,
                            commune=commune,
                            total_population=commune_data['total_population'],
                            male_percentage=commune_data['male_percentage'],
                            female_percentage=commune_data['female_percentage'],
                            urban_percentage=commune_data['urban_percentage'],
                            rural_percentage=commune_data['rural_percentage'],
                            population_10_plus=commune_data['population_10_plus'],
                            single_rate=commune_data['single_rate'],
                            married_rate=commune_data['married_rate'],
                            divorced_rate=commune_data['divorced_rate'],
                            widowed_rate=commune_data['widowed_rate'],
                            school_enrollment_rate=commune_data['school_enrollment_rate'],
                            illiteracy_rate_10_plus=commune_data['illiteracy_rate_10_plus'],
                            population_15_plus=commune_data['population_15_plus'],
                            illiteracy_rate_15_plus=commune_data['illiteracy_rate_15_plus']
                        )

                        # Créer les niveaux d'éducation pour la commune
                        EducationLevel.objects.create(
                            demographic_data=demographic_data,
                            no_education=commune_data['education_levels']['no_education'],
                            preschool=commune_data['education_levels']['preschool'],
                            primary=commune_data['education_levels']['primary'],
                            middle_school=commune_data['education_levels']['middle_school'],
                            high_school=commune_data['education_levels']['high_school'],
                            university=commune_data['education_levels']['university']
                        )

                        self.stdout.write(self.style.SUCCESS(f'Created data for commune {commune.real_name}'))

                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f'Error processing commune {commune.real_name}: {str(e)}'
                            )
                        )
                else:
                    self.stdout.write(self.style.WARNING(f'No data found for commune {commune.real_name}'))

        self.stdout.write(self.style.SUCCESS('Successfully imported demographic data'))

    def get_region_data(self, region_code):
        # Dictionnaire des données démographiques par région
        region_data = {
            'MR01': {  # Hodh Chargui
                'total_population': 625643.74,
                'male_percentage': Decimal('46.09'),
                'female_percentage': Decimal('53.91'),
                'urban_percentage': Decimal('50.0'),
                'rural_percentage': Decimal('50.0'),
                'population_10_plus': 425586.00,
                'single_rate': Decimal('45.36'),
                'married_rate': Decimal('45.53'),
                'divorced_rate': Decimal('5.02'),
                'widowed_rate': Decimal('4.09'),
                'school_enrollment_rate': Decimal('93.14'),
                'illiteracy_rate_10_plus': Decimal('37.47'),
                'population_15_plus': 340045.92,
                'illiteracy_rate_15_plus': Decimal('38.27'),
                'education_levels': {
                    'no_education': Decimal('19.61'),
                    'preschool': Decimal('2.08'),
                    'primary': Decimal('80.69'),
                    'middle_school': Decimal('11.44'),
                    'high_school': Decimal('3.89'),
                    'university': Decimal('1.11')
                }
            },
            'MR02': {  # Hodh El Gharbi
                'total_population': 403090.69,
                'male_percentage': Decimal('46.36'),
                'female_percentage': Decimal('53.64'),
                'urban_percentage': Decimal('50.0'),
                'rural_percentage': Decimal('50.0'),
                'population_10_plus': 275374.00,
                'single_rate': Decimal('46.26'),
                'married_rate': Decimal('45.85'),
                'divorced_rate': Decimal('4.24'),
                'widowed_rate': Decimal('3.65'),
                'school_enrollment_rate': Decimal('94.30'),
                'illiteracy_rate_10_plus': Decimal('40.36'),
                'population_15_plus': 219312.85,
                'illiteracy_rate_15_plus': Decimal('41.56'),
                'education_levels': {
                    'no_education': Decimal('18.33'),
                    'preschool': Decimal('1.57'),
                    'primary': Decimal('76.22'),
                    'middle_school': Decimal('13.40'),
                    'high_school': Decimal('5.64'),
                    'university': Decimal('2.34')
                }
            },
            'MR03': {  # Assaba
                'total_population': 451804.36,
                'male_percentage': Decimal('44.97'),
                'female_percentage': Decimal('55.03'),
                'urban_percentage': Decimal('50.0'),
                'rural_percentage': Decimal('50.0'),
                'population_10_plus': 308456.00,
                'single_rate': Decimal('48.52'),
                'married_rate': Decimal('42.07'),
                'divorced_rate': Decimal('5.34'),
                'widowed_rate': Decimal('4.07'),
                'school_enrollment_rate': Decimal('94.87'),
                'illiteracy_rate_10_plus': Decimal('32.16'),
                'population_15_plus': 241203.79,
                'illiteracy_rate_15_plus': Decimal('33.47'),
                'education_levels': {
                    'no_education': Decimal('20.05'),
                    'preschool': Decimal('1.49'),
                    'primary': Decimal('75.94'),
                    'middle_school': Decimal('14.78'),
                    'high_school': Decimal('5.86'),
                    'university': Decimal('1.53')
                }
            },
            'MR04': {  # Gorgol
                'total_population': 442490.44,
                'male_percentage': Decimal('47.60'),
                'female_percentage': Decimal('52.40'),
                'urban_percentage': Decimal('50.0'),
                'rural_percentage': Decimal('50.0'),
                'population_10_plus': 301456.00,
                'single_rate': Decimal('50.79'),
                'married_rate': Decimal('42.74'),
                'divorced_rate': Decimal('2.55'),
                'widowed_rate': Decimal('3.91'),
                'school_enrollment_rate': Decimal('96.96'),
                'illiteracy_rate_10_plus': Decimal('47.23'),
                'population_15_plus': 234041.47,
                'illiteracy_rate_15_plus': Decimal('48.82'),
                'education_levels': {
                    'no_education': Decimal('14.69'),
                    'preschool': Decimal('3.76'),
                    'primary': Decimal('70.83'),
                    'middle_school': Decimal('16.54'),
                    'high_school': Decimal('5.76'),
                    'university': Decimal('1.39')
                }
            },
            'MR05': {  # Brakna
                'total_population': 391309.71,
                'male_percentage': Decimal('46.30'),
                'female_percentage': Decimal('53.70'),
                'urban_percentage': Decimal('50.0'),
                'rural_percentage': Decimal('50.0'),
                'population_10_plus': 267456.00,
                'single_rate': Decimal('49.26'),
                'married_rate': Decimal('42.82'),
                'divorced_rate': Decimal('3.41'),
                'widowed_rate': Decimal('4.51'),
                'school_enrollment_rate': Decimal('97.35'),
                'illiteracy_rate_10_plus': Decimal('38.15'),
                'population_15_plus': 215128.87,
                'illiteracy_rate_15_plus': Decimal('39.48'),
                'education_levels': {
                    'no_education': Decimal('14.56'),
                    'preschool': Decimal('3.24'),
                    'primary': Decimal('67.24'),
                    'middle_school': Decimal('18.85'),
                    'high_school': Decimal('7.76'),
                    'university': Decimal('1.82')
                }
            },
            'MR06': {  # Trarza
                'total_population': 323903.18,
                'male_percentage': Decimal('46.91'),
                'female_percentage': Decimal('53.09'),
                'urban_percentage': Decimal('50.0'),
                'rural_percentage': Decimal('50.0'),
                'population_10_plus': 221456.00,
                'single_rate': Decimal('48.50'),
                'married_rate': Decimal('42.57'),
                'divorced_rate': Decimal('4.25'),
                'widowed_rate': Decimal('4.69'),
                'school_enrollment_rate': Decimal('97.89'),
                'illiteracy_rate_10_plus': Decimal('21.98'),
                'population_15_plus': 197699.93,
                'illiteracy_rate_15_plus': Decimal('22.67'),
                'education_levels': {
                    'no_education': Decimal('13.31'),
                    'preschool': Decimal('1.58'),
                    'primary': Decimal('61.72'),
                    'middle_school': Decimal('20.85'),
                    'high_school': Decimal('10.55'),
                    'university': Decimal('3.97')
                }
            },
            'MR07': {  # Adrar
                'total_population': 71622.84,
                'male_percentage': Decimal('48.46'),
                'female_percentage': Decimal('51.54'),
                'urban_percentage': Decimal('50.0'),
                'rural_percentage': Decimal('50.0'),
                'population_10_plus': 48956.00,
                'single_rate': Decimal('46.58'),
                'married_rate': Decimal('41.49'),
                'divorced_rate': Decimal('8.00'),
                'widowed_rate': Decimal('3.93'),
                'school_enrollment_rate': Decimal('98.20'),
                'illiteracy_rate_10_plus': Decimal('19.49'),
                'population_15_plus': 44080.70,
                'illiteracy_rate_15_plus': Decimal('20.31'),
                'education_levels': {
                    'no_education': Decimal('14.57'),
                    'preschool': Decimal('3.20'),
                    'primary': Decimal('58.02'),
                    'middle_school': Decimal('22.41'),
                    'high_school': Decimal('12.84'),
                    'university': Decimal('2.75')
                }
            },
            'MR08': {  # Dakhlet Nouadhibou
                'total_population': 184458.69,
                'male_percentage': Decimal('55.81'),
                'female_percentage': Decimal('44.19'),
                'urban_percentage': Decimal('50.0'),
                'rural_percentage': Decimal('50.0'),
                'population_10_plus': 126456.00,
                'single_rate': Decimal('49.83'),
                'married_rate': Decimal('42.83'),
                'divorced_rate': Decimal('5.25'),
                'widowed_rate': Decimal('2.09'),
                'school_enrollment_rate': Decimal('98.15'),
                'illiteracy_rate_10_plus': Decimal('16.69'),
                'population_15_plus': 123290.15,
                'illiteracy_rate_15_plus': Decimal('17.01'),
                'education_levels': {
                    'no_education': Decimal('14.82'),
                    'preschool': Decimal('4.34'),
                    'primary': Decimal('49.88'),
                    'middle_school': Decimal('22.53'),
                    'high_school': Decimal('16.61'),
                    'university': Decimal('5.19')
                }
            },
            'MR09': {  # Guidimaka
                'total_population': 267843.21,
                'male_percentage': Decimal('47.12'),
                'female_percentage': Decimal('52.88'),
                'urban_percentage': Decimal('50.0'),
                'rural_percentage': Decimal('50.0'),
                'population_10_plus': 183456.00,
                'single_rate': Decimal('47.85'),
                'married_rate': Decimal('43.15'),
                'divorced_rate': Decimal('4.32'),
                'widowed_rate': Decimal('4.68'),
                'school_enrollment_rate': Decimal('95.22'),
                'illiteracy_rate_10_plus': Decimal('35.67'),
                'population_15_plus': 203451.78,
                'illiteracy_rate_15_plus': Decimal('36.89'),
                'education_levels': {
                    'no_education': Decimal('17.45'),
                    'preschool': Decimal('2.13'),
                    'primary': Decimal('73.56'),
                    'middle_school': Decimal('15.67'),
                    'high_school': Decimal('6.89'),
                    'university': Decimal('2.31')
                }
            },
            'MR10': {  # Tiris Zemmour
                'total_population': 85432.15,
                'male_percentage': Decimal('51.23'),
                'female_percentage': Decimal('48.77'),
                'urban_percentage': Decimal('50.0'),
                'rural_percentage': Decimal('50.0'),
                'population_10_plus': 58456.00,
                'single_rate': Decimal('49.12'),
                'married_rate': Decimal('41.85'),
                'divorced_rate': Decimal('5.43'),
                'widowed_rate': Decimal('3.60'),
                'school_enrollment_rate': Decimal('97.85'),
                'illiteracy_rate_10_plus': Decimal('18.76'),
                'population_15_plus': 68421.53,
                'illiteracy_rate_15_plus': Decimal('19.45'),
                'education_levels': {
                    'no_education': Decimal('13.78'),
                    'preschool': Decimal('3.45'),
                    'primary': Decimal('60.23'),
                    'middle_school': Decimal('21.67'),
                    'high_school': Decimal('14.56'),
                    'university': Decimal('4.31')
                }
            },
            'MR11': {  # Inchiri
                'total_population': 19875.32,
                'male_percentage': Decimal('50.15'),
                'female_percentage': Decimal('49.85'),
                'urban_percentage': Decimal('50.0'),
                'rural_percentage': Decimal('50.0'),
                'population_10_plus': 13567.00,
                'single_rate': Decimal('48.37'),
                'married_rate': Decimal('42.56'),
                'divorced_rate': Decimal('5.24'),
                'widowed_rate': Decimal('3.83'),
                'school_enrollment_rate': Decimal('98.01'),
                'illiteracy_rate_10_plus': Decimal('17.89'),
                'population_15_plus': 15678.41,
                'illiteracy_rate_15_plus': Decimal('18.23'),
                'education_levels': {
                    'no_education': Decimal('12.56'),
                    'preschool': Decimal('3.78'),
                    'primary': Decimal('62.45'),
                    'middle_school': Decimal('20.12'),
                    'high_school': Decimal('13.45'),
                    'university': Decimal('4.67')
                }
            },
            'MR12': {  # Nouakchott-Nord
                'total_population': 366789.21,
                'male_percentage': Decimal('49.87'),
                'female_percentage': Decimal('50.13'),
                'urban_percentage': Decimal('50.0'),
                'rural_percentage': Decimal('50.0'),
                'population_10_plus': 250456.00,
                'single_rate': Decimal('52.34'),
                'married_rate': Decimal('40.12'),
                'divorced_rate': Decimal('4.56'),
                'widowed_rate': Decimal('2.98'),
                'school_enrollment_rate': Decimal('98.45'),
                'illiteracy_rate_10_plus': Decimal('15.67'),
                'population_15_plus': 298765.32,
                'illiteracy_rate_15_plus': Decimal('16.23'),
                'education_levels': {
                    'no_education': Decimal('10.23'),
                    'preschool': Decimal('4.56'),
                    'primary': Decimal('55.67'),
                    'middle_school': Decimal('25.34'),
                    'high_school': Decimal('17.89'),
                    'university': Decimal('6.45')
                }
            },
            'MR13': {  # Nouakchott-Ouest
                'total_population': 287654.32,
                'male_percentage': Decimal('49.45'),
                'female_percentage': Decimal('50.55'),
                'urban_percentage': Decimal('50.0'),
                'rural_percentage': Decimal('50.0'),
                'population_10_plus': 196456.00,
                'single_rate': Decimal('53.21'),
                'married_rate': Decimal('39.45'),
                'divorced_rate': Decimal('4.78'),
                'widowed_rate': Decimal('2.56'),
                'school_enrollment_rate': Decimal('98.67'),
                'illiteracy_rate_10_plus': Decimal('14.89'),
                'population_15_plus': 234567.89,
                'illiteracy_rate_15_plus': Decimal('15.34'),
                'education_levels': {
                    'no_education': Decimal('9.87'),
                    'preschool': Decimal('4.78'),
                    'primary': Decimal('54.23'),
                    'middle_school': Decimal('26.45'),
                    'high_school': Decimal('18.67'),
                    'university': Decimal('7.12')
                }
            },
            'MR14': {  # Nouakchott-Sud
                'total_population': 312456.78,
                'male_percentage': Decimal('49.78'),
                'female_percentage': Decimal('50.22'),
                'urban_percentage': Decimal('50.0'),
                'rural_percentage': Decimal('50.0'),
                'population_10_plus': 213456.00,
                'single_rate': Decimal('52.89'),
                'married_rate': Decimal('40.23'),
                'divorced_rate': Decimal('4.12'),
                'widowed_rate': Decimal('2.76'),
                'school_enrollment_rate': Decimal('98.56'),
                'illiteracy_rate_10_plus': Decimal('15.12'),
                'population_15_plus': 256789.45,
                'illiteracy_rate_15_plus': Decimal('15.78'),
                'education_levels': {
                    'no_education': Decimal('10.12'),
                    'preschool': Decimal('4.34'),
                    'primary': Decimal('55.12'),
                    'middle_school': Decimal('25.78'),
                    'high_school': Decimal('17.56'),
                    'university': Decimal('6.89')
                }
            },
            'MR15': {  # Tagant
                'total_population': 98765.43,
                'male_percentage': Decimal('47.89'),
                'female_percentage': Decimal('52.11'),
                'urban_percentage': Decimal('50.0'),
                'rural_percentage': Decimal('50.0'),
                'population_10_plus': 67456.00,
                'single_rate': Decimal('46.78'),
                'married_rate': Decimal('43.56'),
                'divorced_rate': Decimal('5.34'),
                'widowed_rate': Decimal('4.32'),
                'school_enrollment_rate': Decimal('96.78'),
                'illiteracy_rate_10_plus': Decimal('28.45'),
                'population_15_plus': 75678.91,
                'illiteracy_rate_15_plus': Decimal('29.12'),
                'education_levels': {
                    'no_education': Decimal('16.78'),
                    'preschool': Decimal('2.45'),
                    'primary': Decimal('68.90'),
                    'middle_school': Decimal('17.56'),
                    'high_school': Decimal('8.90'),
                    'university': Decimal('3.45')
                }
            }
        }
        return region_data.get(region_code)

    def get_department_data(self, dept_code):
        # Dictionnaire des données démographiques par département
        dept_data = {
            'MR011': {  # Amourj
                'total_population': 78148,
                'male_percentage': Decimal('45.1'),
                'female_percentage': Decimal('54.9'),
                'urban_percentage': Decimal('50.0'),
                'rural_percentage': Decimal('50.0'),
                'population_10_plus': 51781,
                'single_rate': Decimal('42.6'),
                'married_rate': Decimal('48.4'),
                'divorced_rate': Decimal('4.6'),
                'widowed_rate': Decimal('4.3'),
                'school_enrollment_rate': Decimal('94.0'),
                'illiteracy_rate_10_plus': Decimal('50.0'),
                'population_15_plus': 41007,
                'illiteracy_rate_15_plus': Decimal('51.0'),
                'education_levels': {
                    'no_education': Decimal('19.1'),
                    'preschool': Decimal('2.1'),
                    'primary': Decimal('86.4'),
                    'middle_school': Decimal('7.1'),
                    'high_school': Decimal('2.7'),
                    'university': Decimal('1.0')
                }
            },
            'MR021': {  # Aioun
                'total_population': 78229,
                'male_percentage': Decimal('46.5'),
                'female_percentage': Decimal('53.5'),
                'urban_percentage': Decimal('50.0'),
                'rural_percentage': Decimal('50.0'),
                'population_10_plus': 57652,
                'single_rate': Decimal('48.3'),
                'married_rate': Decimal('42.7'),
                'divorced_rate': Decimal('5.2'),
                'widowed_rate': Decimal('3.9'),
                'school_enrollment_rate': Decimal('95.8'),
                'illiteracy_rate_10_plus': Decimal('29.1'),
                'population_15_plus': 47399,
                'illiteracy_rate_15_plus': Decimal('29.9'),
                'education_levels': {
                    'no_education': Decimal('12.7'),
                    'preschool': Decimal('1.6'),
                    'primary': Decimal('60.4'),
                    'middle_school': Decimal('20.8'),
                    'high_school': Decimal('11.0'),
                    'university': Decimal('5.4')
                }
            },
            'MR022': {  # Koubenni
                'total_population': 135157,
                'male_percentage': Decimal('46.8'),
                'female_percentage': Decimal('53.2'),
                'urban_percentage': Decimal('50.0'),
                'rural_percentage': Decimal('50.0'),
                'population_10_plus': 88801,
                'single_rate': Decimal('45.4'),
                'married_rate': Decimal('47.6'),
                'divorced_rate': Decimal('3.4'),
                'widowed_rate': Decimal('3.5'),
                'school_enrollment_rate': Decimal('92.8'),
                'illiteracy_rate_10_plus': Decimal('44.0'),
                'population_15_plus': 69366,
                'illiteracy_rate_15_plus': Decimal('45.8'),
                'education_levels': {
                    'no_education': Decimal('20.1'),
                    'preschool': Decimal('2.0'),
                    'primary': Decimal('83.4'),
                    'middle_school': Decimal('9.4'),
                    'high_school': Decimal('3.2'),
                    'university': Decimal('1.0')
                }
            },
            'MR031': {  # Barkéol
                'total_population': 85137,
                'male_percentage': Decimal('46.8'),
                'female_percentage': Decimal('53.2'),
                'urban_percentage': Decimal('50.0'),
                'rural_percentage': Decimal('50.0'),
                'population_10_plus': 55674,
                'single_rate': Decimal('44.9'),
                'married_rate': Decimal('48.4'),
                'divorced_rate': Decimal('4.1'),
                'widowed_rate': Decimal('2.6'),
                'school_enrollment_rate': Decimal('94.2'),
                'illiteracy_rate_10_plus': Decimal('31.8'),
                'population_15_plus': 55674,
                'illiteracy_rate_15_plus': Decimal('33.1'),
                'education_levels': {
                    'no_education': Decimal('15.8'),
                    'preschool': Decimal('1.0'),
                    'primary': Decimal('68.1'),
                    'middle_school': Decimal('17.2'),
                    'high_school': Decimal('5.9'),
                    'university': Decimal('1.7')
                }
            },
            'MR032': {  # Boumdeid
                'total_population': 42568,
                'male_percentage': Decimal('47.3'),
                'female_percentage': Decimal('52.7'),
                'urban_percentage': Decimal('50.0'),
                'rural_percentage': Decimal('50.0'),
                'population_10_plus': 27845,
                'single_rate': Decimal('45.1'),
                'married_rate': Decimal('47.9'),
                'divorced_rate': Decimal('3.8'),
                'widowed_rate': Decimal('3.2'),
                'school_enrollment_rate': Decimal('93.9'),
                'illiteracy_rate_10_plus': Decimal('32.1'),
                'population_15_plus': 27845,
                'illiteracy_rate_15_plus': Decimal('33.4'),
                'education_levels': {
                    'no_education': Decimal('16.1'),
                    'preschool': Decimal('0.9'),
                    'primary': Decimal('67.8'),
                    'middle_school': Decimal('16.9'),
                    'high_school': Decimal('5.7'),
                    'university': Decimal('1.5')
                }
            },
            'MR041': {  # Kaédi
                'total_population': 118963,
                'male_percentage': Decimal('48.5'),
                'female_percentage': Decimal('51.5'),
                'urban_percentage': Decimal('50.0'),
                'rural_percentage': Decimal('50.0'),
                'population_10_plus': 77896,
                'single_rate': Decimal('44.8'),
                'married_rate': Decimal('48.3'),
                'divorced_rate': Decimal('4.1'),
                'widowed_rate': Decimal('2.8'),
                'school_enrollment_rate': Decimal('95.6'),
                'illiteracy_rate_10_plus': Decimal('30.2'),
                'population_15_plus': 77896,
                'illiteracy_rate_15_plus': Decimal('31.5'),
                'education_levels': {
                    'no_education': Decimal('14.5'),
                    'preschool': Decimal('1.3'),
                    'primary': Decimal('69.1'),
                    'middle_school': Decimal('18.4'),
                    'high_school': Decimal('6.8'),
                    'university': Decimal('2.4')
                }
            },
            'MR042': {  # M'Bout
                'total_population': 92567,
                'male_percentage': Decimal('47.9'),
                'female_percentage': Decimal('52.1'),
                'population_10_plus': 60671,
                'single_rate': Decimal('44.6'),
                'married_rate': Decimal('48.7'),
                'divorced_rate': Decimal('3.9'),
                'widowed_rate': Decimal('2.8'),
                'school_enrollment_rate': Decimal('94.6'),
                'illiteracy_rate_10_plus': Decimal('31.4'),
                'population_15_plus': 60671,
                'illiteracy_rate_15_plus': Decimal('32.7'),
                'education_levels': {
                    'no_education': Decimal('15.3'),
                    'preschool': Decimal('1.1'),
                    'primary': Decimal('68.3'),
                    'middle_school': Decimal('17.8'),
                    'high_school': Decimal('6.0'),
                    'university': Decimal('1.8')
                }
            },
            'MR051': {  # Aleg
                'total_population': 98567,
                'male_percentage': Decimal('48.1'),
                'female_percentage': Decimal('51.9'),
                'population_10_plus': 64521,
                'single_rate': Decimal('44.0'),
                'married_rate': Decimal('49.1'),
                'divorced_rate': Decimal('4.2'),
                'widowed_rate': Decimal('2.7'),
                'school_enrollment_rate': Decimal('95.2'),
                'illiteracy_rate_10_plus': Decimal('30.9'),
                'population_15_plus': 64521,
                'illiteracy_rate_15_plus': Decimal('32.2'),
                'education_levels': {
                    'no_education': Decimal('14.8'),
                    'preschool': Decimal('1.2'),
                    'primary': Decimal('68.7'),
                    'middle_school': Decimal('18.2'),
                    'high_school': Decimal('6.5'),
                    'university': Decimal('2.2')
                }
            },
            'MR052': {  # Bababé
                'total_population': 78456,
                'male_percentage': Decimal('47.5'),
                'female_percentage': Decimal('52.5'),
                'urban_percentage': Decimal('50.0'),
                'rural_percentage': Decimal('50.0'),
                'population_10_plus': 51345,
                'single_rate': Decimal('44.4'),
                'married_rate': Decimal('48.7'),
                'divorced_rate': Decimal('4.0'),
                'widowed_rate': Decimal('2.9'),
                'school_enrollment_rate': Decimal('94.8'),
                'illiteracy_rate_10_plus': Decimal('31.2'),
                'population_15_plus': 51345,
                'illiteracy_rate_15_plus': Decimal('32.5'),
                'education_levels': {
                    'no_education': Decimal('15.0'),
                    'preschool': Decimal('1.1'),
                    'primary': Decimal('68.5'),
                    'middle_school': Decimal('18.0'),
                    'high_school': Decimal('6.2'),
                    'university': Decimal('2.0')
                }
            },
            'MR061': {  # Rosso
                'total_population': 125678,
                'male_percentage': Decimal('48.8'),
                'female_percentage': Decimal('51.2'),
                'population_10_plus': 82235,
                'single_rate': Decimal('43.5'),
                'married_rate': Decimal('49.5'),
                'divorced_rate': Decimal('4.4'),
                'widowed_rate': Decimal('2.6'),
                'school_enrollment_rate': Decimal('95.9'),
                'illiteracy_rate_10_plus': Decimal('30.1'),
                'population_15_plus': 82235,
                'illiteracy_rate_15_plus': Decimal('31.4'),
                'education_levels': {
                    'no_education': Decimal('14.1'),
                    'preschool': Decimal('1.5'),
                    'primary': Decimal('69.3'),
                    'middle_school': Decimal('18.9'),
                    'high_school': Decimal('7.2'),
                    'university': Decimal('2.9')
                }
            },
            'MR062': {  # Boutilimit
                'total_population': 98765,
                'male_percentage': Decimal('48.2'),
                'female_percentage': Decimal('51.8'),
                'population_10_plus': 64634,
                'single_rate': Decimal('44.1'),
                'married_rate': Decimal('48.9'),
                'divorced_rate': Decimal('4.2'),
                'widowed_rate': Decimal('2.8'),
                'school_enrollment_rate': Decimal('95.3'),
                'illiteracy_rate_10_plus': Decimal('30.7'),
                'population_15_plus': 64634,
                'illiteracy_rate_15_plus': Decimal('32.0'),
                'education_levels': {
                    'no_education': Decimal('14.7'),
                    'preschool': Decimal('1.3'),
                    'primary': Decimal('68.7'),
                    'middle_school': Decimal('18.3'),
                    'high_school': Decimal('6.6'),
                    'university': Decimal('2.3')
                }
            },
            'Maghama': {
                'total_population': 82456,
                'male_percentage': Decimal('48.2'),
                'female_percentage': Decimal('51.8'),
                'population_10_plus': 54023,
                'single_rate': Decimal('44.7'),
                'married_rate': Decimal('48.5'),
                'divorced_rate': Decimal('4.0'),
                'widowed_rate': Decimal('2.8'),
                'school_enrollment_rate': Decimal('95.1'),
                'illiteracy_rate_10_plus': Decimal('30.8'),
                'population_15_plus': 54023,
                'illiteracy_rate_15_plus': Decimal('32.1'),
                'education_levels': {
                    'no_education': Decimal('14.9'),
                    'preschool': Decimal('1.2'),
                    'primary': Decimal('68.7'),
                    'middle_school': Decimal('18.1'),
                    'high_school': Decimal('6.4'),
                    'university': Decimal('2.1')
                }
            },
            'Monguel': {
                'total_population': 73906,
                'male_percentage': Decimal('48.2'),
                'female_percentage': Decimal('51.8'),
                'population_10_plus': 48397,
                'single_rate': Decimal('44.7'),
                'married_rate': Decimal('48.5'),
                'divorced_rate': Decimal('4.0'),
                'widowed_rate': Decimal('2.8'),
                'school_enrollment_rate': Decimal('95.1'),
                'illiteracy_rate_10_plus': Decimal('30.8'),
                'population_15_plus': 48397,
                'illiteracy_rate_15_plus': Decimal('32.1'),
                'education_levels': {
                    'no_education': Decimal('14.9'),
                    'preschool': Decimal('1.2'),
                    'primary': Decimal('68.7'),
                    'middle_school': Decimal('18.1'),
                    'high_school': Decimal('6.4'),
                    'university': Decimal('2.1')
                }
            },
            'MR071': {  # Nouadhibou
                'total_population': 162627,
                'male_percentage': Decimal('48.2'),
                'female_percentage': Decimal('51.8'),
                'urban_percentage': Decimal('87.5'),
                'rural_percentage': Decimal('12.5'),
                'population_10_plus': 106481,
                'single_rate': Decimal('44.5'),
                'married_rate': Decimal('48.6'),
                'divorced_rate': Decimal('4.1'),
                'widowed_rate': Decimal('2.8'),
                'school_enrollment_rate': Decimal('95.4'),
                'illiteracy_rate_10_plus': Decimal('30.5'),
                'population_15_plus': 106481,
                'illiteracy_rate_15_plus': Decimal('31.8'),
                'education_levels': {
                    'no_education': Decimal('14.7'),
                    'preschool': Decimal('1.2'),
                    'primary': Decimal('68.9'),
                    'middle_school': Decimal('18.3'),
                    'high_school': Decimal('6.6'),
                    'university': Decimal('2.3')
                }
            },
            'MR072': {  # Chami
                'total_population': 28423,
                'male_percentage': Decimal('47.8'),
                'female_percentage': Decimal('52.2'),
                'urban_percentage': Decimal('82.5'),
                'rural_percentage': Decimal('17.5'),
                'population_10_plus': 18617,
                'single_rate': Decimal('44.3'),
                'married_rate': Decimal('48.8'),
                'divorced_rate': Decimal('4.0'),
                'widowed_rate': Decimal('2.9'),
                'school_enrollment_rate': Decimal('94.7'),
                'illiteracy_rate_10_plus': Decimal('31.0'),
                'population_15_plus': 18617,
                'illiteracy_rate_15_plus': Decimal('32.3'),
                'education_levels': {
                    'no_education': Decimal('14.9'),
                    'preschool': Decimal('1.1'),
                    'primary': Decimal('68.6'),
                    'middle_school': Decimal('18.1'),
                    'high_school': Decimal('6.3'),
                    'university': Decimal('2.1')
                }
            },
            'MR073': {  # Nouamghar
                'total_population': 85635,
                'male_percentage': Decimal('48.0'),
                'female_percentage': Decimal('52.0'),
                'urban_percentage': Decimal('32.5'),
                'rural_percentage': Decimal('67.5'),
                'population_10_plus': 56091,
                'single_rate': Decimal('44.2'),
                'married_rate': Decimal('48.9'),
                'divorced_rate': Decimal('3.9'),
                'widowed_rate': Decimal('3.0'),
                'school_enrollment_rate': Decimal('94.5'),
                'illiteracy_rate_10_plus': Decimal('31.4'),
                'population_15_plus': 56091,
                'illiteracy_rate_15_plus': Decimal('32.7'),
                'education_levels': {
                    'no_education': Decimal('15.2'),
                    'preschool': Decimal('1.0'),
                    'primary': Decimal('68.3'),
                    'middle_school': Decimal('17.8'),
                    'high_school': Decimal('6.0'),
                    'university': Decimal('1.8')
                }
            },
            'MR074': {  # Boulenouar
                'total_population': 62829,
                'male_percentage': Decimal('47.6'),
                'female_percentage': Decimal('52.4'),
                'urban_percentage': Decimal('85.4'),
                'rural_percentage': Decimal('14.6'),
                'population_10_plus': 41153,
                'single_rate': Decimal('44.1'),
                'married_rate': Decimal('49.0'),
                'divorced_rate': Decimal('3.8'),
                'widowed_rate': Decimal('3.1'),
                'school_enrollment_rate': Decimal('94.3'),
                'illiteracy_rate_10_plus': Decimal('31.6'),
                'population_15_plus': 41153,
                'illiteracy_rate_15_plus': Decimal('32.9'),
                'education_levels': {
                    'no_education': Decimal('15.4'),
                    'preschool': Decimal('0.9'),
                    'primary': Decimal('68.0'),
                    'middle_school': Decimal('17.5'),
                    'high_school': Decimal('5.8'),
                    'university': Decimal('1.6')
                }
            },
            'MR121': {  # Nouakchott Ouest
                'total_population': 465152,
                'male_percentage': Decimal('48.3'),
                'female_percentage': Decimal('51.7'),
                'urban_percentage': Decimal('100.0'),
                'rural_percentage': Decimal('0.0'),
                'population_10_plus': 304635,
                'single_rate': Decimal('44.0'),
                'married_rate': Decimal('49.1'),
                'divorced_rate': Decimal('3.7'),
                'widowed_rate': Decimal('3.2'),
                'school_enrollment_rate': Decimal('95.1'),
                'illiteracy_rate_10_plus': Decimal('30.8'),
                'population_15_plus': 304635,
                'illiteracy_rate_15_plus': Decimal('32.1'),
                'education_levels': {
                    'no_education': Decimal('14.9'),
                    'preschool': Decimal('1.2'),
                    'primary': Decimal('68.7'),
                    'middle_school': Decimal('18.1'),
                    'high_school': Decimal('6.4'),
                    'university': Decimal('2.1')
                }
            },
            'MR122': {  # Nouakchott Nord
                'total_population': 425142,
                'male_percentage': Decimal('48.1'),
                'female_percentage': Decimal('51.9'),
                'urban_percentage': Decimal('100.0'),
                'rural_percentage': Decimal('0.0'),
                'population_10_plus': 278469,
                'single_rate': Decimal('43.9'),
                'married_rate': Decimal('49.2'),
                'divorced_rate': Decimal('3.6'),
                'widowed_rate': Decimal('3.3'),
                'school_enrollment_rate': Decimal('94.9'),
                'illiteracy_rate_10_plus': Decimal('31.0'),
                'population_15_plus': 278469,
                'illiteracy_rate_15_plus': Decimal('32.3'),
                'education_levels': {
                    'no_education': Decimal('15.0'),
                    'preschool': Decimal('1.1'),
                    'primary': Decimal('68.5'),
                    'middle_school': Decimal('17.9'),
                    'high_school': Decimal('6.2'),
                    'university': Decimal('2.0')
                }
            },
            'MR141': {  # Nouakchott Sud
                'total_population': 458467,
                'male_percentage': Decimal('48.4'),
                'female_percentage': Decimal('51.6'),
                'urban_percentage': Decimal('100.0'),
                'rural_percentage': Decimal('0.0'),
                'population_10_plus': 300296,
                'single_rate': Decimal('43.8'),
                'married_rate': Decimal('49.3'),
                'divorced_rate': Decimal('3.5'),
                'widowed_rate': Decimal('3.4'),
                'school_enrollment_rate': Decimal('94.7'),
                'illiteracy_rate_10_plus': Decimal('31.2'),
                'population_15_plus': 300296,
                'illiteracy_rate_15_plus': Decimal('32.5'),
                'education_levels': {
                    'no_education': Decimal('15.1'),
                    'preschool': Decimal('1.0'),
                    'primary': Decimal('68.3'),
                    'middle_school': Decimal('17.7'),
                    'high_school': Decimal('6.0'),
                    'university': Decimal('1.9')
                }
            },
            'MR142': {  # Nouakchott Centre
                'total_population': 397589,
                'male_percentage': Decimal('48.2'),
                'female_percentage': Decimal('51.8'),
                'urban_percentage': Decimal('100.0'),
                'rural_percentage': Decimal('0.0'),
                'population_10_plus': 260421,
                'single_rate': Decimal('43.7'),
                'married_rate': Decimal('49.4'),
                'divorced_rate': Decimal('3.4'),
                'widowed_rate': Decimal('3.5'),
                'school_enrollment_rate': Decimal('94.5'),
                'illiteracy_rate_10_plus': Decimal('31.4'),
                'population_15_plus': 260421,
                'illiteracy_rate_15_plus': Decimal('32.7'),
                'education_levels': {
                    'no_education': Decimal('15.2'),
                    'preschool': Decimal('0.9'),
                    'primary': Decimal('68.1'),
                    'middle_school': Decimal('17.5'),
                    'high_school': Decimal('5.8'),
                    'university': Decimal('1.8')
                }
            },
            'MR143': {  # Nouakchott Est
                'total_population': 374572,
                'male_percentage': Decimal('48.0'),
                'female_percentage': Decimal('52.0'),
                'urban_percentage': Decimal('100.0'),
                'rural_percentage': Decimal('0.0'),
                'population_10_plus': 245365,
                'single_rate': Decimal('43.6'),
                'married_rate': Decimal('49.5'),
                'divorced_rate': Decimal('3.3'),
                'widowed_rate': Decimal('3.6'),
                'school_enrollment_rate': Decimal('94.3'),
                'illiteracy_rate_10_plus': Decimal('31.6'),
                'population_15_plus': 245365,
                'illiteracy_rate_15_plus': Decimal('32.9'),
                'education_levels': {
                    'no_education': Decimal('15.3'),
                    'preschool': Decimal('0.8'),
                    'primary': Decimal('67.9'),
                    'middle_school': Decimal('17.3'),
                    'high_school': Decimal('5.6'),
                    'university': Decimal('1.7')
                }
            },
            'MR132': {  # Tiris Zemmour
                'total_population': 302196,
                'male_percentage': Decimal('47.8'),
                'female_percentage': Decimal('52.2'),
                'urban_percentage': Decimal('25.2'),
                'rural_percentage': Decimal('74.8'),
                'population_10_plus': 197939,
                'single_rate': Decimal('43.5'),
                'married_rate': Decimal('49.6'),
                'divorced_rate': Decimal('3.2'),
                'widowed_rate': Decimal('3.7'),
                'school_enrollment_rate': Decimal('94.1'),
                'illiteracy_rate_10_plus': Decimal('31.8'),
                'population_15_plus': 197939,
                'illiteracy_rate_15_plus': Decimal('33.1'),
                'education_levels': {
                    'no_education': Decimal('15.4'),
                    'preschool': Decimal('0.7'),
                    'primary': Decimal('67.7'),
                    'middle_school': Decimal('17.1'),
                    'high_school': Decimal('5.4'),
                    'university': Decimal('1.6')
                }
            },
            'MR133': {  # Inchiri
                'total_population': 325991,
                'male_percentage': Decimal('47.6'),
                'female_percentage': Decimal('52.4'),
                'urban_percentage': Decimal('24.8'),
                'rural_percentage': Decimal('75.2'),
                'population_10_plus': 213525,
                'single_rate': Decimal('43.4'),
                'married_rate': Decimal('49.7'),
                'divorced_rate': Decimal('3.1'),
                'widowed_rate': Decimal('3.8'),
                'school_enrollment_rate': Decimal('93.9'),
                'illiteracy_rate_10_plus': Decimal('32.0'),
                'population_15_plus': 213525,
                'illiteracy_rate_15_plus': Decimal('33.3'),
                'education_levels': {
                    'no_education': Decimal('15.5'),
                    'preschool': Decimal('0.6'),
                    'primary': Decimal('67.5'),
                    'middle_school': Decimal('16.9'),
                    'high_school': Decimal('5.2'),
                    'university': Decimal('1.5')
                }
            },
            'MR131': {  # Adrar
                'total_population': 512957,
                'male_percentage': Decimal('47.4'),
                'female_percentage': Decimal('52.6'),
                'urban_percentage': Decimal('22.5'),
                'rural_percentage': Decimal('77.5'),
                'population_10_plus': 335996,
                'single_rate': Decimal('43.3'),
                'married_rate': Decimal('49.8'),
                'divorced_rate': Decimal('3.0'),
                'widowed_rate': Decimal('3.9'),
                'school_enrollment_rate': Decimal('93.7'),
                'illiteracy_rate_10_plus': Decimal('32.2'),
                'population_15_plus': 335996,
                'illiteracy_rate_15_plus': Decimal('33.5'),
                'education_levels': {
                    'no_education': Decimal('15.6'),
                    'preschool': Decimal('0.5'),
                    'primary': Decimal('67.3'),
                    'middle_school': Decimal('16.7'),
                    'high_school': Decimal('5.0'),
                    'university': Decimal('1.4')
                }
            },
            'MR152': {  # Guidimakha
                'total_population': 403384,
                'male_percentage': Decimal('47.2'),
                'female_percentage': Decimal('52.8'),
                'urban_percentage': Decimal('27.2'),
                'rural_percentage': Decimal('72.8'),
                'population_10_plus': 264217,
                'single_rate': Decimal('43.2'),
                'married_rate': Decimal('49.9'),
                'divorced_rate': Decimal('2.9'),
                'widowed_rate': Decimal('4.0'),
                'school_enrollment_rate': Decimal('93.5'),
                'illiteracy_rate_10_plus': Decimal('32.4'),
                'population_15_plus': 264217,
                'illiteracy_rate_15_plus': Decimal('33.7'),
                'education_levels': {
                    'no_education': Decimal('15.7'),
                    'preschool': Decimal('0.4'),
                    'primary': Decimal('67.1'),
                    'middle_school': Decimal('16.5'),
                    'high_school': Decimal('4.8'),
                    'university': Decimal('1.3')
                }
            },
            'MR151': {  # Gorgol
                'total_population': 367892,
                'male_percentage': Decimal('47.0'),
                'female_percentage': Decimal('53.0'),
                'urban_percentage': Decimal('28.4'),
                'rural_percentage': Decimal('71.6'),
                'population_10_plus': 240970,
                'single_rate': Decimal('43.1'),
                'married_rate': Decimal('50.0'),
                'divorced_rate': Decimal('2.8'),
                'widowed_rate': Decimal('4.1'),
                'school_enrollment_rate': Decimal('93.3'),
                'illiteracy_rate_10_plus': Decimal('32.6'),
                'population_15_plus': 240970,
                'illiteracy_rate_15_plus': Decimal('33.9'),
                'education_levels': {
                    'no_education': Decimal('15.8'),
                    'preschool': Decimal('0.3'),
                    'primary': Decimal('66.9'),
                    'middle_school': Decimal('16.3'),
                    'high_school': Decimal('4.6'),
                    'university': Decimal('1.2')
                }
            },
            'MR153': {  # Brakna
                'total_population': 442486,
                'male_percentage': Decimal('46.8'),
                'female_percentage': Decimal('53.2'),
                'urban_percentage': Decimal('29.5'),
                'rural_percentage': Decimal('70.5'),
                'population_10_plus': 289828,
                'single_rate': Decimal('43.0'),
                'married_rate': Decimal('50.1'),
                'divorced_rate': Decimal('2.7'),
                'widowed_rate': Decimal('4.2'),
                'school_enrollment_rate': Decimal('93.1'),
                'illiteracy_rate_10_plus': Decimal('32.8'),
                'population_15_plus': 289828,
                'illiteracy_rate_15_plus': Decimal('34.1'),
                'education_levels': {
                    'no_education': Decimal('15.9'),
                    'preschool': Decimal('0.2'),
                    'primary': Decimal('66.7'),
                    'middle_school': Decimal('16.1'),
                    'high_school': Decimal('4.4'),
                    'university': Decimal('1.1')
                }
            },
            'MR091': {  # Tagant
                'total_population': 95925,
                'male_percentage': Decimal('46.6'),
                'female_percentage': Decimal('53.4'),
                'urban_percentage': Decimal('29.5'),
                'rural_percentage': Decimal('70.5'),
                'population_10_plus': 62831,
                'single_rate': Decimal('42.9'),
                'married_rate': Decimal('50.2'),
                'divorced_rate': Decimal('2.6'),
                'widowed_rate': Decimal('4.3'),
                'school_enrollment_rate': Decimal('92.9'),
                'illiteracy_rate_10_plus': Decimal('33.0'),
                'population_15_plus': 62831,
                'illiteracy_rate_15_plus': Decimal('34.3'),
                'education_levels': {
                    'no_education': Decimal('16.0'),
                    'preschool': Decimal('0.1'),
                    'primary': Decimal('66.5'),
                    'middle_school': Decimal('15.9'),
                    'high_school': Decimal('4.2'),
                    'university': Decimal('1.0')
                }
            },
            'MR092': {  # Assaba
                'total_population': 403384,
                'male_percentage': Decimal('46.4'),
                'female_percentage': Decimal('53.6'),
                'urban_percentage': Decimal('30.0'),
                'rural_percentage': Decimal('70.0'),
                'population_10_plus': 264217,
                'single_rate': Decimal('42.8'),
                'married_rate': Decimal('50.3'),
                'divorced_rate': Decimal('2.5'),
                'widowed_rate': Decimal('4.4'),
                'school_enrollment_rate': Decimal('92.7'),
                'illiteracy_rate_10_plus': Decimal('33.2'),
                'population_15_plus': 264217,
                'illiteracy_rate_15_plus': Decimal('34.5'),
                'education_levels': {
                    'no_education': Decimal('16.1'),
                    'preschool': Decimal('0.0'),
                    'primary': Decimal('66.3'),
                    'middle_school': Decimal('15.7'),
                    'high_school': Decimal('4.0'),
                    'university': Decimal('0.9')
                }
            },
            'MR093': {  # Hodh El Gharbi
                'total_population': 325991,
                'male_percentage': Decimal('46.2'),
                'female_percentage': Decimal('53.8'),
                'urban_percentage': Decimal('30.5'),
                'rural_percentage': Decimal('69.5'),
                'population_10_plus': 213525,
                'single_rate': Decimal('42.7'),
                'married_rate': Decimal('50.4'),
                'divorced_rate': Decimal('2.4'),
                'widowed_rate': Decimal('4.5'),
                'school_enrollment_rate': Decimal('92.5'),
                'illiteracy_rate_10_plus': Decimal('33.4'),
                'population_15_plus': 213525,
                'illiteracy_rate_15_plus': Decimal('34.7'),
                'education_levels': {
                    'no_education': Decimal('16.2'),
                    'preschool': Decimal('0.0'),
                    'primary': Decimal('66.1'),
                    'middle_school': Decimal('15.5'),
                    'high_school': Decimal('3.8'),
                    'university': Decimal('0.8')
                }
            },
            'MR111': {  # Hodh Chargui
                'total_population': 512957,
                'male_percentage': Decimal('46.0'),
                'female_percentage': Decimal('54.0'),
                'urban_percentage': Decimal('31.0'),
                'rural_percentage': Decimal('69.0'),
                'population_10_plus': 335996,
                'single_rate': Decimal('42.6'),
                'married_rate': Decimal('50.5'),
                'divorced_rate': Decimal('2.3'),
                'widowed_rate': Decimal('4.6'),
                'school_enrollment_rate': Decimal('92.3'),
                'illiteracy_rate_10_plus': Decimal('33.6'),
                'population_15_plus': 335996,
                'illiteracy_rate_15_plus': Decimal('34.9'),
                'education_levels': {
                    'no_education': Decimal('16.3'),
                    'preschool': Decimal('0.0'),
                    'primary': Decimal('65.9'),
                    'middle_school': Decimal('15.3'),
                    'high_school': Decimal('3.6'),
                    'university': Decimal('0.7')
                }
            },
            'MR112': {  # Trarza
                'total_population': 397589,
                'male_percentage': Decimal('45.8'),
                'female_percentage': Decimal('54.2'),
                'urban_percentage': Decimal('31.5'),
                'rural_percentage': Decimal('68.5'),
                'population_10_plus': 260421,
                'single_rate': Decimal('42.5'),
                'married_rate': Decimal('50.6'),
                'divorced_rate': Decimal('2.2'),
                'widowed_rate': Decimal('4.7'),
                'school_enrollment_rate': Decimal('92.1'),
                'illiteracy_rate_10_plus': Decimal('33.8'),
                'population_15_plus': 260421,
                'illiteracy_rate_15_plus': Decimal('35.1'),
                'education_levels': {
                    'no_education': Decimal('16.4'),
                    'preschool': Decimal('0.0'),
                    'primary': Decimal('65.7'),
                    'middle_school': Decimal('15.1'),
                    'high_school': Decimal('3.4'),
                    'university': Decimal('0.6')
                }
            },
            'MR113': {  # Inchiri
                'total_population': 28423,
                'male_percentage': Decimal('45.6'),
                'female_percentage': Decimal('54.4'),
                'urban_percentage': Decimal('32.0'),
                'rural_percentage': Decimal('68.0'),
                'population_10_plus': 18617,
                'single_rate': Decimal('42.4'),
                'married_rate': Decimal('50.7'),
                'divorced_rate': Decimal('2.1'),
                'widowed_rate': Decimal('4.8'),
                'school_enrollment_rate': Decimal('91.9'),
                'illiteracy_rate_10_plus': Decimal('34.0'),
                'population_15_plus': 18617,
                'illiteracy_rate_15_plus': Decimal('35.3'),
                'education_levels': {
                    'no_education': Decimal('16.5'),
                    'preschool': Decimal('0.0'),
                    'primary': Decimal('65.5'),
                    'middle_school': Decimal('14.9'),
                    'high_school': Decimal('3.2'),
                    'university': Decimal('0.5')
                }
            },
            'MR063': {  # Tiris Zemmour
                'total_population': 62829,
                'male_percentage': Decimal('45.4'),
                'female_percentage': Decimal('54.6'),
                'urban_percentage': Decimal('32.5'),
                'rural_percentage': Decimal('67.5'),
                'population_10_plus': 41153,
                'single_rate': Decimal('42.3'),
                'married_rate': Decimal('50.8'),
                'divorced_rate': Decimal('2.0'),
                'widowed_rate': Decimal('4.9'),
                'school_enrollment_rate': Decimal('91.7'),
                'illiteracy_rate_10_plus': Decimal('34.2'),
                'population_15_plus': 41153,
                'illiteracy_rate_15_plus': Decimal('35.5'),
                'education_levels': {
                    'no_education': Decimal('16.6'),
                    'preschool': Decimal('0.0'),
                    'primary': Decimal('65.3'),
                    'middle_school': Decimal('14.7'),
                    'high_school': Decimal('3.0'),
                    'university': Decimal('0.4')
                }
            },
            'MR064': {  # Inchiri
                'total_population': 85635,
                'male_percentage': Decimal('45.2'),
                'female_percentage': Decimal('54.8'),
                'urban_percentage': Decimal('33.0'),
                'rural_percentage': Decimal('67.0'),
                'population_10_plus': 56091,
                'single_rate': Decimal('42.2'),
                'married_rate': Decimal('50.9'),
                'divorced_rate': Decimal('1.9'),
                'widowed_rate': Decimal('5.0'),
                'school_enrollment_rate': Decimal('91.5'),
                'illiteracy_rate_10_plus': Decimal('34.4'),
                'population_15_plus': 56091,
                'illiteracy_rate_15_plus': Decimal('35.7'),
                'education_levels': {
                    'no_education': Decimal('16.7'),
                    'preschool': Decimal('0.0'),
                    'primary': Decimal('65.1'),
                    'middle_school': Decimal('14.5'),
                    'high_school': Decimal('2.8'),
                    'university': Decimal('0.3')
                }
            },
            'MR065': {  # Adrar
                'total_population': 118963,
                'male_percentage': Decimal('45.0'),
                'female_percentage': Decimal('55.0'),
                'urban_percentage': Decimal('33.5'),
                'rural_percentage': Decimal('66.5'),
                'population_10_plus': 77896,
                'single_rate': Decimal('42.1'),
                'married_rate': Decimal('51.0'),
                'divorced_rate': Decimal('1.8'),
                'widowed_rate': Decimal('5.1'),
                'school_enrollment_rate': Decimal('91.3'),
                'illiteracy_rate_10_plus': Decimal('34.6'),
                'population_15_plus': 77896,
                'illiteracy_rate_15_plus': Decimal('35.9'),
                'education_levels': {
                    'no_education': Decimal('16.8'),
                    'preschool': Decimal('0.0'),
                    'primary': Decimal('64.9'),
                    'middle_school': Decimal('14.3'),
                    'high_school': Decimal('2.6'),
                    'university': Decimal('0.2')
                }
            },
            'MR066': {  # Tagant
                'total_population': 92567,
                'male_percentage': Decimal('44.8'),
                'female_percentage': Decimal('55.2'),
                'urban_percentage': Decimal('34.0'),
                'rural_percentage': Decimal('66.0'),
                'population_10_plus': 60671,
                'single_rate': Decimal('42.0'),
                'married_rate': Decimal('51.1'),
                'divorced_rate': Decimal('1.7'),
                'widowed_rate': Decimal('5.2'),
                'school_enrollment_rate': Decimal('91.1'),
                'illiteracy_rate_10_plus': Decimal('34.8'),
                'population_15_plus': 60671,
                'illiteracy_rate_15_plus': Decimal('36.1'),
                'education_levels': {
                    'no_education': Decimal('16.9'),
                    'preschool': Decimal('0.0'),
                    'primary': Decimal('64.7'),
                    'middle_school': Decimal('14.1'),
                    'high_school': Decimal('2.4'),
                    'university': Decimal('0.1')
                }
            },
            'MR067': {  # Assaba
                'total_population': 78456,
                'male_percentage': Decimal('44.6'),
                'female_percentage': Decimal('55.4'),
                'urban_percentage': Decimal('34.5'),
                'rural_percentage': Decimal('65.5'),
                'population_10_plus': 51345,
                'single_rate': Decimal('41.9'),
                'married_rate': Decimal('51.2'),
                'divorced_rate': Decimal('1.6'),
                'widowed_rate': Decimal('5.3'),
                'school_enrollment_rate': Decimal('90.9'),
                'illiteracy_rate_10_plus': Decimal('35.0'),
                'population_15_plus': 51345,
                'illiteracy_rate_15_plus': Decimal('36.3'),
                'education_levels': {
                    'no_education': Decimal('17.0'),
                    'preschool': Decimal('0.0'),
                    'primary': Decimal('64.5'),
                    'middle_school': Decimal('13.9'),
                    'high_school': Decimal('2.2'),
                    'university': Decimal('0.0')
                }
            }
        }
        return dept_data.get(dept_code)

    def get_commune_data(self, commune_name):
        """Retourne les données démographiques pour une commune donnée"""
        commune_data = {
            'Barkeol': {
                'total_population': 39563,
                'male_percentage': 46.5,
                'female_percentage': 53.5,
                'single_rate': 45.2,
                'married_rate': 47.8,
                'divorced_rate': 3.8,
                'widowed_rate': 3.2,
                'school_enrollment_rate': 94.5,
                'illiteracy_rate_10_plus': 32.5,
                'population_15_plus': 25874,
                'illiteracy_rate_15_plus': 33.8,
                'urban_percentage': 35.2,
                'rural_percentage': 64.8,
                'education_levels': {
                    'no_education': 15.2,
                    'preschool': 1.1,
                    'primary': 67.8,
                    'middle_school': 17.5,
                    'high_school': 6.2,
                    'university': 2.0
                }
            },
            'Amourj': {
                'total_population': 9604,
                'male_percentage': Decimal('45.5'),
                'female_percentage': Decimal('54.5'),
                'population_10_plus': 6824,
                'single_rate': Decimal('44.9'),
                'married_rate': Decimal('43.6'),
                'divorced_rate': Decimal('7.4'),
                'widowed_rate': Decimal('4.2'),
                'school_enrollment_rate': Decimal('95.3'),
                'illiteracy_rate_10_plus': Decimal('31.4'),
                'population_15_plus': 5505,
                'illiteracy_rate_15_plus': Decimal('31.5'),
                'education_levels': {
                    'no_education': Decimal('17.1'),
                    'preschool': Decimal('2.2'),
                    'primary': Decimal('66.8'),
                    'middle_school': Decimal('18.4'),
                    'high_school': Decimal('9.4'),
                    'university': Decimal('2.9')
                }
            },
            'Aioun': {
                'total_population': 36517,
                'male_percentage': Decimal('45.2'),
                'female_percentage': Decimal('54.8'),
                'population_10_plus': 27978,
                'single_rate': Decimal('52.1'),
                'married_rate': Decimal('38.9'),
                'divorced_rate': Decimal('5.7'),
                'widowed_rate': Decimal('3.3'),
                'school_enrollment_rate': Decimal('97.3'),
                'illiteracy_rate_10_plus': Decimal('19.6'),
                'population_15_plus': 23047,
                'illiteracy_rate_15_plus': Decimal('20.1'),
                'education_levels': {
                    'no_education': Decimal('8.4'),
                    'preschool': Decimal('1.2'),
                    'primary': Decimal('50.0'),
                    'middle_school': Decimal('25.5'),
                    'high_school': Decimal('15.3'),
                    'university': Decimal('7.4')
                }
            },
            'Koubenni': {
                'total_population': 19249,
                'male_percentage': Decimal('45.3'),
                'female_percentage': Decimal('54.7'),
                'population_10_plus': 13294,
                'single_rate': Decimal('50.7'),
                'married_rate': Decimal('41.1'),
                'divorced_rate': Decimal('5.0'),
                'widowed_rate': Decimal('3.2'),
                'school_enrollment_rate': Decimal('97.1'),
                'illiteracy_rate_10_plus': Decimal('29.9'),
                'population_15_plus': 10446,
                'illiteracy_rate_15_plus': Decimal('31.2'),
                'education_levels': {
                    'no_education': Decimal('13.6'),
                    'preschool': Decimal('1.2'),
                    'primary': Decimal('70.0'),
                    'middle_school': Decimal('18.9'),
                    'high_school': Decimal('6.9'),
                    'university': Decimal('2.1')
                }
            },
            'Boumdeid': {
                'total_population': 19845,
                'male_percentage': Decimal('47.0'),
                'female_percentage': Decimal('53.0'),
                'population_10_plus': 12987,
                'single_rate': Decimal('44.9'),
                'married_rate': Decimal('48.1'),
                'divorced_rate': Decimal('3.9'),
                'widowed_rate': Decimal('3.1'),
                'school_enrollment_rate': Decimal('94.1'),
                'illiteracy_rate_10_plus': Decimal('31.9'),
                'population_15_plus': 12987,
                'illiteracy_rate_15_plus': Decimal('33.2'),
                'education_levels': {
                    'no_education': Decimal('15.9'),
                    'preschool': Decimal('1.0'),
                    'primary': Decimal('68.0'),
                    'middle_school': Decimal('17.1'),
                    'high_school': Decimal('5.8'),
                    'university': Decimal('1.6')
                }
            },
            'Kaédi': {
                'total_population': 118963,
                'male_percentage': Decimal('48.5'),
                'female_percentage': Decimal('51.5'),
                'population_10_plus': 77896,
                'single_rate': Decimal('44.8'),
                'married_rate': Decimal('48.3'),
                'divorced_rate': Decimal('4.1'),
                'widowed_rate': Decimal('2.8'),
                'school_enrollment_rate': Decimal('95.6'),
                'illiteracy_rate_10_plus': Decimal('30.2'),
                'population_15_plus': 77896,
                'illiteracy_rate_15_plus': Decimal('31.5'),
                'education_levels': {
                    'no_education': Decimal('14.5'),
                    'preschool': Decimal('1.3'),
                    'primary': Decimal('69.1'),
                    'middle_school': Decimal('18.4'),
                    'high_school': Decimal('6.8'),
                    'university': Decimal('2.4')
                }
            },
            'M\'Bout': {
                'total_population': 92567,
                'male_percentage': Decimal('47.9'),
                'female_percentage': Decimal('52.1'),
                'population_10_plus': 60671,
                'single_rate': Decimal('44.6'),
                'married_rate': Decimal('48.7'),
                'divorced_rate': Decimal('3.9'),
                'widowed_rate': Decimal('2.8'),
                'school_enrollment_rate': Decimal('94.6'),
                'illiteracy_rate_10_plus': Decimal('31.4'),
                'population_15_plus': 60671,
                'illiteracy_rate_15_plus': Decimal('32.7'),
                'education_levels': {
                    'no_education': Decimal('15.3'),
                    'preschool': Decimal('1.1'),
                    'primary': Decimal('68.3'),
                    'middle_school': Decimal('17.8'),
                    'high_school': Decimal('6.0'),
                    'university': Decimal('1.8')
                }
            },
            'Aleg': {
                'total_population': 45892,
                'male_percentage': Decimal('48.3'),
                'female_percentage': Decimal('51.7'),
                'population_10_plus': 30045,
                'single_rate': Decimal('43.8'),
                'married_rate': Decimal('49.3'),
                'divorced_rate': Decimal('4.3'),
                'widowed_rate': Decimal('2.6'),
                'school_enrollment_rate': Decimal('95.5'),
                'illiteracy_rate_10_plus': Decimal('30.6'),
                'population_15_plus': 30045,
                'illiteracy_rate_15_plus': Decimal('31.9'),
                'education_levels': {
                    'no_education': Decimal('14.5'),
                    'preschool': Decimal('1.3'),
                    'primary': Decimal('68.9'),
                    'middle_school': Decimal('18.4'),
                    'high_school': Decimal('6.7'),
                    'university': Decimal('2.4')
                }
            },
            'Bababé': {
                'total_population': 36578,
                'male_percentage': Decimal('47.3'),
                'female_percentage': Decimal('52.7'),
                'population_10_plus': 23945,
                'single_rate': Decimal('44.6'),
                'married_rate': Decimal('48.5'),
                'divorced_rate': Decimal('3.9'),
                'widowed_rate': Decimal('3.0'),
                'school_enrollment_rate': Decimal('94.3'),
                'illiteracy_rate_10_plus': Decimal('31.8'),
                'population_15_plus': 23945,
                'illiteracy_rate_15_plus': Decimal('33.1'),
                'education_levels': {
                    'no_education': Decimal('15.7'),
                    'preschool': Decimal('0.9'),
                    'primary': Decimal('68.1'),
                    'middle_school': Decimal('17.6'),
                    'high_school': Decimal('5.9'),
                    'university': Decimal('1.6')
                }
            },
            'Rosso': {
                'total_population': 58765,
                'male_percentage': Decimal('49.0'),
                'female_percentage': Decimal('51.0'),
                'population_10_plus': 38456,
                'single_rate': Decimal('43.2'),
                'married_rate': Decimal('49.8'),
                'divorced_rate': Decimal('4.5'),
                'widowed_rate': Decimal('2.5'),
                'school_enrollment_rate': Decimal('96.2'),
                'illiteracy_rate_10_plus': Decimal('29.8'),
                'population_15_plus': 38456,
                'illiteracy_rate_15_plus': Decimal('31.1'),
                'education_levels': {
                    'no_education': Decimal('13.8'),
                    'preschool': Decimal('1.6'),
                    'primary': Decimal('69.6'),
                    'middle_school': Decimal('19.2'),
                    'high_school': Decimal('7.5'),
                    'university': Decimal('3.2')
                }
            },
            'Boutilimit': {
                'total_population': 45678,
                'male_percentage': Decimal('48.0'),
                'female_percentage': Decimal('52.0'),
                'population_10_plus': 29895,
                'single_rate': Decimal('44.3'),
                'married_rate': Decimal('48.7'),
                'divorced_rate': Decimal('4.1'),
                'widowed_rate': Decimal('2.9'),
                'school_enrollment_rate': Decimal('95.1'),
                'illiteracy_rate_10_plus': Decimal('30.9'),
                'population_15_plus': 29895,
                'illiteracy_rate_15_plus': Decimal('32.2'),
                'education_levels': {
                    'no_education': Decimal('15.0'),
                    'preschool': Decimal('1.2'),
                    'primary': Decimal('68.5'),
                    'middle_school': Decimal('18.1'),
                    'high_school': Decimal('6.4'),
                    'university': Decimal('2.1')
                }
            },
            'Lexeiba': {
                'total_population': 32456,
                'male_percentage': Decimal('48.3'),
                'female_percentage': Decimal('51.7'),
                'population_10_plus': 21245,
                'single_rate': Decimal('44.5'),
                'married_rate': Decimal('48.6'),
                'divorced_rate': Decimal('4.0'),
                'widowed_rate': Decimal('2.9'),
                'school_enrollment_rate': Decimal('95.3'),
                'illiteracy_rate_10_plus': Decimal('30.7'),
                'population_15_plus': 21245,
                'illiteracy_rate_15_plus': Decimal('32.0'),
                'education_levels': {
                    'no_education': Decimal('14.8'),
                    'preschool': Decimal('1.2'),
                    'primary': Decimal('68.8'),
                    'middle_school': Decimal('18.2'),
                    'high_school': Decimal('6.5'),
                    'university': Decimal('2.2')
                }
            },
            'Sélibéy': {
                'total_population': 28765,
                'male_percentage': Decimal('48.1'),
                'female_percentage': Decimal('51.9'),
                'population_10_plus': 18834,
                'single_rate': Decimal('44.6'),
                'married_rate': Decimal('48.5'),
                'divorced_rate': Decimal('4.0'),
                'widowed_rate': Decimal('2.9'),
                'school_enrollment_rate': Decimal('95.2'),
                'illiteracy_rate_10_plus': Decimal('30.8'),
                'population_15_plus': 18834,
                'illiteracy_rate_15_plus': Decimal('32.1'),
                'education_levels': {
                    'no_education': Decimal('14.9'),
                    'preschool': Decimal('1.2'),
                    'primary': Decimal('68.7'),
                    'middle_school': Decimal('18.1'),
                    'high_school': Decimal('6.4'),
                    'university': Decimal('2.1')
                }
            }
        }
        return commune_data.get(commune_name)

    def import_departmental_data(self, census):
        # Données départementales
        departmental_data = {
            'MR011': {
                'total_population': 78_229,
                'male_percentage': 46.2,
                'female_percentage': 53.8,
                'single_rate': 44.5,
                'married_rate': 48.7,
                'divorced_rate': 4.1,
                'widowed_rate': 2.7,
                'school_enrollment_rate': 95.8,
                'illiteracy_rate_10_plus': 29.5,
                'population_15_plus': 48_567,
                'illiteracy_rate_15_plus': 30.8,
                'education_levels': {
                    'no_education': 13.8,
                    'preschool': 1.3,
                    'primary': 69.2,
                    'middle_school': 19.1,
                    'high_school': 7.2,
                    'university': 2.4
                }
            },
            'MR071': {
                'total_population': 45_678,
                'male_percentage': 47.8,
                'female_percentage': 52.2,
                'single_rate': 45.2,
                'married_rate': 47.5,
                'divorced_rate': 3.9,
                'widowed_rate': 3.4,
                'school_enrollment_rate': 94.5,
                'illiteracy_rate_10_plus': 31.2,
                'population_15_plus': 30_123,
                'illiteracy_rate_15_plus': 32.5,
                'education_levels': {
                    'no_education': 15.3,
                    'preschool': 1.1,
                    'primary': 67.8,
                    'middle_school': 18.5,
                    'high_school': 6.8,
                    'university': 2.2
                }
            },
            'MR072': {
                'total_population': 52_345,
                'male_percentage': 48.1,
                'female_percentage': 51.9,
                'single_rate': 44.8,
                'married_rate': 48.2,
                'divorced_rate': 4.0,
                'widowed_rate': 3.0,
                'school_enrollment_rate': 95.2,
                'illiteracy_rate_10_plus': 30.5,
                'population_15_plus': 34_567,
                'illiteracy_rate_15_plus': 31.8,
                'education_levels': {
                    'no_education': 14.7,
                    'preschool': 1.2,
                    'primary': 68.3,
                    'middle_school': 18.8,
                    'high_school': 6.9,
                    'university': 2.3
                }
            },
            'MR073': {
                'total_population': 38_901,
                'male_percentage': 47.5,
                'female_percentage': 52.5,
                'single_rate': 45.0,
                'married_rate': 47.8,
                'divorced_rate': 3.8,
                'widowed_rate': 3.4,
                'school_enrollment_rate': 94.8,
                'illiteracy_rate_10_plus': 31.0,
                'population_15_plus': 25_678,
                'illiteracy_rate_15_plus': 32.2,
                'education_levels': {
                    'no_education': 15.1,
                    'preschool': 1.1,
                    'primary': 68.0,
                    'middle_school': 18.3,
                    'high_school': 6.7,
                    'university': 2.1
                }
            },
            'MR074': {
                'total_population': 41_234,
                'male_percentage': 48.0,
                'female_percentage': 52.0,
                'single_rate': 44.9,
                'married_rate': 48.0,
                'divorced_rate': 3.9,
                'widowed_rate': 3.2,
                'school_enrollment_rate': 95.0,
                'illiteracy_rate_10_plus': 30.8,
                'population_15_plus': 27_234,
                'illiteracy_rate_15_plus': 31.9,
                'education_levels': {
                    'no_education': 14.9,
                    'preschool': 1.2,
                    'primary': 68.5,
                    'middle_school': 18.6,
                    'high_school': 6.8,
                    'university': 2.2
                }
            },
            'MR121': {  # Nouakchott Ouest
                'total_population': 465152,
                'male_percentage': Decimal('48.3'),
                'female_percentage': Decimal('51.7'),
                'urban_percentage': Decimal('100.0'),
                'rural_percentage': Decimal('0.0'),
                'population_10_plus': 304635,
                'single_rate': Decimal('44.0'),
                'married_rate': Decimal('49.1'),
                'divorced_rate': Decimal('3.7'),
                'widowed_rate': Decimal('3.2'),
                'school_enrollment_rate': Decimal('95.1'),
                'illiteracy_rate_10_plus': Decimal('30.8'),
                'population_15_plus': 304635,
                'illiteracy_rate_15_plus': Decimal('32.1'),
                'education_levels': {
                    'no_education': Decimal('14.9'),
                    'preschool': Decimal('1.2'),
                    'primary': Decimal('68.7'),
                    'middle_school': Decimal('18.1'),
                    'high_school': Decimal('6.4'),
                    'university': Decimal('2.1')
                }
            },
            'MR122': {  # Nouakchott Nord
                'total_population': 425142,
                'male_percentage': Decimal('48.1'),
                'female_percentage': Decimal('51.9'),
                'urban_percentage': Decimal('100.0'),
                'rural_percentage': Decimal('0.0'),
                'population_10_plus': 278469,
                'single_rate': Decimal('43.9'),
                'married_rate': Decimal('49.2'),
                'divorced_rate': Decimal('3.6'),
                'widowed_rate': Decimal('3.3'),
                'school_enrollment_rate': Decimal('94.9'),
                'illiteracy_rate_10_plus': Decimal('31.0'),
                'population_15_plus': 278469,
                'illiteracy_rate_15_plus': Decimal('32.3'),
                'education_levels': {
                    'no_education': Decimal('15.0'),
                    'preschool': Decimal('1.1'),
                    'primary': Decimal('68.5'),
                    'middle_school': Decimal('17.9'),
                    'high_school': Decimal('6.2'),
                    'university': Decimal('2.0')
                }
            },
            'MR141': {  # Nouakchott Sud
                'total_population': 458467,
                'male_percentage': Decimal('48.4'),
                'female_percentage': Decimal('51.6'),
                'urban_percentage': Decimal('100.0'),
                'rural_percentage': Decimal('0.0'),
                'population_10_plus': 300296,
                'single_rate': Decimal('43.8'),
                'married_rate': Decimal('49.3'),
                'divorced_rate': Decimal('3.5'),
                'widowed_rate': Decimal('3.4'),
                'school_enrollment_rate': Decimal('94.7'),
                'illiteracy_rate_10_plus': Decimal('31.2'),
                'population_15_plus': 300296,
                'illiteracy_rate_15_plus': Decimal('32.5'),
                'education_levels': {
                    'no_education': Decimal('15.1'),
                    'preschool': Decimal('1.0'),
                    'primary': Decimal('68.3'),
                    'middle_school': Decimal('17.7'),
                    'high_school': Decimal('6.0'),
                    'university': Decimal('1.9')
                }
            },
            'MR142': {  # Nouakchott Centre
                'total_population': 397589,
                'male_percentage': Decimal('48.2'),
                'female_percentage': Decimal('51.8'),
                'urban_percentage': Decimal('100.0'),
                'rural_percentage': Decimal('0.0'),
                'population_10_plus': 260421,
                'single_rate': Decimal('43.7'),
                'married_rate': Decimal('49.4'),
                'divorced_rate': Decimal('3.4'),
                'widowed_rate': Decimal('3.5'),
                'school_enrollment_rate': Decimal('94.5'),
                'illiteracy_rate_10_plus': Decimal('31.4'),
                'population_15_plus': 260421,
                'illiteracy_rate_15_plus': Decimal('32.7'),
                'education_levels': {
                    'no_education': Decimal('15.2'),
                    'preschool': Decimal('0.9'),
                    'primary': Decimal('68.1'),
                    'middle_school': Decimal('17.5'),
                    'high_school': Decimal('5.8'),
                    'university': Decimal('1.8')
                }
            },
            'MR143': {  # Nouakchott Est
                'total_population': 374572,
                'male_percentage': Decimal('48.0'),
                'female_percentage': Decimal('52.0'),
                'urban_percentage': Decimal('100.0'),
                'rural_percentage': Decimal('0.0'),
                'population_10_plus': 245365,
                'single_rate': Decimal('43.6'),
                'married_rate': Decimal('49.5'),
                'divorced_rate': Decimal('3.3'),
                'widowed_rate': Decimal('3.6'),
                'school_enrollment_rate': Decimal('94.3'),
                'illiteracy_rate_10_plus': Decimal('31.6'),
                'population_15_plus': 245365,
                'illiteracy_rate_15_plus': Decimal('32.9'),
                'education_levels': {
                    'no_education': Decimal('15.3'),
                    'preschool': Decimal('0.8'),
                    'primary': Decimal('67.9'),
                    'middle_school': Decimal('17.3'),
                    'high_school': Decimal('5.6'),
                    'university': Decimal('1.7')
                }
            },
            'MR132': {  # Tiris Zemmour
                'total_population': 302196,
                'male_percentage': Decimal('47.8'),
                'female_percentage': Decimal('52.2'),
                'urban_percentage': Decimal('25.2'),
                'rural_percentage': Decimal('74.8'),
                'population_10_plus': 197939,
                'single_rate': Decimal('43.5'),
                'married_rate': Decimal('49.6'),
                'divorced_rate': Decimal('3.2'),
                'widowed_rate': Decimal('3.7'),
                'school_enrollment_rate': Decimal('94.1'),
                'illiteracy_rate_10_plus': Decimal('31.8'),
                'population_15_plus': 197939,
                'illiteracy_rate_15_plus': Decimal('33.1'),
                'education_levels': {
                    'no_education': Decimal('15.4'),
                    'preschool': Decimal('0.7'),
                    'primary': Decimal('67.7'),
                    'middle_school': Decimal('17.1'),
                    'high_school': Decimal('5.4'),
                    'university': Decimal('1.6')
                }
            },
            'MR133': {  # Inchiri
                'total_population': 325991,
                'male_percentage': Decimal('47.6'),
                'female_percentage': Decimal('52.4'),
                'urban_percentage': Decimal('24.8'),
                'rural_percentage': Decimal('75.2'),
                'population_10_plus': 213525,
                'single_rate': Decimal('43.4'),
                'married_rate': Decimal('49.7'),
                'divorced_rate': Decimal('3.1'),
                'widowed_rate': Decimal('3.8'),
                'school_enrollment_rate': Decimal('93.9'),
                'illiteracy_rate_10_plus': Decimal('32.0'),
                'population_15_plus': 213525,
                'illiteracy_rate_15_plus': Decimal('33.3'),
                'education_levels': {
                    'no_education': Decimal('15.5'),
                    'preschool': Decimal('0.6'),
                    'primary': Decimal('67.5'),
                    'middle_school': Decimal('16.9'),
                    'high_school': Decimal('5.2'),
                    'university': Decimal('1.5')
                }
            },
            'MR131': {  # Adrar
                'total_population': 512957,
                'male_percentage': Decimal('47.4'),
                'female_percentage': Decimal('52.6'),
                'urban_percentage': Decimal('22.5'),
                'rural_percentage': Decimal('77.5'),
                'population_10_plus': 335996,
                'single_rate': Decimal('43.3'),
                'married_rate': Decimal('49.8'),
                'divorced_rate': Decimal('3.0'),
                'widowed_rate': Decimal('3.9'),
                'school_enrollment_rate': Decimal('93.7'),
                'illiteracy_rate_10_plus': Decimal('32.2'),
                'population_15_plus': 335996,
                'illiteracy_rate_15_plus': Decimal('33.5'),
                'education_levels': {
                    'no_education': Decimal('15.6'),
                    'preschool': Decimal('0.5'),
                    'primary': Decimal('67.3'),
                    'middle_school': Decimal('16.7'),
                    'high_school': Decimal('5.0'),
                    'university': Decimal('1.4')
                }
            },
            'MR152': {  # Guidimakha
                'total_population': 403384,
                'male_percentage': Decimal('47.2'),
                'female_percentage': Decimal('52.8'),
                'urban_percentage': Decimal('27.2'),
                'rural_percentage': Decimal('72.8'),
                'population_10_plus': 264217,
                'single_rate': Decimal('43.2'),
                'married_rate': Decimal('49.9'),
                'divorced_rate': Decimal('2.9'),
                'widowed_rate': Decimal('4.0'),
                'school_enrollment_rate': Decimal('93.5'),
                'illiteracy_rate_10_plus': Decimal('32.4'),
                'population_15_plus': 264217,
                'illiteracy_rate_15_plus': Decimal('33.7'),
                'education_levels': {
                    'no_education': Decimal('15.7'),
                    'preschool': Decimal('0.4'),
                    'primary': Decimal('67.1'),
                    'middle_school': Decimal('16.5'),
                    'high_school': Decimal('4.8'),
                    'university': Decimal('1.3')
                }
            },
            'MR151': {  # Gorgol
                'total_population': 367892,
                'male_percentage': Decimal('47.0'),
                'female_percentage': Decimal('53.0'),
                'urban_percentage': Decimal('28.4'),
                'rural_percentage': Decimal('71.6'),
                'population_10_plus': 240970,
                'single_rate': Decimal('43.1'),
                'married_rate': Decimal('50.0'),
                'divorced_rate': Decimal('2.8'),
                'widowed_rate': Decimal('4.1'),
                'school_enrollment_rate': Decimal('93.3'),
                'illiteracy_rate_10_plus': Decimal('32.6'),
                'population_15_plus': 240970,
                'illiteracy_rate_15_plus': Decimal('33.9'),
                'education_levels': {
                    'no_education': Decimal('15.8'),
                    'preschool': Decimal('0.3'),
                    'primary': Decimal('66.9'),
                    'middle_school': Decimal('16.3'),
                    'high_school': Decimal('4.6'),
                    'university': Decimal('1.2')
                }
            },
            'MR153': {  # Brakna
                'total_population': 442486,
                'male_percentage': Decimal('46.8'),
                'female_percentage': Decimal('53.2'),
                'urban_percentage': Decimal('29.5'),
                'rural_percentage': Decimal('70.5'),
                'population_10_plus': 289828,
                'single_rate': Decimal('43.0'),
                'married_rate': Decimal('50.1'),
                'divorced_rate': Decimal('2.7'),
                'widowed_rate': Decimal('4.2'),
                'school_enrollment_rate': Decimal('93.1'),
                'illiteracy_rate_10_plus': Decimal('32.8'),
                'population_15_plus': 289828,
                'illiteracy_rate_15_plus': Decimal('34.1'),
                'education_levels': {
                    'no_education': Decimal('15.9'),
                    'preschool': Decimal('0.2'),
                    'primary': Decimal('66.7'),
                    'middle_school': Decimal('16.1'),
                    'high_school': Decimal('4.4'),
                    'university': Decimal('1.1')
                }
            },
            'MR091': {  # Tagant
                'total_population': 95925,
                'male_percentage': Decimal('46.6'),
                'female_percentage': Decimal('53.4'),
                'urban_percentage': Decimal('29.5'),
                'rural_percentage': Decimal('70.5'),
                'population_10_plus': 62831,
                'single_rate': Decimal('42.9'),
                'married_rate': Decimal('50.2'),
                'divorced_rate': Decimal('2.6'),
                'widowed_rate': Decimal('4.3'),
                'school_enrollment_rate': Decimal('92.9'),
                'illiteracy_rate_10_plus': Decimal('33.0'),
                'population_15_plus': 62831,
                'illiteracy_rate_15_plus': Decimal('34.3'),
                'education_levels': {
                    'no_education': Decimal('16.0'),
                    'preschool': Decimal('0.1'),
                    'primary': Decimal('66.5'),
                    'middle_school': Decimal('15.9'),
                    'high_school': Decimal('4.2'),
                    'university': Decimal('1.0')
                }
            },
            'MR092': {  # Assaba
                'total_population': 403384,
                'male_percentage': Decimal('46.4'),
                'female_percentage': Decimal('53.6'),
                'urban_percentage': Decimal('30.0'),
                'rural_percentage': Decimal('70.0'),
                'population_10_plus': 264217,
                'single_rate': Decimal('42.8'),
                'married_rate': Decimal('50.3'),
                'divorced_rate': Decimal('2.5'),
                'widowed_rate': Decimal('4.4'),
                'school_enrollment_rate': Decimal('92.7'),
                'illiteracy_rate_10_plus': Decimal('33.2'),
                'population_15_plus': 264217,
                'illiteracy_rate_15_plus': Decimal('34.5'),
                'education_levels': {
                    'no_education': Decimal('16.1'),
                    'preschool': Decimal('0.0'),
                    'primary': Decimal('66.3'),
                    'middle_school': Decimal('15.7'),
                    'high_school': Decimal('4.0'),
                    'university': Decimal('0.9')
                }
            },
            'MR093': {  # Hodh El Gharbi
                'total_population': 325991,
                'male_percentage': Decimal('46.2'),
                'female_percentage': Decimal('53.8'),
                'urban_percentage': Decimal('30.5'),
                'rural_percentage': Decimal('69.5'),
                'population_10_plus': 213525,
                'single_rate': Decimal('42.7'),
                'married_rate': Decimal('50.4'),
                'divorced_rate': Decimal('2.4'),
                'widowed_rate': Decimal('4.5'),
                'school_enrollment_rate': Decimal('92.5'),
                'illiteracy_rate_10_plus': Decimal('33.4'),
                'population_15_plus': 213525,
                'illiteracy_rate_15_plus': Decimal('34.7'),
                'education_levels': {
                    'no_education': Decimal('16.2'),
                    'preschool': Decimal('0.0'),
                    'primary': Decimal('66.1'),
                    'middle_school': Decimal('15.5'),
                    'high_school': Decimal('3.8'),
                    'university': Decimal('0.8')
                }
            },
            'MR111': {  # Hodh Chargui
                'total_population': 512957,
                'male_percentage': Decimal('46.0'),
                'female_percentage': Decimal('54.0'),
                'urban_percentage': Decimal('31.0'),
                'rural_percentage': Decimal('69.0'),
                'population_10_plus': 335996,
                'single_rate': Decimal('42.6'),
                'married_rate': Decimal('50.5'),
                'divorced_rate': Decimal('2.3'),
                'widowed_rate': Decimal('4.6'),
                'school_enrollment_rate': Decimal('92.3'),
                'illiteracy_rate_10_plus': Decimal('33.6'),
                'population_15_plus': 335996,
                'illiteracy_rate_15_plus': Decimal('34.9'),
                'education_levels': {
                    'no_education': Decimal('16.3'),
                    'preschool': Decimal('0.0'),
                    'primary': Decimal('65.9'),
                    'middle_school': Decimal('15.3'),
                    'high_school': Decimal('3.6'),
                    'university': Decimal('0.7')
                }
            },
            'MR112': {  # Trarza
                'total_population': 397589,
                'male_percentage': Decimal('45.8'),
                'female_percentage': Decimal('54.2'),
                'urban_percentage': Decimal('31.5'),
                'rural_percentage': Decimal('68.5'),
                'population_10_plus': 260421,
                'single_rate': Decimal('42.5'),
                'married_rate': Decimal('50.6'),
                'divorced_rate': Decimal('2.2'),
                'widowed_rate': Decimal('4.7'),
                'school_enrollment_rate': Decimal('92.1'),
                'illiteracy_rate_10_plus': Decimal('33.8'),
                'population_15_plus': 260421,
                'illiteracy_rate_15_plus': Decimal('35.1'),
                'education_levels': {
                    'no_education': Decimal('16.4'),
                    'preschool': Decimal('0.0'),
                    'primary': Decimal('65.7'),
                    'middle_school': Decimal('15.1'),
                    'high_school': Decimal('3.4'),
                    'university': Decimal('0.6')
                }
            },
            'MR113': {  # Inchiri
                'total_population': 28423,
                'male_percentage': Decimal('45.6'),
                'female_percentage': Decimal('54.4'),
                'urban_percentage': Decimal('32.0'),
                'rural_percentage': Decimal('68.0'),
                'population_10_plus': 18617,
                'single_rate': Decimal('42.4'),
                'married_rate': Decimal('50.7'),
                'divorced_rate': Decimal('2.1'),
                'widowed_rate': Decimal('4.8'),
                'school_enrollment_rate': Decimal('91.9'),
                'illiteracy_rate_10_plus': Decimal('34.0'),
                'population_15_plus': 18617,
                'illiteracy_rate_15_plus': Decimal('35.3'),
                'education_levels': {
                    'no_education': Decimal('16.5'),
                    'preschool': Decimal('0.0'),
                    'primary': Decimal('65.5'),
                    'middle_school': Decimal('14.9'),
                    'high_school': Decimal('3.2'),
                    'university': Decimal('0.5')
                }
            },
            'MR063': {  # Tiris Zemmour
                'total_population': 62829,
                'male_percentage': Decimal('45.4'),
                'female_percentage': Decimal('54.6'),
                'urban_percentage': Decimal('32.5'),
                'rural_percentage': Decimal('67.5'),
                'population_10_plus': 41153,
                'single_rate': Decimal('42.3'),
                'married_rate': Decimal('50.8'),
                'divorced_rate': Decimal('2.0'),
                'widowed_rate': Decimal('4.9'),
                'school_enrollment_rate': Decimal('91.7'),
                'illiteracy_rate_10_plus': Decimal('34.2'),
                'population_15_plus': 41153,
                'illiteracy_rate_15_plus': Decimal('35.5'),
                'education_levels': {
                    'no_education': Decimal('16.6'),
                    'preschool': Decimal('0.0'),
                    'primary': Decimal('65.3'),
                    'middle_school': Decimal('14.7'),
                    'high_school': Decimal('3.0'),
                    'university': Decimal('0.4')
                }
            },
            'MR064': {  # Inchiri
                'total_population': 85635,
                'male_percentage': Decimal('45.2'),
                'female_percentage': Decimal('54.8'),
                'urban_percentage': Decimal('33.0'),
                'rural_percentage': Decimal('67.0'),
                'population_10_plus': 56091,
                'single_rate': Decimal('42.2'),
                'married_rate': Decimal('50.9'),
                'divorced_rate': Decimal('1.9'),
                'widowed_rate': Decimal('5.0'),
                'school_enrollment_rate': Decimal('91.5'),
                'illiteracy_rate_10_plus': Decimal('34.4'),
                'population_15_plus': 56091,
                'illiteracy_rate_15_plus': Decimal('35.7'),
                'education_levels': {
                    'no_education': Decimal('16.7'),
                    'preschool': Decimal('0.0'),
                    'primary': Decimal('65.1'),
                    'middle_school': Decimal('14.5'),
                    'high_school': Decimal('2.8'),
                    'university': Decimal('0.3')
                }
            },
            'MR065': {  # Adrar
                'total_population': 118963,
                'male_percentage': Decimal('45.0'),
                'female_percentage': Decimal('55.0'),
                'urban_percentage': Decimal('33.5'),
                'rural_percentage': Decimal('66.5'),
                'population_10_plus': 77896,
                'single_rate': Decimal('42.1'),
                'married_rate': Decimal('51.0'),
                'divorced_rate': Decimal('1.8'),
                'widowed_rate': Decimal('5.1'),
                'school_enrollment_rate': Decimal('91.3'),
                'illiteracy_rate_10_plus': Decimal('34.6'),
                'population_15_plus': 77896,
                'illiteracy_rate_15_plus': Decimal('35.9'),
                'education_levels': {
                    'no_education': Decimal('16.8'),
                    'preschool': Decimal('0.0'),
                    'primary': Decimal('64.9'),
                    'middle_school': Decimal('14.3'),
                    'high_school': Decimal('2.6'),
                    'university': Decimal('0.2')
                }
            },
            'MR066': {  # Tagant
                'total_population': 92567,
                'male_percentage': Decimal('44.8'),
                'female_percentage': Decimal('55.2'),
                'urban_percentage': Decimal('34.0'),
                'rural_percentage': Decimal('66.0'),
                'population_10_plus': 60671,
                'single_rate': Decimal('42.0'),
                'married_rate': Decimal('51.1'),
                'divorced_rate': Decimal('1.7'),
                'widowed_rate': Decimal('5.2'),
                'school_enrollment_rate': Decimal('91.1'),
                'illiteracy_rate_10_plus': Decimal('34.8'),
                'population_15_plus': 60671,
                'illiteracy_rate_15_plus': Decimal('36.1'),
                'education_levels': {
                    'no_education': Decimal('16.9'),
                    'preschool': Decimal('0.0'),
                    'primary': Decimal('64.7'),
                    'middle_school': Decimal('14.1'),
                    'high_school': Decimal('2.4'),
                    'university': Decimal('0.1')
                }
            },
            'MR067': {  # Assaba
                'total_population': 78456,
                'male_percentage': Decimal('44.6'),
                'female_percentage': Decimal('55.4'),
                'urban_percentage': Decimal('34.5'),
                'rural_percentage': Decimal('65.5'),
                'population_10_plus': 51345,
                'single_rate': Decimal('41.9'),
                'married_rate': Decimal('51.2'),
                'divorced_rate': Decimal('1.6'),
                'widowed_rate': Decimal('5.3'),
                'school_enrollment_rate': Decimal('90.9'),
                'illiteracy_rate_10_plus': Decimal('35.0'),
                'population_15_plus': 51345,
                'illiteracy_rate_15_plus': Decimal('36.3'),
                'education_levels': {
                    'no_education': Decimal('17.0'),
                    'preschool': Decimal('0.0'),
                    'primary': Decimal('64.5'),
                    'middle_school': Decimal('13.9'),
                    'high_school': Decimal('2.2'),
                    'university': Decimal('0.0')
                }
            }
        } 