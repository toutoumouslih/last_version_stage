import React, { useEffect, useRef, useState } from 'react';
import './ConceptsDefinitions.css';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const ANSADE_LOCATION = { lat: 18.0735, lng: -15.9582 };

const MapAnsade = () => (
  <MapContainer
    center={[ANSADE_LOCATION.lat, ANSADE_LOCATION.lng]}
    zoom={15}
    style={{ width: '100%', height: 220, borderRadius: 12, margin: '16px 0', boxShadow: '0 2px 12px #0001' }}
    scrollWheelZoom={false}
  >
    <TileLayer
      attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    />
    <Marker position={[ANSADE_LOCATION.lat, ANSADE_LOCATION.lng]}>
      <Popup>ANSADE, Nouakchott</Popup>
    </Marker>
  </MapContainer>
);

// Compteur animé
const AnimatedNumber: React.FC<{ value: number }> = ({ value }) => {
  const [display, setDisplay] = useState(0);
  const ref = useRef<number>(0);
  useEffect(() => {
    let start = ref.current;
    const duration = 1200;
    const startTime = performance.now();
    const animate = (now: number) => {
      const progress = Math.min((now - startTime) / duration, 1);
      setDisplay(Math.floor(start + (value - start) * progress));
      if (progress < 1) requestAnimationFrame(animate);
      else ref.current = value;
    };
    requestAnimationFrame(animate);
  }, [value]);
  return <span style={{ fontWeight: 700, fontSize: 32, color: '#366092', letterSpacing: 1 }}>{display.toLocaleString('fr-FR')}</span>;
};

const concepts = [
  {
    icon: '📊',
    title: 'Recensement Général de la Population (RGP)',
    description: `Le Recensement Général de la Population (RGP) est une opération statistique réalisée à intervalles réguliers pour collecter des informations sur la population d'un pays. Il permet de dresser un portrait précis de la population, en termes de nombre, de répartition géographique, de structure par âge, sexe, état civil, et d'autres caractéristiques démographiques et sociales.`,
  },
  {
    icon: '🗺️',
    title: 'GeoJSON',
    description: `Le GeoJSON est un format standardisé pour représenter des objets géographiques au sein de données. Ce format permet de structurer des informations géospatiales, telles que des points, des lignes ou des polygones. Sur ce site, les GeoJSON sont utilisés pour représenter les différentes régions administratives de la Mauritanie.`,
  },
  {
    icon: '🏛️',
    title: 'Région Administrative',
    description: `Une région administrative est une division géographique et administrative d'un pays. En Mauritanie, il existe plusieurs niveaux de subdivisions administratives, tels que les régions, départements, et communes. Chaque niveau a ses propres caractéristiques démographiques et géographiques.`,
  },
  {
    icon: '🏢',
    title: 'Département Administratif',
    description: `Le département administratif est une unité administrative située sous le niveau de la région. Chaque département est constitué de plusieurs communes, qui représentent les plus petites subdivisions administratives dans le pays.`,
  },
  {
    icon: '📍',
    title: "Agence Nationale de la Statistique (ANSADE)",
    description: "L'ANSADE est l'organisme officiel chargé de la collecte, l'analyse et la diffusion des statistiques en Mauritanie. Localisation à Nouakchott :",
    map: true
  },
  {
    icon: '📌',
    title: 'Site (dans ce projet)',
    description: `Un "site" désigne ici une unité géographique d'analyse, qui peut correspondre à une région, un département ou une commune. Chaque site regroupe des données démographiques, sociales et éducatives, et sert de base à la visualisation cartographique et statistique du projet.`,
    badge: 'Concept clé'
  },
];

const ressources = [
  { label: 'Documentation officielle GeoJSON', url: 'https://geojson.org/' },
  { label: 'Site officiel ANSADE', url: 'https://www.ansade.mr/' },
  { label: 'OpenStreetMap', url: 'https://www.openstreetmap.org/' },
];

const ConceptsDefinitions: React.FC = () => {
  const [populationTotale, setPopulationTotale] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/api/demographics/?year=2023')
      .then(res => res.json())
      .then(data => {
        const total = data
          .filter((d: any) => d.commune)
          .reduce((sum: number, d: any) => sum + (d.total_population || 0), 0);
        setPopulationTotale(total);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(120deg, #f8fafc 0%, #eaf1fa 100%)',
      padding: '0 0 40px 0',
    }}>
      <div style={{ maxWidth: 900, margin: '0 auto', padding: '32px 16px 0 16px' }}>
        <h1 className="page-title" style={{ color: '#366092', fontWeight: 800, fontSize: 38, marginBottom: 8, letterSpacing: 1 }}>Concepts et Définitions</h1>
        <div style={{ marginBottom: 32, background: '#fff', borderRadius: 16, boxShadow: '0 2px 16px #0001', padding: 24, display: 'flex', alignItems: 'center', gap: 32, flexWrap: 'wrap', transition: 'box-shadow 0.2s' }}>
          <div style={{ flex: 1 }}>
            <h2 style={{ color: '#366092', fontWeight: 700, fontSize: 24, marginBottom: 8 }}>À propos du projet</h2>
            <p style={{ fontSize: 17, color: '#333', marginBottom: 12 }}>
              Ce site propose une visualisation interactive et des analyses avancées des données démographiques, sociales et éducatives de la Mauritanie, issues du dernier recensement général de la population.
            </p>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <span style={{ fontSize: 22, color: '#366092', fontWeight: 600 }}>Population totale selon l'année 2023 :</span>
              {loading ? <span style={{ color: '#aaa', fontSize: 28 }}>...</span> : <AnimatedNumber value={populationTotale} />}
            </div>
          </div>
          <img src="https://cdn-icons-png.flaticon.com/512/684/684908.png" alt="Mauritanie" style={{ width: 120, borderRadius: 12, boxShadow: '0 2px 8px #0001' }} />
        </div>
        <div className="concepts-list" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: 28 }}>
          {concepts.map((concept, index) => (
            <div
              key={index}
              className="concept-item"
              style={{
                background: '#fff',
                borderRadius: 16,
                boxShadow: '0 2px 12px #0001',
                padding: 24,
                position: 'relative',
                transition: 'transform 0.18s, box-shadow 0.18s',
                cursor: 'default',
                minHeight: 220,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'flex-start',
                alignItems: 'flex-start',
                gap: 10,
                border: '1px solid #eaf1fa',
              }}
              onMouseEnter={e => (e.currentTarget.style.transform = 'translateY(-4px) scale(1.025)', e.currentTarget.style.boxShadow = '0 6px 24px #36609222')}
              onMouseLeave={e => (e.currentTarget.style.transform = '', e.currentTarget.style.boxShadow = '0 2px 12px #0001')}
            >
              <span style={{ fontSize: 36, marginBottom: 4 }}>{concept.icon}</span>
              <h2 className="concept-title" style={{ color: '#366092', fontWeight: 700, fontSize: 22, margin: 0 }}>{concept.title}</h2>
              <p className="concept-description" style={{ color: '#444', fontSize: 16, margin: 0 }}>{concept.description}</p>
              {concept.badge && <span style={{ background: '#eaf1fa', color: '#366092', fontWeight: 600, borderRadius: 8, padding: '3px 10px', fontSize: 13, marginTop: 6 }}>{concept.badge}</span>}
              {concept.map && <MapAnsade />}
            </div>
          ))}
        </div>
        <div style={{ marginTop: 48, background: '#fff', borderRadius: 16, boxShadow: '0 2px 12px #0001', padding: 24 }}>
          <h2 style={{ color: '#366092', fontWeight: 700, fontSize: 22, marginBottom: 12 }}>Ressources utiles</h2>
          <ul style={{ paddingLeft: 20, fontSize: 16, color: '#366092' }}>
            {ressources.map((r, i) => (
              <li key={i} style={{ marginBottom: 6 }}>
                <a href={r.url} target="_blank" rel="noopener noreferrer" style={{ color: '#366092', textDecoration: 'underline', fontWeight: 500 }}>{r.label}</a>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ConceptsDefinitions;
