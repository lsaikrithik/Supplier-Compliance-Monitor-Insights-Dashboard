// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import SupplierList from './components/SupplierList';
import SupplierDetail from './components/SupplierDetail';
import ComplianceUpload from './components/ComplianceUpload';
import WeatherImpact from './components/WeatherImpact';
import './App.css'; // Import CSS

function App() {
  return (
    <Router>
      <div className="app-container">
        {/* Navigation Bar with Stylish Buttons */}
        <nav className="nav-container">
          <Link to="/" className="nav-button">📋 Suppliers</Link>
          <Link to="/upload" className="nav-button">📤 Upload Compliance Data</Link>
          <Link to="/weather-impact" className="nav-button">⛅ Weather Impact</Link>
        </nav>

        {/* Routing */}
        <Routes>
          <Route path="/" element={<SupplierList />} />
          <Route path="/suppliers/:supplier_id" element={<SupplierDetail />} />
          <Route path="/upload" element={<ComplianceUpload />} />
          <Route path="/weather-impact" element={<WeatherImpact />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
