import React, { useState, useRef } from 'react';
import L from 'leaflet';
import { useMap } from 'react-leaflet';
import { useDispatch } from 'react-redux';
import { setMap } from '../redux/mapSlice';
import { useSelector } from 'react-redux';
import { selectMap } from '../redux/mapSlice';
import { useEffect } from 'react';

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
  const mapRef = useRef<L.Map | null>(null);

  const dispatch = useDispatch();
  const map = useMap();

  useEffect(() => {
    if (map) {
      dispatch(setMap(map));
    }
  }, [map, dispatch]);

  return (
    <div>
      {/* Rest of the component code */}
    </div>
  );
};

export default MapComponent; 