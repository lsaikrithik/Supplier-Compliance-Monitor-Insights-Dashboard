// src/components/ComplianceUpload.js
import React, { useState } from 'react';
import axios from 'axios';
import '../App.css'; // Import CSS for styling

function ComplianceUpload() {
  const [formData, setFormData] = useState({
    supplier_id: '',
    metric: '',
    result: '',
    status: '',
    date_recorded: '',
  });

  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setMessage('');
    setError('');
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Validate form data
    if (
      !formData.supplier_id ||
      !formData.metric ||
      !formData.result ||
      !formData.status ||
      !formData.date_recorded
    ) {
      setError('⚠️ Please fill in all fields.');
      return;
    }

    // Prepare data for API request
    const requestData = {
      supplier_id: parseInt(formData.supplier_id),
      metric: formData.metric,
      result: formData.result,
      status: formData.status,
      date_recorded: formData.date_recorded,
    };

    // Make API request to backend
    axios
      .post(`${process.env.REACT_APP_BACKEND_URL}/suppliers/check-compliance`, requestData)
      .then((res) => {
        setMessage('✅ Compliance data uploaded successfully.');
        setFormData({
          supplier_id: '',
          metric: '',
          result: '',
          status: '',
          date_recorded: '',
        });
      })
      .catch((err) => {
        console.error(err);
        setError('❌ An error occurred while uploading compliance data.');
      });
  };

  return (
    <div className="upload-container">
      <h1 className="upload-title">📤 Upload Compliance Data</h1>
      <form className="upload-form" onSubmit={handleSubmit}>
        <input
          type="number"
          name="supplier_id"
          placeholder="Supplier ID"
          value={formData.supplier_id}
          onChange={handleChange}
          className="upload-input"
          required
        />
        <input
          name="metric"
          placeholder="Metric"
          value={formData.metric}
          onChange={handleChange}
          className="upload-input"
          required
        />
        <input
          name="result"
          placeholder="Result"
          value={formData.result}
          onChange={handleChange}
          className="upload-input"
          required
        />
        <input
          name="status"
          placeholder="Status"
          value={formData.status}
          onChange={handleChange}
          className="upload-input"
          required
        />
        <label className="date-label">📅 Date Recorded:</label>
        <input
          type="date"
          name="date_recorded"
          value={formData.date_recorded}
          onChange={handleChange}
          className="upload-input"
          required
        />
        <button type="submit" className="upload-button">Upload</button>
      </form>
      
      {message && <p className="success-message">{message}</p>}
      {error && <p className="error-message">{error}</p>}
    </div>
  );
}

export default ComplianceUpload;
