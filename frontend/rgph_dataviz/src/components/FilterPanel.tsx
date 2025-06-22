import React from 'react';
import { Accordion, Badge, Button } from 'react-bootstrap';
import { FilterCategory, FilterOption, GeoLevelFilterOption } from '../types/types';
import { GEO_LEVEL_FILTERS } from './filtersConfig';

interface FilterPanelProps {
  categories: FilterCategory[];
  activeFilter: FilterOption | null;
  onFilterSelect: (filter: FilterOption) => void;
  onClearFilter: () => void;
  onTogglePanel: () => void;
  showFilters: boolean;
  activeGeoLevel: 'region' | 'department' | 'commune';
  onGeoLevelSelect: (level: 'region' | 'department' | 'commune') => void;
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
  onGeoLevelSelect
}) => {
  if (!showFilters) return null;

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