import axios from 'axios';

// Configuration de l'URL de l'API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

// Configuration d'Axios pour gérer les CORS
axios.defaults.withCredentials = true;

export interface DemographicData {
  total_population: number;
  male_percentage: number;
  female_percentage: number;
  urban_percentage: number;
  rural_percentage: number;
  population_10_plus: number;
  single_rate: number;
  married_rate: number;
  divorced_rate: number;
  widowed_rate: number;
  school_enrollment_rate: number;
  illiteracy_rate_10_plus: number;
  population_15_plus: number;
  illiteracy_rate_15_plus: number;
}

// Interface pour la géométrie GeoJSON
export interface GeoJSONGeometry {
  type: "Point" | "MultiPoint" | "LineString" | "MultiLineString" | "Polygon" | "MultiPolygon" | "GeometryCollection";
  coordinates: number[][] | number[][][] | number[][][][];
}

export interface Region {
  id: number;
  name: string;
  code: string;
  geometry: GeoJSONGeometry;
  demographic_data?: DemographicData;
}

export interface Department {
  id: number;
  name: string;
  code: string;
  region_id: number;
  geometry: GeoJSONGeometry;
  demographic_data?: DemographicData;
}

export interface Commune {
  id: number;
  name: string;
  code: string;
  department_id: number;
  geometry: GeoJSONGeometry;
  demographic_data?: DemographicData;
}

interface RegionResponse {
  id: number;
  adm0_en: string;
  adm0_pcode: string;
  adm1_en: string;
  adm1_pcode: string;
  geo_json: GeoJSONGeometry;
}

interface DepartmentResponse {
  id: number;
  adm0_en: string;
  adm0_pcode: string;
  adm1_en: string;
  adm1_pcode: string;
  adm2_en: string;
  adm2_pcode: string;
  geo_json: GeoJSONGeometry;
}

interface CommuneResponse {
  id: number;
  adm0_en: string;
  adm0_pcode: string;
  adm1_en: string;
  adm1_pcode: string;
  adm2_en: string;
  adm2_pcode: string;
  adm3_en: string;
  adm3_pcode: string;
  geo_json: GeoJSONGeometry;
}

const api = {
  // Récupérer toutes les régions
  getRegions: async (): Promise<Region[]> => {
    try {
      const response = await axios.get(`${API_BASE_URL}/regions/`);
      console.log('Raw API response:', response.data);
      console.log('First region geo_json:', response.data[0]?.geo_json);
      if (!response.data || !Array.isArray(response.data)) {
        console.error('Invalid response format:', response.data);
        return [];
      }
      
      return response.data.map((region: RegionResponse) => ({
        id: region.id,
        name: region.adm1_en,
        code: region.adm1_pcode,
        geometry: region.geo_json
      }));
    } catch (error) {
      console.error('Error fetching regions:', error);
      return [];
    }
  },

  // Récupérer les départements d'une région
  getDepartments: async (regionId?: number): Promise<Department[]> => {
    try {
      const url = regionId 
        ? `${API_BASE_URL}/departments/${regionId}/`
        : `${API_BASE_URL}/departments/`;
      const response = await axios.get(url);
      if (!response.data || !Array.isArray(response.data)) {
        console.error('Invalid response format:', response.data);
        return [];
      }
      
      return response.data.map((dept: DepartmentResponse) => ({
        id: dept.id,
        name: dept.adm2_en,
        code: dept.adm2_pcode,
        region_id: regionId || 0,
        geometry: dept.geo_json
      }));
    } catch (error) {
      console.error('Error fetching departments:', error);
      return [];
    }
  },

  // Récupérer les communes d'un département
  getCommunes: async (departmentId?: number): Promise<Commune[]> => {
    try {
      const url = departmentId 
        ? `${API_BASE_URL}/communes/${departmentId}/`
        : `${API_BASE_URL}/communes/`;
      const response = await axios.get(url);
      if (!response.data || !Array.isArray(response.data)) {
        console.error('Invalid response format:', response.data);
        return [];
      }
      
      return response.data.map((commune: CommuneResponse) => ({
        id: commune.id,
        name: commune.adm3_en,
        code: commune.adm3_pcode,
        department_id: departmentId || 0,
        geometry: commune.geo_json
      }));
    } catch (error) {
      console.error('Error fetching communes:', error);
      return [];
    }
  },

  // Récupérer les données démographiques pour une zone administrative
  getDemographicData: async (code: string): Promise<DemographicData> => {
    const response = await axios.get(`${API_BASE_URL}/statistics/${code}/`);
    return response.data;
  }
};

export default api;
