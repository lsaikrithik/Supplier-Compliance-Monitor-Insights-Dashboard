// src/components/WeatherImpact.js
import React, { useState } from 'react';
import axios from 'axios';
import './WeatherImpact.css';

function WeatherImpact() {
  const [formData, setFormData] = useState({
    supplier_id: '',
    latitude: '',
    longitude: '',
    delivery_date: '',
  });

  const [responseMessage, setResponseMessage] = useState('');
  const [conditions, setConditions] = useState([]);
  const [error, setError] = useState('');

  const handleChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setResponseMessage('');
    setError('');
  };

  const handleSubmit = e => {
    e.preventDefault();

    // Validate form data
    if (
      !formData.supplier_id ||
      !formData.latitude ||
      !formData.longitude ||
      !formData.delivery_date
    ) {
      setError('Please fill in all fields.');
      return;
    }

    // Validate delivery date is within the next 5 days
    const currentDate = new Date();
    const deliveryDate = new Date(formData.delivery_date);
    const maxDate = new Date();
    maxDate.setDate(currentDate.getDate() + 5);

    if (deliveryDate < currentDate) {
      setError('Delivery date must be today or in the future.');
      return;
    }
    if (deliveryDate > maxDate) {
      setError('Delivery date must be within the next 5 days.');
      return;
    }

    // Prepare data for API request
    const requestData = {
      supplier_id: parseInt(formData.supplier_id),
      latitude: parseFloat(formData.latitude),
      longitude: parseFloat(formData.longitude),
      delivery_date: formData.delivery_date,
    };

    // Make API request to backend
    axios
      .post(`${process.env.REACT_APP_BACKEND_URL}/suppliers/check-weather-impact`, requestData)
      .then(res => {
        setResponseMessage(res.data.message);
        if (res.data.conditions) {
          setConditions(res.data.conditions);
        } else {
          setConditions([]);
        }
      })
      .catch(err => {
        console.error(err);
        if (err.response && err.response.data && err.response.data.detail) {
          setError(err.response.data.detail);
        } else {
          setError('An error occurred while checking weather impact.');
        }
      });
  };

  return (
    <div className="weather-impact-container">
      <h1>Check Weather Impact on Delivery Compliance</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Supplier ID:</label>
          <input
            type="number"
            name="supplier_id"
            value={formData.supplier_id}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Latitude:</label>
          <input
            type="number"
            step="any"
            name="latitude"
            value={formData.latitude}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Longitude:</label>
          <input
            type="number"
            step="any"
            name="longitude"
            value={formData.longitude}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Delivery Date:</label>
          <input
            type="date"
            name="delivery_date"
            value={formData.delivery_date}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit">Check Weather Impact</button>
      </form>

      {responseMessage && (
        <div style={{ marginTop: '20px' }}>
          <h2>Result:</h2>
          <p>{responseMessage}</p>
          {conditions.length > 0 && (
            <div>
              <h3>Adverse Weather Conditions Detected:</h3>
              <ul>
                {conditions.map((condition, index) => (
                  <li key={index}>{condition}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {error && (
        <div style={{ marginTop: '20px', color: 'red' }}>
          <h2>Error:</h2>
          <p>{error}</p>
        </div>
      )}
    </div>
  );
}

export default WeatherImpact;
