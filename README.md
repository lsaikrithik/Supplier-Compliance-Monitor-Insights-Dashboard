# Supplier Compliance Monitor & Insights Dashboard

## Overview
The Supplier Compliance Monitor & Insights Dashboard is a full-stack application designed to help procurement teams track and manage supplier compliance with contract terms. Key features include:
- Monitoring supplier compliance with delivery times, quality standards, and agreed discounts.
- Uploading and analyzing compliance data for suppliers.
- Generating AI-driven insights to improve supplier relationships.
- Assessing weather impact on delivery compliance and adjusting records accordingly.

---

## Running the Application

### Prerequisites:
- **Backend:** Python 3.8+, PostgreSQL, API keys for OpenAI (or equivalent) and OpenWeatherMap.
- **Frontend:** Node.js and npm.

---

## Backend Setup

1. **Create the Database:**  
   Create the database `supplier_compliance_db` in PostgreSQL.

2. **Activate Virtual Environment:**  
   ```bash
   .\venv\Scripts\activate
   ```

3. **Install Required Packages:**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Tables:**  
   Run the backend server once to initialize tables.

5. **Seed the Database:**  
   ```bash
   python seed_data.py
   ```

6. **Set Up Environment Variables:**  
   Create a `.env` file with the necessary variables (database URL, API keys).

7. **Start the Backend Server:**  
   ```bash
   cd backend
   uvicorn main:app --reload
   ```  
   The backend API runs at [http://localhost:8000](http://localhost:8000).

---

## Frontend Setup

1. **Install Dependencies:**  
   ```bash
   cd frontend
   npm install
   ```

2. **Configure Environment Variables:**  
   Set the backend API URL as required.

3. **Start the Frontend Server:**  
   ```bash
   npm start
   ```  
   The frontend is available at [http://localhost:3000](http://localhost:3000).

4. **Handling Missing Installations:**  
   If any installations are missing, install them using:
   ```bash
   npm install <the_file_name>
   ```

---

## Using the Application

- **View Suppliers:** Visit [http://localhost:3000/](http://localhost:3000/).
- **Supplier Details:** Click on a supplier for more information.
- **Upload Compliance Data:** Use "Upload Compliance Data" to submit records.
- **Check Weather Impact:** Use "Check Weather Impact" to analyze delivery delays.

---

## Backend (FastAPI)

The backend serves as the core of the application, managing data processing, database interactions, API endpoints, AI integration, and external API communication.

### Components

#### Models
- **Supplier Model:** Stores supplier data, including name, country, compliance score, contract terms, and last audit date.
- **ComplianceRecord Model:** Tracks supplier compliance metrics, including supplier ID, recorded date, result, and status.

#### Database Connection
- **SQLAlchemy ORM:** Interacts with a PostgreSQL database using Python objects.
- **Database Session Management:** Ensures proper handling of database sessions per request.

#### API Endpoints
- `GET /suppliers` - Retrieves all suppliers.
- `GET /suppliers/{supplier_id}` - Retrieves details of a specific supplier, including compliance records.
- `POST /suppliers/check-compliance` - Uploads and validates new compliance data.
- `GET /suppliers/insights/{supplier_id}` - Generates AI-driven insights based on compliance history.
- `POST /suppliers/check-weather-impact` - Assesses weather impact on delivery compliance using the OpenWeatherMap API.

#### AI Integration
- **AI Service (e.g., OpenAI API):** Analyzes compliance data and provides insights to improve supplier relationships.

#### External API Integration
- **OpenWeatherMap API:** Retrieves weather data to assess delivery compliance impact.

### Process Flow
1. **Request Processing:** Validates input and required fields.
2. **Database Interaction:** Queries or updates data as necessary.
3. **External Service Integration:** Fetches AI insights and weather data.
4. **Response Handling:** Returns data or confirmation messages in JSON format.

---

## Frontend (React.js)

The frontend provides an interactive interface for users to monitor suppliers, upload compliance data, and access insights.

### Components
- **SupplierList:** Displays all suppliers and their compliance scores.
- **SupplierDetail:** Shows details of a selected supplier, including compliance records and AI insights.
- **ComplianceUpload:** Form for uploading new compliance data.
- **WeatherImpact:** Checks weather-related delivery disruptions.

### Data Handling
- **Axios/Fetch API:** Manages HTTP requests to backend endpoints.
- **State Management:** Utilizes React's `useState` and `useEffect` hooks.
- **Routing:** Uses React Router for seamless navigation.

---

## Notes

- **API Key Security:** Store API keys securely and avoid committing them to version control.
- **CORS Configuration:** Adjust `main.py` if frontend-backend origins differ.
- **Data Validation:** Ensure required fields are included in requests.
- **Error Handling:** Implement graceful error management.
- **Weather API Limitations:** The free plan only allows forecasting for the next five days.

---

## Summary

- **Backend:** Manages data, API requests, and integrations.
- **Frontend:** Provides an intuitive user interface.
- **Integration:** Uses API communication between frontend and backend for seamless functionality.
``` 

