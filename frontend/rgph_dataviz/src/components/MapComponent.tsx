import React, { useEffect, useState, useRef } from 'react';
import { MapContainer, TileLayer, GeoJSON, Marker, useMap } from 'react-leaflet';
import { FaEye, FaEyeSlash, FaDownload, FaSearch } from 'react-icons/fa';
import { Modal, Button, Alert } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { FILTER_CATEGORIES } from './filtersConfig';
import { FilterPanel } from './FilterPanel';
import { Region, Departement, Commune, Demographic, FilterOption } from '../types/types';
import debounce from 'lodash.debounce';
console.log('MapComponent loaded');

const MAURITANIA_BOUNDS = L.latLngBounds(
  L.latLng(14.5, -17.5),
  L.latLng(27.5, -4.5)
);

// Styles globaux pour les labels cliquables
const styles = `
  .clickable-zone-label {
    pointer-events: auto !important;
  }
  .clickable-zone-label div {
    transition: all 0.2s;
  }
  .clickable-zone-label:hover div {
    filter: brightness(1.1);
    transform: scale(1.05);
  }
`;

const MapControls = ({
  showNames,
  setShowNames,
  handleExportClick
}: {
  showNames: boolean,
  setShowNames: (show: boolean) => void,
  handleExportClick: () => void
}) => {
  return (
    <div className="leaflet-top leaflet-right" style={{ marginTop: '10px', marginRight: '10px' }}>
      <div className="leaflet-control leaflet-bar" style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
        <button
          title={showNames ? 'Masquer les noms' : 'Afficher les noms'}
          onClick={() => setShowNames(!showNames)}
          style={{
            backgroundColor: 'white',
            border: 'none',
            padding: '8px',
            borderRadius: '4px',
            cursor: 'pointer',
            boxShadow: '0 1px 5px rgba(0,0,0,0.4)',
            transition: 'background-color 0.2s ease, transform 0.2s ease',
            transform: 'scale(1)',
          }}
          onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.1)'}
          onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
        >
          {showNames ? <FaEyeSlash size={20} color="#FF6347" /> : <FaEye size={20} color="#4CAF50" />}
        </button>

        <button
          title="Exporter toutes les données"
          onClick={handleExportClick}
          style={{
            backgroundColor: 'white',
            border: 'none',
            padding: '8px',
            borderRadius: '4px',
            cursor: 'pointer',
            boxShadow: '0 1px 5px rgba(0,0,0,0.4)',
            transition: 'background-color 0.2s ease, transform 0.2s ease',
            transform: 'scale(1)',
          }}
          onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.1)'}
          onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
        >
          <FaDownload size={20} color="#2196F3" />
        </button>
      </div>
    </div>
  );
};

interface ZoneLabelsProps {
  regions: Region[];
  departements: Departement[];
  communes: Commune[];
  demographics: Demographic[];
  activeFilter: FilterOption | null;
  showNames: boolean;
  activeGeoLevel: 'region' | 'department' | 'commune';
  zoomLevel: number;
  selectedZoneId: number | null;
  onZoneClick: (id: number, level: 'region' | 'department' | 'commune') => void;
}

const ZoneLabels: React.FC<ZoneLabelsProps> = ({
  regions,
  departements,
  communes,
  demographics,
  activeFilter,
  showNames,
  activeGeoLevel,
  zoomLevel,
  selectedZoneId,
  onZoneClick
}) => {
  const map = useMap();
  const [currentZoom, setCurrentZoom] = useState(zoomLevel);

  useEffect(() => {
    const updateZoom = () => setCurrentZoom(map.getZoom());
    map.on('zoomend', updateZoom);
    return () => { map.off('zoomend', updateZoom); };
  }, [map]);

  const getDisplayValue = (data: Demographic | undefined) => {
    if (!data || !activeFilter) return '';
    // Supporte les champs imbriqués comme 'education_level.no_education'
    // @ts-ignore: field peut être string
    const fieldPath = String(activeFilter.field).split('.');
    let rawValue: any = data;
    for (const part of fieldPath) {
      if (rawValue && part in rawValue) {
        rawValue = rawValue[part];
      } else {
        rawValue = undefined;
        break;
      }
    }
    if (rawValue === null || rawValue === undefined || rawValue === '') return '';
    const numericValue = typeof rawValue === 'string' ? parseFloat(rawValue) : rawValue;
    return activeFilter.type === 'percentage'
      ? `${numericValue.toFixed(1)}%`
      : new Intl.NumberFormat('fr-FR').format(numericValue);
  };

  const getCenter = (geojson: any) => L.geoJSON(geojson).getBounds().getCenter();

  const createLabelIcon = (
    text: string, 
    id: number, 
    level: 'region' | 'department' | 'commune', 
    value: string = '', 
    isSelected: boolean = false
  ) => {
    const getBackgroundColor = () => {
      if (!value || !activeFilter) return isSelected ? '#FFD700' : 'transparent';

      const numericValue = parseFloat(value.replace('%', ''));
      
      if (activeFilter && activeFilter.colorScale && activeFilter.ranges) {
        for (let i = 0; i < activeFilter.ranges.length; i++) {
          if (numericValue <= activeFilter.ranges[i]) {
            return isSelected ? '#FFD700' : activeFilter.colorScale[i];
          }
        }
        return isSelected ? '#FFD700' : activeFilter.colorScale[activeFilter.colorScale.length - 1];
      }
      return isSelected ? '#FFD700' : '#3388ff';
    };

    return L.divIcon({
      className: 'clickable-zone-label',
      html: `
        <div style="
          ${showNames ? 'background: rgba(255,255,255,0.9);' : 'background: transparent;'}
          border-radius: 4px;
          padding: 2px 5px;
          font-size: 12px;
          text-align: center;
          font-weight: bold;
          ${showNames ? 'border: 1px solid #333;' : 'border: none;'}
          ${showNames ? 'box-shadow: 0 0 4px rgba(0,0,0,0.2);' : 'box-shadow: none;'}
          min-width: ${showNames ? '100px' : '60px'};
          ${isSelected ? 'border: 2px solid #FF4500 !important;' : ''}
          cursor: pointer;
        ">
          ${showNames ? `<div>${text}</div>` : ''}
          ${value ? `
            <div style="
              font-weight: normal; 
              font-size: 10px;
              ${!showNames ? `background: ${getBackgroundColor()};` : ''}
              ${!showNames ? 'padding: 2px 5px;' : ''}
              ${!showNames ? 'border-radius: 3px;' : ''}
              ${!showNames ? 'color: white;' : ''}
            ">
              ${value}
            </div>
          ` : ''}
        </div>
      `,
      iconSize: showNames ? [100, value ? 40 : 30] : [60, value ? 30 : 20],
      iconAnchor: showNames ? [50, value ? 20 : 15] : [30, value ? 15 : 10],
    });
  };

  return (
    <>
      <style>{styles}</style>
      
      {(activeGeoLevel === 'region' || currentZoom < 7) && regions.map(region => {
        const data = demographics.find(d => d.region === region.id);
        const value = getDisplayValue(data);
        const isSelected = selectedZoneId === region.id && activeGeoLevel === 'region';
        return (
          <Marker
            key={`region-label-${region.id}`}
            position={getCenter(region.geo_json)}
            icon={createLabelIcon(region.adm1_en, region.id, 'region', value, isSelected)}
            eventHandlers={{
              click: (e) => {
                e.originalEvent.stopPropagation();
                onZoneClick(region.id, 'region');
              }
            }}
          />
        );
      })}

      {(activeGeoLevel === 'department' || (currentZoom >= 7 && currentZoom < 9)) && departements.map(dep => {
        const data = demographics.find(d => d.department === dep.id);
        const value = getDisplayValue(data);
        const isSelected = selectedZoneId === dep.id && activeGeoLevel === 'department';
        return (
          <Marker
            key={`dep-label-${dep.id}`}
            position={getCenter(dep.geo_json)}
            icon={createLabelIcon(dep.adm2_en, dep.id, 'department', value, isSelected)}
            eventHandlers={{
              click: (e) => {
                e.originalEvent.stopPropagation();
                onZoneClick(dep.id, 'department');
              }
            }}
          />
        );
      })}
      
      {(activeGeoLevel === 'commune' || currentZoom >= 9) && communes.map(com => {
        const data = demographics.find(d => d.commune === com.id);
        const value = getDisplayValue(data);
        const isSelected = selectedZoneId === com.id && activeGeoLevel === 'commune';
        return (
          <Marker
            key={`com-label-${com.id}`}
            position={getCenter(com.geo_json)}
            icon={createLabelIcon(com.adm3_en, com.id, 'commune', value, isSelected)}
            eventHandlers={{
              click: (e) => {
                e.originalEvent.stopPropagation();
                onZoneClick(com.id, 'commune');
              }
            }}
          />
        );
      })}
    </>
  );
};

const normalize = (str: string) => str.normalize('NFD').replace(/[ -]/g, '').toLowerCase();

const MapComponent: React.FC = () => {
  const [activeGeoLevel, setActiveGeoLevel] = useState<'region' | 'department' | 'commune'>('region');
  const [showDownloadSuccess, setShowDownloadSuccess] = useState(false);
  const [regions, setRegions] = useState<Region[]>([]);
  const [departements, setDepartements] = useState<Departement[]>([]);
  const [communes, setCommunes] = useState<Commune[]>([]);
  const [demographics, setDemographics] = useState<Demographic[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [selectedData, setSelectedData] = useState<Demographic | null>(null);
  const [selectedZoneId, setSelectedZoneId] = useState<number | null>(null);
  const [activeFilter, setActiveFilter] = useState<FilterOption | null>(null);
  const [showFilters, setShowFilters] = useState(true);
  const [showNames, setShowNames] = useState(true);
  const [zoomLevel, setZoomLevel] = useState(6);
  const [availableYears, setAvailableYears] = useState<number[]>([]);
  const [selectedYear, setSelectedYear] = useState<number | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [highlightedZone, setHighlightedZone] = useState<{id: number, level: 'region'|'department'|'commune'}|null>(null);
  const mapRef = useRef<L.Map | null>(null);

  const handleGeoLevelSelect = (level: 'region' | 'department' | 'commune') => {
    setActiveGeoLevel(level);
    setSelectedZoneId(null);
    if (mapRef.current) {
      const newZoom = level === 'region' ? 6 : level === 'department' ? 8 : 10;
      mapRef.current.setZoom(newZoom);
    }
  };

  const handleExportClick = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/export-all-data/?year=${selectedYear}`);
      if (response.ok) {
        const blob = await response.blob();
        // Forcer le nom du fichier côté frontend
        const filename = `donnees_mauritanie_${selectedYear}.xlsx`;
        const file = new File([blob], filename, { type: blob.type });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(file);
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        setShowDownloadSuccess(true);
        setTimeout(() => setShowDownloadSuccess(false), 3000);
      } else {
        alert('Erreur lors du téléchargement du fichier.');
      }
    } catch (error) {
      console.error("Erreur lors de l'exportation des données :", error);
    }
  };

  const handleExportZoneData = async (zoneId: number, zoneType: 'region' | 'department' | 'commune') => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/export-zone-data/${zoneId}/${zoneType}/?year=${selectedYear}`);
      if (response.ok) {
        const blob = await response.blob();
        // Forcer le nom du fichier côté frontend
        const filename = `donnees_${zoneType}_${zoneId}_${selectedYear}.xlsx`;
        const file = new File([blob], filename, { type: blob.type });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(file);
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        setShowDownloadSuccess(true);
        setTimeout(() => setShowDownloadSuccess(false), 3000);
      } else {
        alert('Erreur lors du téléchargement des données de la zone.');
      }
    } catch (error) {
      console.error("Erreur lors de l'exportation des données de la zone :", error);
    }
  };

  useEffect(() => {
    const loadData = async () => {
      try {
        // Charger les années disponibles
        const yearsResponse = await fetch('http://127.0.0.1:8000/api/api/census-years/');
        const yearsData = await yearsResponse.json();
        setAvailableYears(yearsData);
        
        // Définir l'année par défaut (la plus récente)
        if (yearsData.length > 0) {
          const defaultYear = Math.max(...yearsData);
          setSelectedYear(defaultYear);
        }

        const [regionsData, depsData, communesData] = await Promise.all([
          fetch('http://127.0.0.1:8000/api/api/regions/').then(res => res.json()),
          fetch('http://127.0.0.1:8000/api/api/departments/').then(res => res.json()),
          fetch('http://127.0.0.1:8000/api/api/communes/').then(res => res.json()),
        ]);
        setRegions(regionsData);
        setDepartements(depsData);
        setCommunes(communesData);
      } catch (error) {
        console.error("Error loading data:", error);
      }
    };
    loadData();
  }, []);

  // Charger les données démographiques quand l'année change
  useEffect(() => {
    const loadDemographicData = async () => {
      if (selectedYear) {
        try {
          const response = await fetch(`http://127.0.0.1:8000/api/api/demographics/?year=${selectedYear}`);
          const demoData = await response.json();
          setDemographics(demoData);
        } catch (error) {
          console.error("Error loading demographic data:", error);
        }
      }
    };
    loadDemographicData();
  }, [selectedYear]);

  const handleFeatureClick = (featureId: number, level: 'region' | 'department' | 'commune') => {
    const field = level === 'region' ? 'region' : level === 'department' ? 'department' : 'commune';
    const data = demographics.find(d => d[field] === featureId);

    if (data) {
      setSelectedData({
        ...data,
        zoneType: level,
        zoneId: featureId
      });
      setSelectedZoneId(featureId);
      setShowModal(true);
    }
  };

  const getColorForValue = (value: number, filter: FilterOption | null): string => {
    if (!filter) return '#3388ff';
    for (let i = 0; i < filter.ranges.length; i++) {
      if (value <= filter.ranges[i]) return filter.colorScale[i];
    }
    return filter.colorScale[filter.colorScale.length - 1];
  };

  const getStyle = (id: number, level: 'region' | 'department' | 'commune') => {
    const field = level === 'region' ? 'region' : level === 'department' ? 'department' : 'commune';
    const data = demographics.find(d => d[field] === id);
    const isSelected = selectedZoneId === id && activeGeoLevel === level;

    if (!activeFilter) {
      return {
        color: isSelected ? '#FF4500' : '#555',
        weight: isSelected ? 3 : 1,
        fillOpacity: 0.2,
        fillColor: isSelected ? '#FFD700' : '#3388ff'
      };
    }

    const value = data ? parseFloat(data[activeFilter.field] as any) : 0;

    return {
      color: isSelected ? '#FF4500' : '#555',
      weight: isSelected ? 3 : 1,
      fillOpacity: 0.7,
      fillColor: isSelected ? '#FFD700' : getColorForValue(value, activeFilter)
    };
  };

  const demographicLabels: Record<string, string> = {
    total_population: 'Population totale',
    male_percentage: '% Hommes',
    female_percentage: '% Femmes',
    urban_percentage: '% Urbain',
    rural_percentage: '% Rural',
    population_10_plus: 'Population 10 ans et +',
    single_rate: '% Célibataires',
    married_rate: '% Mariés',
    divorced_rate: '% Divorcés',
    widowed_rate: '% Veufs/veuves',
    school_enrollment_rate: 'Taux de scolarisation',
    illiteracy_rate_10_plus: "Taux d'analphabétisme (10+)",
    population_15_plus: 'Population 15 ans et +',
    illiteracy_rate_15_plus: "Taux d'analphabétisme (15+)",
  };

  // Recherche avancée (auto-complétion, insensible à la casse/accents)
  const allZones = [
    ...regions.map(r => ({ id: r.id, name: r.adm1_en, level: 'region', geo_json: r.geo_json })),
    ...departements.map(d => ({ id: d.id, name: d.adm2_en, level: 'department', geo_json: d.geo_json })),
    ...communes.map(c => ({ id: c.id, name: c.adm3_en, level: 'commune', geo_json: c.geo_json })),
  ];
  const handleSearch = debounce((value: string) => {
    const term = normalize(value);
    if (!term) { setSearchResults([]); return; }
    setSearchResults(
      allZones.filter(z => normalize(z.name).includes(term)).slice(0, 7)
    );
  }, 200);
  useEffect(() => { handleSearch(searchTerm); }, [searchTerm, regions, departements, communes]);
  const handleSelectZone = (zone: any) => {
    setHighlightedZone({ id: zone.id, level: zone.level });
    setSearchTerm(zone.name);
    setSearchResults([]);
    setActiveGeoLevel(zone.level);
    setSelectedZoneId(zone.id);
    if (mapRef.current) {
      const bounds = L.geoJSON(zone.geo_json).getBounds();
      mapRef.current.fitBounds(bounds, { maxZoom: 10 });
    }
  };

  // Ajoute la fonction de sélection de zone depuis la recherche
  const handleZoneSearchSelect = (zoneId: number, level: 'region' | 'department' | 'commune') => {
    setActiveGeoLevel(level);
    setSelectedZoneId(zoneId);
    // Centre la carte sur la zone
    let zone = null;
    if (level === 'region') zone = regions.find(r => r.id === zoneId);
    if (level === 'department') zone = departements.find(d => d.id === zoneId);
    if (level === 'commune') zone = communes.find(c => c.id === zoneId);
    if (zone && mapRef.current) {
      const bounds = L.geoJSON(zone.geo_json).getBounds();
      mapRef.current.fitBounds(bounds, { maxZoom: 10 });
    }
    // Ouvre la modale si les données existent
    const field = level === 'region' ? 'region' : level === 'department' ? 'department' : 'commune';
    const data = demographics.find(d => d[field] === zoneId);
    if (data) {
      setSelectedData({ ...data, zoneType: level, zoneId });
      setShowModal(true);
    }
  };

  return (
    <div style={{ display: 'flex', height: '100vh', flexDirection: 'column' }}>
      {showDownloadSuccess && (
        <Alert variant="success" onClose={() => setShowDownloadSuccess(false)} dismissible style={{ position: 'fixed', top: '20px', right: '20px', zIndex: 9999 }}>
          <Alert.Heading>Le fichier a été téléchargé avec succès !</Alert.Heading>
          <p>Votre fichier d'exportation est prêt à être utilisé.</p>
        </Alert>
      )}

      <div style={{ padding: '10px', backgroundColor: '#f8f9fa', borderBottom: '1px solid #dee2e6', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h4 style={{ margin: 0 }}>Carte de la Mauritanie</h4>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <label htmlFor="year-select" style={{ fontWeight: 'bold', marginRight: '5px' }}>
            Année de recensement:
          </label>
          <select
            id="year-select"
            value={selectedYear || ''}
            onChange={(e) => setSelectedYear(Number(e.target.value))}
            style={{
              padding: '5px 10px',
              borderRadius: '4px',
              border: '1px solid #ccc',
              backgroundColor: 'white',
              fontSize: '14px',
              cursor: 'pointer'
            }}
          >
            {availableYears.map(year => (
              <option key={year} value={year}>
                {year}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div style={{ display: 'flex', flex: 1, overflow: 'hidden' }}>
        <FilterPanel 
          categories={FILTER_CATEGORIES} 
          activeFilter={activeFilter} 
          onFilterSelect={setActiveFilter} 
          onClearFilter={() => setActiveFilter(null)} 
          onTogglePanel={() => setShowFilters(!showFilters)} 
          showFilters={showFilters} 
          activeGeoLevel={activeGeoLevel}
          onGeoLevelSelect={handleGeoLevelSelect}
          regions={regions}
          departements={departements}
          communes={communes}
          onZoneSearchSelect={handleZoneSearchSelect}
        /> 
        <div style={{ flex: 1, position: 'relative', height: '100%', display: 'flex', flexDirection: 'column' }}>
          <div style={{ height: '70%', width: '100%', position: 'relative' }}>
            <MapContainer 
              center={[20.5, -10.5]} 
              zoom={6} 
              style={{ height: '100%', width: '100%' }} 
              minZoom={5} 
              maxBounds={MAURITANIA_BOUNDS}
              ref={(map) => {
                if (map) {
                  mapRef.current = map;
                  setZoomLevel(map.getZoom());
                  map.on('zoomend', () => setZoomLevel(map.getZoom()));
                }
              }}
            >
              <TileLayer url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}" attribution='&copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community' />
              <TileLayer url="https://stamen-tiles-{s}.a.ssl.fastly.net/toner-hybrid/{z}/{x}/{y}{r}.png" attribution='Map tiles by <a href="http://stamen.com">Stamen Design</a>' />
              <MapControls showNames={showNames} setShowNames={setShowNames} handleExportClick={handleExportClick} />
              
              {regions.map(region => (
                <GeoJSON 
                  key={region.id} 
                  data={region.geo_json} 
                  style={() => getStyle(region.id, 'region')} 
                  eventHandlers={{ 
                    click: (e) => {
                      e.originalEvent.stopPropagation();
                      handleFeatureClick(region.id, 'region');
                    }
                  }}
                  bubblingMouseEvents={false}
                />
              ))}
              
              {departements.map(dep => (
                <GeoJSON 
                  key={dep.id} 
                  data={dep.geo_json} 
                  style={() => getStyle(dep.id, 'department')} 
                  eventHandlers={{ 
                    click: (e) => {
                      e.originalEvent.stopPropagation();
                      handleFeatureClick(dep.id, 'department');
                    }
                  }}
                  bubblingMouseEvents={false}
                />
              ))}
              
              {communes.map(com => (
                <GeoJSON 
                  key={com.id} 
                  data={com.geo_json} 
                  style={() => getStyle(com.id, 'commune')} 
                  eventHandlers={{ 
                    click: (e) => {
                      e.originalEvent.stopPropagation();
                      handleFeatureClick(com.id, 'commune');
                    }
                  }}
                />
              ))}
              
              <ZoneLabels 
                regions={regions} 
                departements={departements} 
                communes={communes} 
                demographics={demographics} 
                activeFilter={activeFilter} 
                showNames={showNames}
                activeGeoLevel={activeGeoLevel}
                zoomLevel={zoomLevel}
                selectedZoneId={selectedZoneId}
                onZoneClick={handleFeatureClick}
              />
            </MapContainer>
          </div>

          <div style={{ height: '30%', padding: '10px', borderTop: '1px solid #eee', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#666' }}>
            <p>Cliquez sur une zone ou son nom pour voir les détails (niveau actuel: {activeGeoLevel})</p>
          </div>
        </div>
      </div>

      {selectedData && (
        <Modal show={showModal} onHide={() => setShowModal(false)} size="lg">
          <Modal.Header closeButton>
            <Modal.Title>
              Détails de la {selectedData.zoneType === 'commune' ? 'Commune' : 
                            selectedData.zoneType === 'department' ? 'Moughataa' : 'Région'}
              {selectedYear && ` - Recensement ${selectedYear}`}
            </Modal.Title>
          </Modal.Header>
          <Modal.Body style={{ maxHeight: '70vh', overflowY: 'auto' }}>
            <h5 style={{ marginTop: 0, marginBottom: '1rem', color: '#366092', fontWeight: 600 }}>Informations démographiques</h5>
            <table className="table table-bordered" style={{ background: '#f9f9f9', borderRadius: 8 }}>
              <tbody>
                {(() => {
                  const maritalFields = [
                    'single_rate', 'married_rate', 'divorced_rate', 'widowed_rate'
                  ];
                  const educationIndicators = [
                    'school_enrollment_rate',
                    'illiteracy_rate_10_plus',
                    'illiteracy_rate_15_plus'
                  ];
                  let hasMaritalSubtitle = false;
                  let hasEducationSubtitle = false;
                  let rows: React.ReactNode[] = [];
                  let buffer: React.ReactNode[] = [];
                  Object.entries(selectedData)
                    .filter(([key]) =>
                      !["commune", "region", "department", "country", "id", "census", "zoneType", "zoneId", "education_level"].includes(key)
                    )
                    .forEach(([key, value], idx, arr) => {
                      const isPercent = [
                        'percentage', 'rate', 'taux', 'pourcentage', 'illiteracy', 'school_enrollment'
                      ].some(substr => key.toLowerCase().includes(substr));
                      const label = demographicLabels[key] || key;
                      let displayValue = String(value);
                      if (isPercent && value !== null && value !== undefined && value !== '') {
                        displayValue = value + ' %';
                      }
                      // Bloc État matrimonial
                      if (!hasMaritalSubtitle && maritalFields.includes(key)) {
                        hasMaritalSubtitle = true;
                        if (buffer.length > 0) rows = rows.concat(buffer), buffer = [];
                        rows.push(
                          <tr key="subtitle-marital-block">
                            <td colSpan={2} style={{ padding: 0, border: 'none' }}>
                              <h5 style={{ margin: '18px 0 8px 0', color: '#366092', fontWeight: 600 }}>État matrimonial</h5>
                            </td>
                          </tr>
                        );
                      }
                      // Bloc Indicateurs d'éducation
                      if (!hasEducationSubtitle && educationIndicators.includes(key)) {
                        hasEducationSubtitle = true;
                        if (buffer.length > 0) rows = rows.concat(buffer), buffer = [];
                        rows.push(
                          <tr key="subtitle-education-block">
                            <td colSpan={2} style={{ padding: 0, border: 'none' }}>
                              <h5 style={{ margin: '18px 0 8px 0', color: '#366092', fontWeight: 600 }}>Indicateurs d'éducation</h5>
                            </td>
                          </tr>
                        );
                      }
                      buffer.push(
                        <tr key={key} style={{ verticalAlign: 'middle' }}>
                          <td style={{ fontWeight: 600, color: '#366092', width: '60%', padding: '8px 12px' }}>{label}</td>
                          <td style={{ textAlign: 'right', width: '40%', padding: '8px 12px', fontSize: '1rem' }}>{displayValue}</td>
                        </tr>
                      );
                    });
                  if (buffer.length > 0) rows = rows.concat(buffer);
                  return rows;
                })()}
              </tbody>
            </table>
            {/* Titre Niveaux d'éducation toujours visible */}
            <h5 style={{ marginTop: '2rem', marginBottom: '1rem', color: '#366092', fontWeight: 600 }}>Niveaux d'éducation</h5>
            {selectedData.education_level ? (
              <table className="table table-bordered" style={{ background: '#f9f9f9', borderRadius: 8 }}>
                <tbody>
                  {Object.entries(selectedData.education_level).map(([key, value]) => {
                    const labels: Record<string, string> = {
                      no_education: 'Aucun niveau',
                      preschool: 'Préscolaire',
                      primary: 'Primaire',
                      middle_school: 'Collège',
                      high_school: 'Lycée',
                      university: 'Université'
                    };
                    // Tous les niveaux d'éducation sont des pourcentages
                    let displayValue = value !== null && value !== undefined && value !== '' ? value + ' %' : '';
                    return (
                      <tr key={key} style={{ verticalAlign: 'middle' }}>
                        <td style={{ fontWeight: 600, color: '#366092', width: '60%', padding: '8px 12px' }}>{labels[key] || key}</td>
                        <td style={{ textAlign: 'right', width: '40%', padding: '8px 12px', fontSize: '1rem' }}>{displayValue}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            ) : (
              <div style={{ color: '#888', fontStyle: 'italic', marginBottom: '1rem' }}>
                Pas de données de niveaux d'éducation disponibles.
              </div>
            )}
          </Modal.Body>
          <Modal.Footer>
            <Button 
              variant="success" 
              onClick={() => {
                if (selectedData.zoneType && selectedData.zoneId) {
                  handleExportZoneData(selectedData.zoneId, selectedData.zoneType);
                }
              }}
              disabled={!selectedData.zoneType || !selectedData.zoneId}
            >
              <FaDownload style={{ marginRight: '8px' }} />
              Exporter les données de cette {selectedData.zoneType === 'commune' ? 'commune' : 
                                          selectedData.zoneType === 'department' ? 'département' : 'région'}
            </Button>
            <Button variant="secondary" onClick={() => setShowModal(false)}>
              Fermer
            </Button>
          </Modal.Footer>
        </Modal>
      )}

      {/* Barre de recherche avancée flottante */}
      {/* <div style={{ position: 'absolute', top: 16, left: 70, zIndex: 10, width: 1 }}>
        <div style={{ display: 'flex', alignItems: 'center', background: '#fff', borderRadius: 8, boxShadow: '0 2px 8px rgba(0,0,0,0.10)', padding: '4px 12px', gap: 8 }}>
          <FaSearch color="#366092" />
          <input
            type="text"
            placeholder="Rechercher une zone..."
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            style={{ border: 'none', outline: 'none', fontSize: 15, flex: 1, background: 'transparent', color: '#222', padding: '6px 0' }}
          />
        </div>
        {searchResults.length > 0 && (
          <div style={{ background: '#fff', borderRadius: 8, boxShadow: '0 2px 8px rgba(0,0,0,0.15)', marginTop: 2, maxHeight: 220, overflowY: 'auto', position: 'absolute', width: '100%' }}>
            {searchResults.map(zone => (
              <div
                key={zone.level + '-' + zone.id}
                onClick={() => handleSelectZone(zone)}
                style={{ padding: '10px 14px', cursor: 'pointer', color: '#366092', fontWeight: 500, borderBottom: '1px solid #f0f0f0', background: highlightedZone && highlightedZone.id === zone.id && highlightedZone.level === zone.level ? '#eaf1fa' : 'transparent' }}
              >
                {zone.name} <span style={{ fontSize: 12, color: '#888', fontWeight: 400 }}>({zone.level === 'region' ? 'Région' : zone.level === 'department' ? 'Moughataa' : 'Commune'})</span>
              </div>
            ))}
          </div>
        )}
      </div> */}
    </div>
  );
};

export default MapComponent;