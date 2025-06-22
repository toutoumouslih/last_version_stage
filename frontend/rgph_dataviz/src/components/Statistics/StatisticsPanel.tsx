import React from 'react';
import { Box, Paper, Typography, Grid, useTheme } from '@mui/material';
import { Region, Department, Commune, DemographicData } from '../../services/api';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

interface StatisticsPanelProps {
  area: Region | Department | Commune;
  type: 'region' | 'department' | 'commune';
  demographicData: DemographicData;
}

const StatisticsPanel: React.FC<StatisticsPanelProps> = ({ area, type, demographicData }) => {
  const theme = useTheme();

  // Données pour le graphique de répartition par sexe
  const genderData = [
    { name: 'Hommes', value: demographicData.male_percentage },
    { name: 'Femmes', value: demographicData.female_percentage }
  ];

  // Données pour le graphique de l'état matrimonial
  const maritalStatusData = [
    { name: 'Célibataires', value: demographicData.single_rate },
    { name: 'Mariés', value: demographicData.married_rate },
    { name: 'Divorcés', value: demographicData.divorced_rate },
    { name: 'Veufs', value: demographicData.widowed_rate }
  ];

  // Couleurs pour les graphiques
  const COLORS = [
    theme.palette.primary.main,
    theme.palette.secondary.main,
    theme.palette.error.main,
    theme.palette.warning.main
  ];

  return (
    <Paper
      elevation={3}
      sx={{
        position: 'absolute',
        top: 20,
        right: 20,
        width: 400,
        maxHeight: '80vh',
        overflow: 'auto',
        p: 2,
        backgroundColor: 'rgba(255, 255, 255, 0.9)'
      }}
    >
      <Typography variant="h5" gutterBottom>
        {area.name}
      </Typography>
      <Typography variant="subtitle1" color="textSecondary" gutterBottom>
        {type === 'region' ? 'Région' : type === 'department' ? 'Département' : 'Commune'}
      </Typography>

      <Grid container spacing={2}>
        {/* Population totale */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2, textAlign: 'center' }}>
            <Typography variant="h6">Population Totale</Typography>
            <Typography variant="h4" color="primary">
              {demographicData.total_population.toLocaleString()}
            </Typography>
          </Paper>
        </Grid>

        {/* Répartition par sexe */}
        <Grid item xs={12}>
          <Typography variant="h6" gutterBottom>
            Répartition par Sexe
          </Typography>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={genderData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(1)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {genderData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </Grid>

        {/* État matrimonial */}
        <Grid item xs={12}>
          <Typography variant="h6" gutterBottom>
            État Matrimonial
          </Typography>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={maritalStatusData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" fill={theme.palette.primary.main} />
            </BarChart>
          </ResponsiveContainer>
        </Grid>

        {/* Autres statistiques */}
        <Grid item xs={12}>
          <Typography variant="h6" gutterBottom>
            Autres Statistiques
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <Typography variant="body2">
                Population 10+ ans: {demographicData.population_10_plus.toLocaleString()}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography variant="body2">
                Population 15+ ans: {demographicData.population_15_plus.toLocaleString()}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography variant="body2">
                Taux de scolarisation: {demographicData.school_enrollment_rate.toFixed(1)}%
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography variant="body2">
                Taux d'analphabétisme (10+): {demographicData.illiteracy_rate_10_plus.toFixed(1)}%
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography variant="body2">
                Taux d'analphabétisme (15+): {demographicData.illiteracy_rate_15_plus.toFixed(1)}%
              </Typography>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default StatisticsPanel; 