import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import '../App.css';  // Ensure the path is correct

function SupplierDetail() {
  const { supplier_id } = useParams();
  const [supplier, setSupplier] = useState(undefined);
  const [insights, setInsights] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch supplier details
    axios.get(`http://localhost:8000/suppliers/${parseInt(supplier_id)}`)
      .then(res => setSupplier(res.data))
      .catch(err => {
        console.error(err);
        setError('Supplier not found.');
      });

    // Fetch insights specific to this supplier (if endpoint supports it)
    axios.get(`http://localhost:8000/suppliers/insights/${parseInt(supplier_id)}`)
      .then(res => setInsights(res.data.insights))
      .catch(err => {
        console.error(err);
        setInsights('Failed to fetch insights.');
      });
  }, [supplier_id]);

  if (error) return <p className="error-message">{error}</p>;
  if (supplier === undefined) return <p className="loading-message">Loading...</p>;

  return (
    <div className="supplier-detail-container">
      <div className="supplier-header">
        <h1>{supplier.name}</h1>
        <p className="supplier-info">Country: <span>{supplier.country}</span></p>
        <p className="supplier-info">Compliance Score: <span>{supplier.compliance_score}</span></p>
        <p className="supplier-info">Last Audit: <span>{supplier.last_audit}</span></p>
      </div>
      
      <div className="card">
        <h2>Contract Terms</h2>
        <pre className="contract-terms">{JSON.stringify(supplier.contract_terms, null, 2)}</pre>
      </div>
      
      <div className="card">
        <h2>Compliance Insights</h2>
        {insights ? (
          <div className="markdown-body">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {insights}
            </ReactMarkdown>
          </div>
        ) : (
          <p>No insights available.</p>
        )}
      </div>
    </div>
  );
}

export default SupplierDetail;
