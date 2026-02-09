# 🌍 CLIMA — Autonomous Climate Intelligence System

CLIMA is an autonomous climate intelligence system that detects environmental anomalies, reasons about their causes using Gemini, and generates real-time response plans. It transforms raw climate signals into actionable decision intelligence.

---

##  What CLIMA Does

CLIMA continuously monitors multiple environmental dimensions:

-  Air Quality (PM2.5 / PM10)
-  Fire Hotspots
-  Weather Conditions
-  River Water Levels

When anomalies emerge, CLIMA:
1. Detects the anomaly
2. Builds a **causal explanation graph**
3. Infers root causes using **Gemini**
4. Generates mitigation and response plans
5. Serves results via an interactive dashboard

---

##  Gemini Integration

CLIMA uses **Google Gemini (gemini-2.5-flash)** as a core reasoning engine:

- Converts structured environmental snapshots into **causal narratives**
- Produces **machine-readable JSON** with:
  - Incident type
  - Root cause
  - Causal chain
  - Impact assessment
  - Confidence score
- Generates response plans for:
  - Citizens
  - Emergency services
  - Government authorities

Gemini reasoning is **cached per anomaly** and includes retry + backoff logic to optimize quota usage.

---

##  System Architecture
Data Sources
(AQI | Fire | Weather | River)

↓

Anomaly Detection Agent

↓

Causal Reasoning Agent (Gemini)

↓

Causal Graph Builder

↓

Response Planning Agent

↓

Validation & Confidence Check

↓

API + Frontend Dashboard

---


##  Frontend Dashboard

The UI provides real-time climate intelligence:

-  Interactive **causal graph**
-  AQI trend visualization with thresholds
-  Fire hotspot map
-  Structured response plan
-  Visual severity indicators

Built as a lightweight static frontend consuming backend APIs.

---

##  Built With

- **Python** (core logic, agents)
- **FastAPI** (API layer)
- **Google Gemini API**
- **HTML / CSS / JavaScript**
- **Chart.js** (AQI graphs)
- **Vis.js** (causal graphs)
- **Leaflet.js** (maps)

Dummy datasets are used to simulate global environmental coverage.

---

## Setup Instructions

###  Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
export GEMINI_API_KEY=your_api_key_here
```

---
##  Running the Project
### Backend
```bash
python backend/main.py
```
### Frontend
```
open : frontend/index.html
API endpoint : GET http://localhost:8000/incident
```
