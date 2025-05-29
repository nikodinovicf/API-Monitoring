# API_Prometheus 🚀
A Flask-based API with Prometheus monitoring, Alertmanager, and Grafana integration.

## Features 🔥
- **Flask REST API** with SQLAlchemy
- **Prometheus Metrics** for monitoring requests
- **Health Check Endpoint** (`/api/healthz`) to verify database status
- **Dockerized Setup** with `docker-compose`
- **Grafana Dashboard** for API performance visualization

---

✅ **Ensure `config.py` is inside `app/`, NOT `app/app/`.**  
✅ **Confirm `database.db` is inside `database/`.**  

---

## 🚀 Getting Started
### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/your-repo/API_Prometheus.git
cd API_Prometheus
```
### 2️⃣ **Build & Start Containers**
```sh
docker-compose up --build
```
### 3️⃣ **Check Active Routes**
```sh
docker exec -it flask_app-1 bash
python -m flask routes
```
### 4️⃣ **Health Check API**
```sh
curl -X GET http://localhost:5050/api/healthz
```

📊 Monitoring with Grafana

    Access Grafana at http://localhost:3000
    Log in (admin/admin)
    Import Prometheus Data Source
    Visualize API Performance 📈


