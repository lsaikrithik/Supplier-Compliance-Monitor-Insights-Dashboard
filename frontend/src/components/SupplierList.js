// src/components/SupplierList.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { FaIndustry } from 'react-icons/fa';
import '../App.css'; // Import the CSS file

function SupplierList() {
  const [suppliers, setSuppliers] = useState([]);

  useEffect(() => {
    axios
      .get('http://localhost:8000/suppliers')
      .then((res) => setSuppliers(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="supplier-list-container">
      <h1 className="supplier-list-title">📋 Supplier List</h1>

      {suppliers.length === 0 ? (
        <p className="no-suppliers">No suppliers found.</p>
      ) : (
        <div className="supplier-grid">
          {suppliers.map((supplier) => (
            <Link
              key={supplier.supplier_id}
              to={`/suppliers/${supplier.supplier_id}`}
              className="supplier-card"
            >
              <div className="icon-container">
                <FaIndustry className="supplier-icon" />
              </div>
              <div className="supplier-info">
                <h2 className="supplier-name">{supplier.name}</h2>
                <p className="supplier-score">
                  Compliance Score:{' '}
                  <span className="score-value">{supplier.compliance_score}</span>
                </p>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

export default SupplierList;
