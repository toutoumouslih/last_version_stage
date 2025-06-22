export type Region = {
    id: number;
    adm1_en: string;
    geo_json: any;
  };
  
  export type Departement = {
    id: number;
    adm2_en: string;
    geo_json: any;
  };
  
  export type Commune = {
    id: number;
    adm3_en: string;
    geo_json: any;
  };

  // Dans votre fichier types.ts
export type GeoLevelFilterOption = {
  id: string;
  label: string;
  level: 'region' | 'department' | 'commune';
};

// Ajoutez cette interface à vos props existantes
interface FilterPanelProps {
  categories: FilterCategory[];
  activeFilter: FilterOption | null;
  onFilterSelect: (filter: FilterOption) => void;
  onClearFilter: () => void;
  onTogglePanel: () => void;
  showFilters: boolean;
  activeGeoLevel: 'region' | 'department' | 'commune'; // Propriété ajoutée pour le niveau géographique
  onGeoLevelSelect: (level: 'region' | 'department' | 'commune') => void; // Fonction ajoutée pour changer le niveau géographique
}

  
  export type Demographic = {
    id: number;
    [key: string]: any;
    zoneType?: 'region' | 'department' | 'commune';
    zoneId?: number;
    region: number | null;
    department: number | null;
    commune: number | null;
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
    census: number;
    country: number | null;
  };
  
  export type FilterOption = {
    id: string;
    label: string;
    field: keyof Demographic;
    type: 'number' | 'percentage';
    colorScale: string[];
    ranges: number[];
  };
  
  export type FilterCategory = {
    id: string;
    title: string;
    options: FilterOption[];
  };