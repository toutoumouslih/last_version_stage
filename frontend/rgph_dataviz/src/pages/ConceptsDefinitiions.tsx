import React from 'react';
import './ConceptsDefinitions.css';

const concepts = [
  {
    title: 'Recensement Général de la Population (RGP)',
    description: `Le Recensement Général de la Population (RGP) est une opération statistique réalisée à intervalles réguliers pour collecter des informations sur la population d'un pays. Il permet de dresser un portrait précis de la population, en termes de nombre, de répartition géographique, de structure par âge, sexe, état civil, et d'autres caractéristiques démographiques et sociales.`,
  },
  {
    title: 'GeoJSON',
    description: `Le GeoJSON est un format standardisé pour représenter des objets géographiques au sein de données. Ce format permet de structurer des informations géospatiales, telles que des points, des lignes ou des polygones. Sur ce site, les GeoJSON sont utilisés pour représenter les différentes régions administratives de la Mauritanie.`,
  },
  {
    title: 'Région Administrative',
    description: `Une région administrative est une division géographique et administrative d'un pays. En Mauritanie, il existe plusieurs niveaux de subdivisions administratives, tels que les régions, départements, et communes. Chaque niveau a ses propres caractéristiques démographiques et géographiques.`,
  },
  {
    title: 'Département Administratif',
    description: `Le département administratif est une unité administrative située sous le niveau de la région. Chaque département est constitué de plusieurs communes, qui représentent les plus petites subdivisions administratives dans le pays.`,
  },
  // Ajoutez d'autres concepts ici...
];

const ConceptsDefinitions: React.FC = () => {
  return (
    <div className="concepts-definitions-container">
      <h1 className="page-title">Concepts et Définitions</h1>
      <div className="concepts-list">
        {concepts.map((concept, index) => (
          <div key={index} className="concept-item">
            <h2 className="concept-title">{concept.title}</h2>
            <p className="concept-description">{concept.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ConceptsDefinitions;
