import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toutoustage.settings')
django.setup()

from myapp.models import DemographicData, Census

def main():
    try:
        census = Census.objects.get(year=2023)
        print('Total records:', DemographicData.objects.count())
        
        print('\nRegional data:')
        for data in DemographicData.objects.filter(region__isnull=False):
            print(f'{data.region.name}: Population={data.total_population}')
        
        print('\nDepartmental data:')
        for data in DemographicData.objects.filter(department__isnull=False):
            print(f'{data.department.name}: Population={data.total_population}')
        
        print('\nCommunal data:')
        for data in DemographicData.objects.filter(commune__isnull=False):
            print(f'{data.commune.name}: Population={data.total_population}')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main() 