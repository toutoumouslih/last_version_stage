import React from 'react';
import { Routes, Route } from 'react-router-dom';
import './App.css';
import MapComponent from './components/MapComponent';
import Header from './components/Header';
import KeyStatsPage from './pages/ChiffresCles2023';
import ConceptsDefinitions from './pages/ConceptsDefinitiions'

function App() {
  return (
    <div className="App">
      <Header />
      <Routes>
        <Route path="/" element={<MapComponent />} />
        <Route path="/chiffres-cles-2023" element={<KeyStatsPage />} />
        <Route path="/ConceptsDefinitions" element={<ConceptsDefinitions/>} />
      </Routes>
    </div>
  );
}

export default App;