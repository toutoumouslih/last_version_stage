// src/types/DemographicData.ts

export interface DemographicData {
    [key: string]: any;
    department?: number;
    commune?: number;
    zoneType?: 'region' | 'department' | 'commune';
    zoneId?: number;
    id: number;
    total_population: number;
    male_percentage: string;
    female_percentage: string;
    urban_percentage: string;
    rural_percentage: string;
    population_10_plus: number;
    single_rate: string;
    married_rate: string;
    divorced_rate: string;
    widowed_rate: string;
    school_enrollment_rate: string;
    illiteracy_rate_10_plus: string;
    population_15_plus: number;
    illiteracy_rate_15_plus: string;
    region: number;
  }
  