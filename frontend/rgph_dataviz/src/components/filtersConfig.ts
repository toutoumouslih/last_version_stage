import { Demographic } from '../types/types';

export type FilterOption = {
  id: string;
  label: string;
  field: keyof Demographic;
  type: 'number' | 'percentage';
  colorScale: string[];
  ranges: number[];
};

export type GeoLevelFilterOption = {
  id: string;
  label: string;
  level: 'region' | 'department' | 'commune';
};


export type FilterCategory = {
  id: string;
  title: string;
  options: FilterOption[];
};

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
    id: 'gender-distribution',
    title: 'Répartition par sexe',
    options: [
      {
        id: 'male-percentage',
        label: '% Hommes',
        field: 'male_percentage',
        type: 'percentage',
        colorScale: ['#F7FBFF', '#C6DBEF', '#6BAED6', '#3182BD', '#08519C', '#08306B'],
        ranges: [40, 45, 48, 52, 55, 60]
      },
      {
        id: 'female-percentage',
        label: '% Femmes',
        field: 'female_percentage',
        type: 'percentage',
        colorScale: ['#FFF5F0', '#FCAE91', '#FB6A4A', '#DE2D26', '#A50F15', '#67000D'],
        ranges: [40, 45, 48, 52, 55, 60]
      }
    ]
  },
  {
    id: 'marital-status',
    title: 'État matrimonial',
    options: [
      {
        id: 'single-rate',
        label: '% Célibataires',
        field: 'single_rate',
        type: 'percentage',
        colorScale: ['#F7FCF5', '#BAE4B3', '#74C476', '#31A354', '#006D2C', '#00441B'],
        ranges: [20, 30, 40, 50, 60, 70]
      },
      {
        id: 'married-rate',
        label: '% Mariés',
        field: 'married_rate',
        type: 'percentage',
        colorScale: ['#F7F4F9', '#D4B9DA', '#998EC3', '#8073AC', '#6A51A3', '#4A1486'],
        ranges: [20, 30, 40, 50, 60, 70]
      },
      {
        id: 'divorced-rate',
        label: '% Divorcés',
        field: 'divorced_rate',
        type: 'percentage',
        colorScale: ['#FEEDDE', '#FDBE85', '#FD8D3C', '#E6550D', '#A63603', '#7F2704'],
        ranges: [1, 2, 3, 5, 7, 10]
      },
      {
        id: 'widowed-rate',
        label: '% Veufs',
        field: 'widowed_rate',
        type: 'percentage',
        colorScale: ['#F1EEF6', '#BDC9E1', '#74A9CF', '#2B8CBE', '#045A8D', '#023858'],
        ranges: [1, 2, 3, 5, 7, 10]
      }
    ]
  },
  {
    id: 'education',
    title: 'Éducation',
    options: [
      {
        id: 'school-enrollment',
        label: 'Taux de scolarisation',
        field: 'school_enrollment_rate',
        type: 'percentage',
        colorScale: ['#F0F9E8', '#BAE4BC', '#7BCCC4', '#43A2CA', '#0868AC', '#084081'],
        ranges: [20, 40, 60, 70, 80, 90]
      },
      {
        id: 'illiteracy-10-plus',
        label: 'Taux d\'analphabétisme (10 ans +)',
        field: 'illiteracy_rate_10_plus',
        type: 'percentage',
        colorScale: ['#FEEBE2', '#FBB4B9', '#F768A1', '#C51B8A', '#7A0177', '#49006A'],
        ranges: [10, 20, 30, 40, 50, 60]
      },
      {
        id: 'illiteracy-15-plus',
        label: 'Taux d\'analphabétisme (15 ans +)',
        field: 'illiteracy_rate_15_plus',
        type: 'percentage',
        colorScale: ['#FEE6CE', '#FDAE6B', '#FD8D3C', '#E6550D', '#A63603', '#7F2704'],
        ranges: [10, 20, 30, 40, 50, 60]
      }
    ]
  }
];


export const GEO_LEVEL_FILTERS: GeoLevelFilterOption[] = [
  {
    id: 'region-level',
    label: 'Région',
    level: 'region'
  },
  {
    id: 'department-level',
    label: 'Moughataa',
    level: 'department'
  },
  {
    id: 'commune-level',
    label: 'Commune',
    level: 'commune'
  }
];