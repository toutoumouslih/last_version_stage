import React, { useState, useEffect } from 'react';
import { Card, Row, Col, ProgressBar, Button, Modal, Form, Spinner } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
  faUsers, 
  faVenusMars, 
  faGraduationCap,
  faBriefcase
} from '@fortawesome/free-solid-svg-icons';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface KeyStat {
  id: string;
  title: string;
  value: string;
  icon: any;
  description?: string;
  progress?: number;
}

interface Demographic {
  id: number;
  total_population: number;
  male_percentage: string;
  female_percentage: string;
  school_enrollment_rate: string;
  illiteracy_rate_15_plus: string;
  region?: number;
  department?: number;
  commune?: number;
}

interface Region {
  id: number;
  adm1_en: string;
}

const KeyStatsPage: React.FC = () => {
  const [showModal, setShowModal] = useState(false);
  const [selectedStat, setSelectedStat] = useState<KeyStat | null>(null);
  const [demographics, setDemographics] = useState<Demographic[]>([]);
  const [regions, setRegions] = useState<Region[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedRegion, setSelectedRegion] = useState<string>('all');
  const [chartData, setChartData] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [demoResponse, regionsResponse] = await Promise.all([
          fetch('http://127.0.0.1:8000/api/api/demographics/'),
          fetch('http://127.0.0.1:8000/api/api/regions/')
        ]);
        
        const demoData = await demoResponse.json();
        const regionsData = await regionsResponse.json();
        
        setDemographics(demoData);
        setRegions(regionsData);
        prepareChartData(demoData);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching data:", error);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const prepareChartData = (data: Demographic[]) => {
    const regionEntries = data.filter(d => d.department === null && d.commune === null);
    
    const chartData = regionEntries.map(entry => {
      const regionName = regions.find(r => r.id === entry.region)?.adm1_en || `Region ${entry.region}`;
      return {
        name: regionName,
        population: entry.total_population,
        male: parseFloat(entry.male_percentage),
        female: parseFloat(entry.female_percentage),
        illiteracy: parseFloat(entry.illiteracy_rate_15_plus)
      };
    });
    
    setChartData(chartData);
  };

  const getRegionPopulation = (regionId: number) => {
    const regionData = demographics.find(d => 
      d.region === regionId && d.department === null && d.commune === null
    );
    return regionData ? regionData.total_population : 0;
  };

  const getNationalPopulation = () => {
    return demographics
      .filter(d => d.department === null && d.commune === null)
      .reduce((sum, item) => sum + item.total_population, 0);
  };

  const getAggregatedValue = (field: keyof Demographic, isPercentage = true): number => {
    const regionData = selectedRegion === 'all'
      ? demographics.filter(d => d.department === null && d.commune === null)
      : demographics.filter(d => d.region === parseInt(selectedRegion) && d.department === null && d.commune === null);
    
    if (regionData.length === 0) return 0;
    
    const sum = regionData.reduce((total, item) => {
      const value = parseFloat(item[field] as string) || 0;
      return total + value;
    }, 0);
    
    const average = sum / regionData.length;
    return isPercentage ? average : Math.round(average);
  };

  const keyStats: KeyStat[] = [
    {
      id: 'population',
      title: "Population totale",
      value: selectedRegion === 'all' 
        ? getNationalPopulation().toLocaleString() 
        : getRegionPopulation(parseInt(selectedRegion)).toLocaleString(),
      icon: faUsers,
      description: "Population totale de la zone sélectionnée"
    },
    {
      id: 'gender',
      title: "Ratio hommes/femmes",
      value: `${getAggregatedValue('male_percentage').toFixed(1)}% hommes / ${getAggregatedValue('female_percentage').toFixed(1)}% femmes`,
      icon: faVenusMars,
      description: "Répartition par sexe de la population"
    },
    {
      id: 'education',
      title: "Taux de scolarisation",
      value: `${getAggregatedValue('school_enrollment_rate').toFixed(1)}%`,
      icon: faGraduationCap,
      progress: getAggregatedValue('school_enrollment_rate'),
      description: "Taux de scolarisation des enfants en âge d'être scolarisés"
    },
    {
      id: 'illiteracy',
      title: "Taux d'analphabétisme",
      value: `${getAggregatedValue('illiteracy_rate_15_plus').toFixed(1)}%`,
      icon: faBriefcase,
      progress: getAggregatedValue('illiteracy_rate_15_plus'),
      description: "Taux d'analphabétisme chez les personnes de 15 ans et plus"
    }
  ];

  const handleCardClick = (stat: KeyStat) => {
    setSelectedStat(stat);
    setShowModal(true);
  };

  const handleRegionChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedRegion(e.target.value);
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: '100vh' }}>
        <Spinner animation="border" variant="primary" />
      </div>
    );
  }

  return (
    <div className="container-fluid p-0" style={{ backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
      <div className="bg-white shadow-sm p-3">
        <div className="d-flex justify-content-between align-items-center">
          <h4 className="mb-0">Chiffres clés Mauritanie 2024</h4>
          <Button 
            variant="outline-secondary"
            size="sm"
            onClick={() => window.location.href = '/'}
          >
            Voir la carte
          </Button>
        </div>
      </div>

      <div className="p-3 bg-light border-bottom">
        <div className="d-flex align-items-center">
          <span className="me-2 fw-bold">Filtres:</span>
          <Form.Select 
            className="me-2" 
            style={{ width: '200px' }}
            value={selectedRegion}
            onChange={handleRegionChange}
          >
            <option value="all">Toutes les régions</option>
            {regions.map(region => (
              <option key={region.id} value={region.id}>
                {region.adm1_en}
              </option>
            ))}
          </Form.Select>
        </div>
      </div>

      <div className="p-3">
        <Row className="g-3 mb-4">
          {keyStats.map((stat) => (
            <Col key={stat.id} xs={12} sm={6} md={4} lg={3}>
              <Card 
                className="h-100 border-0 shadow-sm" 
                onClick={() => handleCardClick(stat)}
                style={{ cursor: 'pointer' }}
              >
                <Card.Body className="text-center">
                  <FontAwesomeIcon 
                    icon={stat.icon} 
                    size="2x" 
                    className="text-primary mb-2" 
                  />
                  <h6 className="card-title text-muted">{stat.title}</h6>
                  <h4 className="text-dark fw-bold">{stat.value}</h4>
                  
                  {stat.progress !== undefined && (
                    <div className="mt-2">
                      <ProgressBar 
                        now={stat.progress} 
                        variant={stat.id === 'illiteracy' ? 'danger' : 'success'}
                        className="mb-1" 
                        label={`${stat.progress.toFixed(1)}%`}
                      />
                      <small className="text-muted">Cliquez pour plus de détails</small>
                    </div>
                  )}
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>

        <Row className="mb-4">
          <Col md={12} className="mb-3">
            <Card className="border-0 shadow-sm h-100">
              <Card.Header className="bg-white border-bottom">
                <h5 className="mb-0">Statistiques par région</h5>
              </Card.Header>
              <Card.Body>
                <div style={{ height: '400px' }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={chartData}
                      margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis 
                        dataKey="name" 
                        angle={-45} 
                        textAnchor="end"
                        height={70}
                      />
                      <YAxis yAxisId="left" orientation="left" />
                      <YAxis yAxisId="right" orientation="right" />
                      <Tooltip 
                        formatter={(value, name) => {
                          if (name === 'Population') {
                            return [value.toLocaleString(), name];
                          }
                          return [`${value}%`, name];
                        }}
                      />
                      <Legend />
                      <Bar 
                        yAxisId="left"
                        dataKey="population" 
                        name="Population" 
                        fill="#8884d8" 
                      />
                      <Bar 
                        yAxisId="right"
                        dataKey="illiteracy" 
                        name="Taux d'analphabétisme (%)" 
                        fill="#ff8042" 
                      />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </Card.Body>
            </Card>
          </Col>
        </Row>

        <Modal show={showModal} onHide={() => setShowModal(false)}>
          <Modal.Header closeButton>
            <Modal.Title>{selectedStat?.title}</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <p>{selectedStat?.description}</p>
            <p className="fw-bold">Valeur: {selectedStat?.value}</p>
            {selectedStat?.progress !== undefined && (
              <div className="mt-3">
                <h6>Détails:</h6>
                <ProgressBar 
                  now={selectedStat.progress} 
                  variant={selectedStat.id === 'illiteracy' ? 'danger' : 'success'}
                  label={`${selectedStat.progress.toFixed(1)}%`}
                />
              </div>
            )}
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowModal(false)}>
              Fermer
            </Button>
          </Modal.Footer>
        </Modal>
      </div>
    </div>
  );
};

export default KeyStatsPage;