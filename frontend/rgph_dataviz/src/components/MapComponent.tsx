import React, { useEffect, useState, useRef } from 'react';
import { MapContainer, TileLayer, GeoJSON, Marker, useMap } from 'react-leaflet';
import { FaEye, FaEyeSlash, FaDownload } from 'react-icons/fa';
import { Modal, Button, Alert } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { FILTER_CATEGORIES } from './filtersConfig';
import { FilterPanel } from './FilterPanel';
import { Region, Departement, Commune, Demographic, FilterOption } from '../types/types';

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
    const rawValue = data[activeFilter.field];
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
      const response = await fetch('http://127.0.0.1:8000/api/export-all-data/');
      if (response.ok) {
        const blob = await response.blob();
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'all_data_export.xlsx';
        link.click();
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
      const response = await fetch(`http://127.0.0.1:8000/api/export-zone-data/${zoneId}/${zoneType}/`);
      if (response.ok) {
        const blob = await response.blob();
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `${zoneType}_data_${zoneId}.xlsx`;
        link.click();
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
        const [regionsData, depsData, communesData, demoData] = await Promise.all([
          fetch('http://127.0.0.1:8000/api/api/regions/').then(res => res.json()),
          fetch('http://127.0.0.1:8000/api/api/departments/').then(res => res.json()),
          fetch('http://127.0.0.1:8000/api/api/communes/').then(res => res.json()),
          fetch('http://127.0.0.1:8000/api/api/demographics/').then(res => res.json())
        ]);
        setRegions(regionsData);
        setDepartements(depsData);
        setCommunes(communesData);
        setDemographics(demoData);
      } catch (error) {
        console.error("Error loading data:", error);
      }
    };
    loadData();
  }, []);

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
        /> 
        <div style={{ flex: 1, position: 'relative', height: '100%', display: 'flex', flexDirection: 'column' }}>
          <div style={{ height: '70%', width: '100%', position: 'relative' }}>
            <MapContainer 
              center={[20.5, -10.5]} 
              zoom={6} 
              style={{ height: '100%', width: '100%' }} 
              minZoom={5} 
              maxBounds={MAURITANIA_BOUNDS}
              whenCreated={(map) => {
                mapRef.current = map;
                setZoomLevel(map.getZoom());
                map.on('zoomend', () => setZoomLevel(map.getZoom()));
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
            </Modal.Title>
          </Modal.Header>
          <Modal.Body style={{ maxHeight: '70vh', overflowY: 'auto' }}>
            <table className="table table-sm table-striped">
              <tbody>
                {Object.entries(selectedData).filter(([key]) => 
                  !["commune", "region", "department", "country", "id", "census", "zoneType", "zoneId"].includes(key)
                ).map(([key, value]) => (
                  <tr key={key}>
                    <td><strong>{key}</strong></td>
                    <td>{String(value)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
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
    </div>
  );
};

export default MapComponent;