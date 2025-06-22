import { FilterCategory } from '../types/types';

export const FILTER_CATEGORIES: FilterCategory[] = [
  {
    id: 'population',
    title: 'Population',
    options: [
      {
        id: 'total-population',
        label: 'Population totale',
        field: 'total_population',
        type: 'number',
        colorScale: ['#FED976', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026'],
        ranges: [20000, 50000, 100000, 200000, 500000, 1000000]
      },
      {
        id: 'population-10-plus',
        label: 'Population 10 ans +',
        field: 'population_10_plus',
        type: 'number',
        colorScale: ['#E5F5E0', '#A1D99B', '#41AB5D', '#238B45', '#006D2C', '#00441B'],
        ranges: [10000, 25000, 50000, 100000, 250000, 500000]
      }
    ]
  },
  {
    id: 'gender',
    title: 'Répartition par sexe',
    options: [
      {
        id: 'male-percentage',
        label: '% Hommes',
        field: 'male_percentage',
        type: 'percentage',
        colorScale: ['#F7FBFF', '#C6DBEF', '#6BAED6', '#3182BD', '#08519C', '#08306B'],
        ranges: [40, 45, 48, 52, 55, 60]
      }
    ]
  }
];