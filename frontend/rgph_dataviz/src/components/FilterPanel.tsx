import React from 'react';
import { Accordion, Badge, Button } from 'react-bootstrap';
import { FilterCategory, FilterOption, GeoLevelFilterOption, Region, Departement, Commune } from '../types/types';
import { GEO_LEVEL_FILTERS } from './filtersConfig';
import Fuse from 'fuse.js';

interface FilterPanelProps {
  categories: FilterCategory[];
  activeFilter: FilterOption | null;
  onFilterSelect: (filter: FilterOption) => void;
  onClearFilter: () => void;
  onTogglePanel: () => void;
  showFilters: boolean;
  activeGeoLevel: 'region' | 'department' | 'commune';
  onGeoLevelSelect: (level: 'region' | 'department' | 'commune') => void;
  regions: Region[];
  departements: Departement[];
  communes: Commune[];
  onZoneSearchSelect: (zoneId: number, level: 'region' | 'department' | 'commune') => void;
}

const formatValue = (value: any, type: 'number' | 'percentage') => {
  if (value === null || value === undefined) return 'N/A';
  if (type === 'percentage') return `${parseFloat(value).toFixed(1)}%`;
  return new Intl.NumberFormat('fr-FR').format(value);
};

export const FilterPanel: React.FC<FilterPanelProps> = ({
  categories,
  activeFilter,
  onFilterSelect,
  onClearFilter,
  onTogglePanel,
  showFilters,
  activeGeoLevel,
  onGeoLevelSelect,
  regions,
  departements,
  communes,
  onZoneSearchSelect
}) => {
  if (!showFilters) return null;

  const [search, setSearch] = React.useState('');
  const [searchResults, setSearchResults] = React.useState<any[]>([]);
  const [highlightedIdx, setHighlightedIdx] = React.useState(0);

  // Prépare les données pour la recherche
  const allZones = [
    ...((regions || []).map(r => ({ id: r.id, name: r.adm1_en, level: 'region', parent: '', full: r }))),
    ...((departements || []).map(d => ({ id: d.id, name: d.adm2_en, level: 'department', parent: (regions || []).find(r => r.id === (d as any).region)?.adm1_en || '', full: d }))),
    ...((communes || []).map(c => ({ id: c.id, name: c.adm3_en, level: 'commune', parent: (departements || []).find(d => d.id === (c as any).department)?.adm2_en || '', full: c }))),
  ];
  const fuse = React.useMemo(() => new Fuse(allZones, { keys: ['name'], threshold: 0.3 }), [regions, departements, communes]);

  React.useEffect(() => {
    if (search.trim().length > 0) {
      setSearchResults(fuse.search(search).map(r => r.item));
      setHighlightedIdx(0);
    } else {
      setSearchResults([]);
    }
  }, [search, fuse]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (searchResults.length === 0) return;
    if (e.key === 'ArrowDown') {
      setHighlightedIdx(idx => Math.min(idx + 1, searchResults.length - 1));
    } else if (e.key === 'ArrowUp') {
      setHighlightedIdx(idx => Math.max(idx - 1, 0));
    } else if (e.key === 'Enter') {
      const zone = searchResults[highlightedIdx];
      if (zone) {
        onZoneSearchSelect(zone.id, zone.level);
        setSearch('');
        setSearchResults([]);
      }
    }
  };

  return (
    <div style={{ 
      width: '300px', 
      overflowY: 'auto', 
      padding: '15px', 
      backgroundColor: '#f8f9fa', 
      borderRight: '1px solid #dee2e6' 
    }}>
      <h4 style={{ 
        marginBottom: '20px', 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center' 
      }}>
        <span>Filtres</span>
        <Button variant="link" size="sm" onClick={onTogglePanel}>
          <i className="bi bi-chevron-left"></i>
        </Button>
      </h4>

      <div style={{ marginBottom: '16px' }}>
        <input
          type="text"
          className="form-control"
          placeholder="Rechercher une zone..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        {searchResults.length > 0 && (
          <div style={{ background: '#fff', border: '1px solid #ccc', borderRadius: 4, marginTop: 2, maxHeight: 200, overflowY: 'auto', zIndex: 1000, position: 'absolute', width: '90%' }}>
            {searchResults.map((zone, idx) => (
              <div
                key={zone.level + '-' + zone.id}
                style={{
                  padding: '8px 12px',
                  background: idx === highlightedIdx ? '#eaf1fa' : 'transparent',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  borderBottom: '1px solid #f1f1f1',
                }}
                onMouseEnter={() => setHighlightedIdx(idx)}
                onMouseDown={() => {
                  onZoneSearchSelect(zone.id, zone.level);
                  setSearch('');
                  setSearchResults([]);
                }}
              >
                <span style={{ fontWeight: 600 }}>{zone.name}</span>
                <span style={{ marginLeft: 8, fontSize: 12, color: '#366092', fontWeight: 500, border: '1px solid #366092', borderRadius: 4, padding: '2px 6px' }}>{zone.level === 'region' ? 'Région' : zone.level === 'department' ? 'Moughataa' : 'Commune'}</span>
                {zone.parent && <span style={{ marginLeft: 8, fontSize: 12, color: '#888' }}>({zone.parent})</span>}
              </div>
            ))}
          </div>
        )}
      </div>

      <div style={{ marginBottom: '20px', padding: '10px', backgroundColor: '#fff', borderRadius: '5px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
        <h5 style={{ marginBottom: '10px', fontSize: '16px' }}>Niveau Géographique</h5>
        <div style={{ display: 'flex', gap: '8px' }}>
          {GEO_LEVEL_FILTERS.map(option => (
            <Button
              key={option.id}
              variant={activeGeoLevel === option.level ? 'primary' : 'outline-secondary'}
              size="sm"
              onClick={() => onGeoLevelSelect(option.level)}
              style={{ flex: 1 }}
            >
              {option.label}
            </Button>
          ))}
        </div>
      </div>
      
      <Accordion defaultActiveKey={['population', 'gender']} alwaysOpen>
        {categories.map(category => (
          <Accordion.Item key={category.id} eventKey={category.id}>
            <Accordion.Header>{category.title}</Accordion.Header>
            <Accordion.Body>
              {category.options.map(option => (
                <div 
                  key={option.id}
                  onClick={() => onFilterSelect(option)}
                  style={{
                    padding: '8px',
                    marginBottom: '5px',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    backgroundColor: activeFilter?.id === option.id ? '#e9ecef' : 'transparent',
                    transition: 'background-color 0.2s'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>{option.label}</span>
                    {activeFilter?.id === option.id && <Badge bg="primary">✓</Badge>}
                  </div>
                </div>
              ))}
            </Accordion.Body>
          </Accordion.Item>
        ))}
      </Accordion>
      
      {activeFilter && (
        <div style={{ 
          marginTop: '20px', 
          padding: '10px', 
          backgroundColor: '#e9ecef', 
          borderRadius: '4px' 
        }}>
          <h6>Filtre actif:</h6>
          <div><strong>{activeFilter.label}</strong></div>
          <div style={{ marginTop: '10px' }}>
            {activeFilter.ranges.map((r, i) => (
              <div key={i} style={{ 
                display: 'flex', 
                alignItems: 'center', 
                marginBottom: '3px' 
              }}>
                <div style={{
                  width: '15px',
                  height: '15px',
                  backgroundColor: activeFilter.colorScale[i],
                  marginRight: '8px',
                  borderRadius: '3px'
                }}></div>
                <div>{formatValue(r, activeFilter.type)}</div>
              </div>
            ))}
          </div>
          <Button 
            variant="outline-danger" 
            size="sm" 
            style={{ marginTop: '10px' }}
            onClick={onClearFilter}
          >
            Supprimer le filtre
          </Button>
        </div>
      )}
    </div>
  );
};