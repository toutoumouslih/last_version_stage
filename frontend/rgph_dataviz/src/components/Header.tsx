// src/components/Header.tsx
import React from 'react';
import './Header.css';
// import logo from '../assets/logo.png'; 

const Header: React.FC = () => {
  return (
    <header className="custom-header">
      <div className="header-left">
        {/* <img src={logo} alt="Logo" className="header-logo" /> */}
        <div className="header-text">
          <span className="arabe">الجمهورية الإسلامية الموريتانية</span>
          <span className="fr">HAUT-COMMISSARIAT AU PLAN</span>
        </div>
      </div>
      <nav className="header-nav">
        <a href="/">Cartes thématiques</a>
        <a href="/chiffres-cles-2023">Chiffres clés 2024</a>
        <a href="#tableaux">Tableaux RGPH 2024</a>
        <a href="#cee">CEE 2024</a>
        <a href="/ConceptsDefinitions">Concepts et définitions</a>
      </nav>
    </header>
  );
};

export default Header;
